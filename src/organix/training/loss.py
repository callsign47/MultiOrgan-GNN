"""
ORGANIX Loss Functions.
"""

import torch
import torch.nn as nn


def get_loss_function(loss_name: str = "mse") -> nn.Module:
    """Returns standard loss function for continuous target regression."""
    name = loss_name.lower()
    if name == "mse":
        return nn.MSELoss()
    elif name == "l1" or name == "mae":
        return nn.L1Loss()
    elif name == "smooth_l1" or name == "huber":
        return nn.SmoothL1Loss()
    else:
        raise ValueError(f"Unknown loss function: {loss_name}")
