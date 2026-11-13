"""
ORGANIX Benchmark Baseline Models (Classical GNN, Tabular, Tree Ensembles).
"""

from typing import Dict, Any
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric.nn as pyg_nn
from torch_geometric.data import HeteroData
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from organix.core.constants import EDGE_TYPES


class ClassicalHGNN(nn.Module):
    """
    Classical Heterogeneous Graph Neural Network (HeteroSAGE).
    Flat message-passing without organ-aware cross-talk readout (patient node readout only).
    """
    def __init__(self, in_dim_dict: Dict[str, int], hidden_dim: int = 64, dropout: float = 0.2):
        super().__init__()
        self.node_types = list(in_dim_dict.keys())
        self.encoder_dict = nn.ModuleDict({
            ntype: nn.Linear(dim, hidden_dim) for ntype, dim in in_dim_dict.items()
        })

        conv_dict = {}
        for src, rel, dst in EDGE_TYPES:
            conv_dict[(src, rel, dst)] = pyg_nn.SAGEConv(hidden_dim, hidden_dim)

        self.hetero_conv = pyg_nn.HeteroConv(conv_dict, aggr="mean")

        # Flat patient node readout only
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, batch_graph: HeteroData) -> torch.Tensor:
        x_dict = {ntype: self.encoder_dict[ntype](batch_graph[ntype].x) for ntype in self.node_types}
        h_dict = self.hetero_conv(x_dict, batch_graph.edge_index_dict)
        h_patient = h_dict["patient"]
        return self.fc(h_patient).squeeze(-1)


class StandardGNNBaseline(nn.Module):
    """Standard Homogeneous GNN Baseline (GCN, GAT, GraphSAGE)."""
    def __init__(self, in_dim: int, hidden_dim: int = 64, gnn_type: str = "graphsage", dropout: float = 0.2):
        super().__init__()
        self.gnn_type = gnn_type.lower()
        if self.gnn_type == "gcn":
            self.conv1 = pyg_nn.GCNConv(in_dim, hidden_dim)
            self.conv2 = pyg_nn.GCNConv(hidden_dim, hidden_dim)
        elif self.gnn_type == "gat":
            self.conv1 = pyg_nn.GATConv(in_dim, hidden_dim // 2, heads=2)
            self.conv2 = pyg_nn.GATConv(hidden_dim, hidden_dim // 2, heads=2)
        elif self.gnn_type == "graphsage":
            self.conv1 = pyg_nn.SAGEConv(in_dim, hidden_dim)
            self.conv2 = pyg_nn.SAGEConv(hidden_dim, hidden_dim)
        else:
            raise ValueError(f"Unknown GNN type: {gnn_type}")

        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
        h = F.relu(self.conv1(x, edge_index))
        h = F.relu(self.conv2(h, edge_index))
        h_pool = pyg_nn.global_mean_pool(h, batch)
        return self.fc(h_pool).squeeze(-1)


def get_tabular_baselines(seed: int = 42) -> Dict[str, Any]:
    """Returns baseline tabular models for reproduction."""
    return {
        "Ridge_Regression": Ridge(alpha=1.0),
        "Random_Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=seed),
        "XGBoost": XGBRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=seed),
    }
