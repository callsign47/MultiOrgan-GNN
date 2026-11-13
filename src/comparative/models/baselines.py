import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric.nn as pyg_nn
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor

# Standard GNN Baseline (operating on homogeneous graph projection)
class StandardGNNBaseline(nn.Module):
    def __init__(self, in_dim, hidden_dim=64, gnn_type='gcn', dropout=0.2):
        super().__init__()
        self.gnn_type = gnn_type.lower()
        if self.gnn_type == 'gcn':
            self.conv1 = pyg_nn.GCNConv(in_dim, hidden_dim)
            self.conv2 = pyg_nn.GCNConv(hidden_dim, hidden_dim)
        elif self.gnn_type == 'gat':
            self.conv1 = pyg_nn.GATConv(in_dim, hidden_dim // 2, heads=2)
            self.conv2 = pyg_nn.GATConv(hidden_dim, hidden_dim // 2, heads=2)
        elif self.gnn_type == 'graphsage':
            self.conv1 = pyg_nn.SAGEConv(in_dim, hidden_dim)
            self.conv2 = pyg_nn.SAGEConv(hidden_dim, hidden_dim)
        else:
            raise ValueError(f"Unknown GNN type: {gnn_type}")
            
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, x, edge_index, batch):
        h = F.relu(self.conv1(x, edge_index))
        h = F.relu(self.conv2(h, edge_index))
        # Global mean pooling
        h_pool = pyg_nn.global_mean_pool(h, batch)
        return self.fc(h_pool).squeeze(-1)

# Classical HGNN Baseline (Flat heterogeneous Conv without organ-aware readout)
class ClassicalHGNN(nn.Module):
    def __init__(self, in_dim_dict, hidden_dim=64, dropout=0.2):
        super().__init__()
        self.node_types = list(in_dim_dict.keys())
        self.encoder_dict = nn.ModuleDict({
            ntype: nn.Linear(dim, hidden_dim) for ntype, dim in in_dim_dict.items()
        })
        
        conv_dict = {}
        edge_types = [
            ('patient', 'pertains_to', 'liver'),
            ('liver', 'rev_pertains_to', 'patient'),
            ('patient', 'pertains_to', 'kidney'),
            ('kidney', 'rev_pertains_to', 'patient'),
            ('patient', 'pertains_to', 'heart'),
            ('heart', 'rev_pertains_to', 'patient'),
            ('patient', 'pertains_to', 'biomarker'),
            ('biomarker', 'rev_pertains_to', 'patient'),
            ('liver', 'interacts_with', 'kidney'),
            ('kidney', 'interacts_with', 'liver'),
            ('liver', 'interacts_with', 'heart'),
            ('heart', 'interacts_with', 'liver'),
            ('kidney', 'interacts_with', 'heart'),
            ('heart', 'interacts_with', 'kidney')
        ]
        for src, rel, dst in edge_types:
            conv_dict[(src, rel, dst)] = pyg_nn.SAGEConv(hidden_dim, hidden_dim)
            
        self.hetero_conv = pyg_nn.HeteroConv(conv_dict, aggr='mean')
        
        # Simple readout (patient node only)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, batch_graph):
        x_dict = {ntype: self.encoder_dict[ntype](batch_graph[ntype].x) for ntype in self.node_types}
        h_dict = self.hetero_conv(x_dict, batch_graph.edge_index_dict)
        h_patient = h_dict['patient']
        return self.fc(h_patient).squeeze(-1)

def get_tabular_baselines():
    return {
        'Ridge_Regression': Ridge(alpha=1.0),
        'Random_Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=42),
        'MLP_Regressor': MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    }
