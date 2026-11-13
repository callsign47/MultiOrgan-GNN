"""
ORGANIX Custom Layers & Building Blocks.
"""

import torch
import torch.nn as nn


class ResidualLinearBlock(nn.Module):
    """Linear projection with LayerNorm, ReLU, Dropout and residual skip connection."""
    def __init__(self, dim: int, dropout: float = 0.2):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(dim, dim),
            nn.LayerNorm(dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.fc(x)
