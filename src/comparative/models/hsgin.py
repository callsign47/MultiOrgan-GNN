import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric.nn as pyg_nn

class HeteroOrganConvBlock(nn.Module):
    def __init__(self, in_channels_dict, out_channels, heads=2):
        super().__init__()
        conv_dict = {}
        # Create message passing convolution per edge type
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
            if src in in_channels_dict and dst in in_channels_dict:
                in_dim = in_channels_dict[src]
                conv_dict[(src, rel, dst)] = pyg_nn.GATConv(
                    in_channels=in_dim,
                    out_channels=out_channels // heads,
                    heads=heads,
                    concat=True,
                    add_self_loops=False
                )
            
        self.conv = pyg_nn.HeteroConv(conv_dict, aggr='mean')

    def forward(self, x_dict, edge_index_dict):
        return self.conv(x_dict, edge_index_dict)


class HSGIN(nn.Module):
    """
    Heterogeneous Systemic Graph Interaction Network (HSGIN)
    Predicts FIB-4 continuous score strictly from non-FIB-4 multi-organ interaction cross-talk.
    """
    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())
        
        # Initial feature encoders per node type
        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            )
            
        # Message passing layers
        self.conv_layers = nn.ModuleList()
        dim_dict = {ntype: hidden_dim for ntype in self.node_types}
        for _ in range(num_layers):
            self.conv_layers.append(HeteroOrganConvBlock(dim_dict, hidden_dim, heads=2))
            
        # Organ-Aware Readout & Prediction MLP Head
        # Readout concats: [patient (H), organ_pool (H), biomarker (H)] -> 3 * H
        readout_dim = hidden_dim * 3
        self.predict_head = nn.Sequential(
            nn.Linear(readout_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, batch_graph):
        x_dict = batch_graph.x_dict
        edge_index_dict = batch_graph.edge_index_dict
        
        # 1. Project node features to hidden_dim
        h_dict = {}
        for ntype in self.node_types:
            h_dict[ntype] = self.encoder_dict[ntype](x_dict[ntype])
            
        # 2. Heterogeneous Message Passing
        for conv in self.conv_layers:
            h_new = conv(h_dict, edge_index_dict)
            for ntype in h_dict.keys():
                if ntype in h_new:
                    h_dict[ntype] = F.relu(h_dict[ntype] + h_new[ntype]) # Residual connection
                    
        # 3. Organ-Aware Readout Layer
        h_patient = h_dict['patient']
        h_biomarker = h_dict['biomarker']
        
        # Mean pool across target organ nodes present in the graph
        active_organs = []
        for ntype in ['liver', 'kidney', 'heart']:
            if ntype in h_dict:
                active_organs.append(h_dict[ntype])
                
        if len(active_organs) > 0:
            h_organ_pool = torch.stack(active_organs, dim=0).mean(dim=0)
        else:
            h_organ_pool = torch.zeros_like(h_patient)
        
        # Concatenate patient, pooled organ representations, and systemic biomarkers
        h_repr = torch.cat([h_patient, h_organ_pool, h_biomarker], dim=-1)
        
        # 4. Predict scalar FIB-4 score
        out = self.predict_head(h_repr).squeeze(-1)
        return out
