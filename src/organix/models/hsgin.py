"""
ORGANIX HSGIN (Heterogeneous Systemic Graph Interaction Network) Model Architecture.
"""

from typing import Dict, List, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric.nn as pyg_nn
from torch_geometric.data import HeteroData
from organix.core.constants import EDGE_TYPES


class HeteroOrganConvBlock(nn.Module):
    """
    Heterogeneous Organ Interaction Convolution Block.
    Computes multi-head graph attention (GATConv) across physiological relations.
    """
    def __init__(self, in_channels_dict: Dict[str, int], out_channels: int, heads: int = 2):
        super().__init__()
        conv_dict = {}
        for src, rel, dst in EDGE_TYPES:
            if src in in_channels_dict and dst in in_channels_dict:
                in_dim = in_channels_dict[src]
                conv_dict[(src, rel, dst)] = pyg_nn.GATConv(
                    in_channels=in_dim,
                    out_channels=out_channels // heads,
                    heads=heads,
                    concat=True,
                    add_self_loops=False,
                )
        self.conv = pyg_nn.HeteroConv(conv_dict, aggr="mean")

    def forward(self, x_dict: Dict[str, torch.Tensor], edge_index_dict: Dict[tuple, torch.Tensor]) -> Dict[str, torch.Tensor]:
        return self.conv(x_dict, edge_index_dict)


class HSGIN(nn.Module):
    """
    Heterogeneous Systemic Graph Interaction Network (HSGIN).
    Predicts continuous FIB-4 score strictly from non-formula multi-organ interaction cross-talk.

    Architecture:
      1. Node feature encoders per organ type with LayerNorm and Dropout.
      2. 2 Heterogeneous GAT message-passing layers with residual connections.
      3. Organ-Aware Readout layer concatenating patient node, pooled target organs, and systemic biomarkers.
      4. Multi-layer projection regression head.
    """
    def __init__(
        self,
        in_dim_dict: Dict[str, int],
        hidden_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        # 1. Feature Encoders per node type
        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
            )

        # 2. Message Passing Layers
        self.conv_layers = nn.ModuleList()
        dim_dict = {ntype: hidden_dim for ntype in self.node_types}
        for _ in range(num_layers):
            self.conv_layers.append(HeteroOrganConvBlock(dim_dict, hidden_dim, heads=2))

        # 3. Readout & Prediction MLP Head
        # Readout concats: [patient (H), organ_pool (H), biomarker (H)] -> 3 * H
        readout_dim = hidden_dim * 3
        self.predict_head = nn.Sequential(
            nn.Linear(readout_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, batch_graph: HeteroData) -> torch.Tensor:
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
                    h_dict[ntype] = F.relu(h_dict[ntype] + h_new[ntype])

        # 3. Organ-Aware Readout Layer
        h_patient = h_dict["patient"]
        h_biomarker = h_dict["biomarker"]

        # Mean pool across target organ nodes present in the graph
        active_organs = []
        for ntype in ["liver", "kidney", "heart"]:
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
