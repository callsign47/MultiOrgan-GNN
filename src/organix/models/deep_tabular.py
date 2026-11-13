"""
ORGANIX Deep Tabular Neural Architectures (FT-Transformer and MLP).
"""

from typing import List, Optional
import numpy as np
import torch
import torch.nn as nn


class MLPRegressorPyTorch(nn.Module):
    """Deep Tabular Multi-Layer Perceptron with LayerNorm and Dropout."""
    def __init__(self, in_features: int = 25, hidden_dims: Optional[List[int]] = None, dropout: float = 0.2):
        super().__init__()
        dims = hidden_dims or [128, 64, 32]
        layers = []
        prev_dim = in_features
        for h_dim in dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.LayerNorm(h_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


class FeatureTokenizer(nn.Module):
    """Numerical feature embedding layer for FT-Transformer."""
    def __init__(self, num_features: int = 25, embed_dim: int = 32):
        super().__init__()
        self.num_features = num_features
        self.embed_dim = embed_dim
        self.weights = nn.Parameter(torch.empty(num_features, embed_dim))
        self.biases = nn.Parameter(torch.empty(num_features, embed_dim))
        self.cls_token = nn.Parameter(torch.empty(1, 1, embed_dim))
        self._init_weights()

    def _init_weights(self) -> None:
        nn.init.kaiming_uniform_(self.weights, a=np.sqrt(5))
        nn.init.zeros_(self.biases)
        nn.init.normal_(self.cls_token, std=0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # tokens: [batch_size, num_features, embed_dim]
        tokens = x.unsqueeze(-1) * self.weights.unsqueeze(0) + self.biases.unsqueeze(0)
        batch_size = x.size(0)
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        return torch.cat([cls_tokens, tokens], dim=1)


class FTTransformer(nn.Module):
    """Feature Tokenizer + Transformer Encoder for Deep Tabular learning."""
    def __init__(
        self,
        num_features: int = 25,
        embed_dim: int = 32,
        num_heads: int = 4,
        num_layers: int = 2,
        ffn_dim: int = 64,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.tokenizer = FeatureTokenizer(num_features=num_features, embed_dim=embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ffn_dim,
            dropout=dropout,
            activation="relu",
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.head = nn.Sequential(
            nn.LayerNorm(embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        tokens = self.tokenizer(x)
        encoded = self.transformer(tokens)
        cls_repr = encoded[:, 0, :]
        return self.head(cls_repr).squeeze(-1)
