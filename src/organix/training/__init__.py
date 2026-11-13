"""
ORGANIX Training Package.
"""

from organix.training.loss import get_loss_function
from organix.training.trainer import train_gnn_model_fold

__all__ = [
    "get_loss_function",
    "train_gnn_model_fold",
]
