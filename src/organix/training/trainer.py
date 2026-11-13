"""
ORGANIX Deterministic Model Trainer for PyG Graphs and PyTorch Neural Networks.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader
from torch_geometric.data import HeteroData
from organix.core.logging import get_logger
from organix.utils.seeding import seed_everything

logger = get_logger("organix.training.trainer")


def train_gnn_model_fold(
    model: nn.Module,
    train_graphs: List[HeteroData],
    val_graphs: List[HeteroData],
    epochs: int = 50,
    lr: float = 0.001,
    weight_decay: float = 1e-4,
    batch_size: int = 64,
    device: Optional[torch.device] = None,
    seed: int = 42,
) -> Tuple[nn.Module, List[float], List[float]]:
    """
    Trains a Heterogeneous GNN model (HSGIN or ClassicalHGNN) on train_graphs,
    evaluating on val_graphs at each epoch and selecting the checkpoint with the lowest validation loss.
    """
    seed_everything(seed)
    dev = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(dev)

    train_loader = PyGDataLoader(train_graphs, batch_size=batch_size, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=batch_size, shuffle=False)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.MSELoss()

    best_val_loss = float("inf")
    best_preds: List[float] = []
    best_targets: List[float] = []
    best_weights: Optional[Dict[str, torch.Tensor]] = None

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for batch in train_loader:
            batch = batch.to(dev)
            optimizer.zero_grad()
            out = model(batch)
            loss = criterion(out, batch["patient"].y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch.num_graphs

        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(dev)
                out = model(batch)
                val_preds.extend(out.cpu().numpy().flatten().tolist())
                val_targets.extend(batch["patient"].y.cpu().numpy().flatten().tolist())

        val_loss = np.mean((np.array(val_preds) - np.array(val_targets)) ** 2)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_preds = val_preds
            best_targets = val_targets
            best_weights = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    if best_weights is not None:
        model.load_state_dict(best_weights)

    return model, best_preds, best_targets
