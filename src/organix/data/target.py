"""
ORGANIX FIB-4 Target Computation and Specification.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def compute_fib4_score(age: pd.Series, ast: pd.Series, alt: pd.Series, platelets: pd.Series) -> pd.Series:
    """
    Computes the continuous FIB-4 index:
        FIB-4 = (Age * AST) / (Platelet Count * sqrt(ALT))
    
    Clinical Units:
        Age: years (RIDAGEYR)
        AST: U/L (LBXSASSI)
        ALT: U/L (LBXSATSI)
        Platelet Count: 10^9/L (LBXPLTSI)
    """
    denominator = platelets * np.sqrt(alt)
    # Guard against zero or negative division
    valid_mask = (platelets > 0) & (alt > 0) & (ast > 0) & (age > 0)
    fib4 = pd.Series(index=age.index, dtype=float)
    fib4[valid_mask] = (age[valid_mask] * ast[valid_mask]) / denominator[valid_mask]
    return fib4


def compute_target_distribution_moments(target_series: pd.Series) -> Dict[str, float]:
    """Computes distribution summary moments for validation."""
    clean = target_series.dropna()
    return {
        "count": float(len(clean)),
        "mean": float(clean.mean()),
        "std": float(clean.std()),
        "median": float(clean.median()),
        "min": float(clean.min()),
        "max": float(clean.max()),
        "skew": float(clean.skew()),
        "kurtosis": float(clean.kurtosis()),
    }
