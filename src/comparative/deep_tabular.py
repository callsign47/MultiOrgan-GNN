import os
import sys
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from pytorch_tabnet.tab_model import TabNetRegressor

class MLPRegressorPyTorch(nn.Module):
    def __init__(self, in_features=25, hidden_dims=[128, 64, 32], dropout=0.2):
        super().__init__()
        layers = []
        prev_dim = in_features
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.LayerNorm(h_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x).squeeze(-1)


class FeatureTokenizer(nn.Module):
    def __init__(self, num_features=25, embed_dim=32):
        super().__init__()
        self.num_features = num_features
        self.embed_dim = embed_dim
        self.weights = nn.Parameter(torch.empty(num_features, embed_dim))
        self.biases = nn.Parameter(torch.empty(num_features, embed_dim))
        self.cls_token = nn.Parameter(torch.empty(1, 1, embed_dim))
        self._init_weights()

    def _init_weights(self):
        nn.init.kaiming_uniform_(self.weights, a=np.sqrt(5))
        nn.init.zeros_(self.biases)
        nn.init.normal_(self.cls_token, std=0.02)

    def forward(self, x):
        # x: [batch_size, num_features]
        # output: [batch_size, 1 + num_features, embed_dim]
        tokens = x.unsqueeze(-1) * self.weights.unsqueeze(0) + self.biases.unsqueeze(0)
        batch_size = x.size(0)
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        return torch.cat([cls_tokens, tokens], dim=1)


class FTTransformer(nn.Module):
    def __init__(self, num_features=25, embed_dim=32, num_heads=4, num_layers=2, ffn_dim=64, dropout=0.1):
        super().__init__()
        self.tokenizer = FeatureTokenizer(num_features=num_features, embed_dim=embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ffn_dim,
            dropout=dropout,
            activation="relu",
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.head = nn.Sequential(
            nn.LayerNorm(embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, 1)
        )

    def forward(self, x):
        tokens = self.tokenizer(x)
        encoded = self.transformer(tokens)
        cls_repr = encoded[:, 0, :]
        return self.head(cls_repr).squeeze(-1)
