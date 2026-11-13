"""
ORGANIX Feature and Domain Attribution (Permutation Importance).
"""

from typing import Dict, List, Any
import numpy as np
import pandas as pd
from organix.core.constants import FEATURE_DOMAINS
from organix.evaluation.metrics import compute_regression_metrics


def compute_permutation_importance(
    model: Any,
    X_val: np.ndarray,
    y_val: np.ndarray,
    feature_names: List[str],
    n_repeats: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Computes held-out feature permutation importance (R^2 drop upon shuffling feature column).
    """
    rng = np.random.default_rng(seed)
    base_metrics = compute_regression_metrics(y_val, model.predict(X_val))
    base_r2 = base_metrics["r2"]

    importance_records = []
    for feat_idx, feat_name in enumerate(feature_names):
        drops = []
        for _ in range(n_repeats):
            X_perm = X_val.copy()
            perm_idx = rng.permutation(len(X_val))
            X_perm[:, feat_idx] = X_perm[perm_idx, feat_idx]
            perm_metrics = compute_regression_metrics(y_val, model.predict(X_perm))
            drops.append(base_r2 - perm_metrics["r2"])

        importance_records.append({
            "feature": feat_name,
            "mean_r2_drop": float(np.mean(drops)),
            "std_r2_drop": float(np.std(drops)),
        })

    df = pd.DataFrame(importance_records).sort_values("mean_r2_drop", ascending=False).reset_index(drop=True)
    return df


def aggregate_domain_importance(feature_importance_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates single-feature importance drops into domain shares."""
    feat_to_domain = {}
    for dom, feats in FEATURE_DOMAINS.items():
        for f in feats:
            feat_to_domain[f] = dom

    df = feature_importance_df.copy()
    df["domain"] = df["feature"].map(feat_to_domain)

    domain_summary = (
        df.groupby("domain")["mean_r2_drop"]
        .agg(["sum", "mean", "count"])
        .reset_index()
        .rename(columns={"sum": "total_r2_drop", "mean": "avg_r2_drop", "count": "feature_count"})
    )
    total_drop = domain_summary["total_r2_drop"].sum()
    domain_summary["percentage_share"] = (domain_summary["total_r2_drop"] / total_drop) * 100.0
    return domain_summary.sort_values("total_r2_drop", ascending=False).reset_index(drop=True)
