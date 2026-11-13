"""
ORGANIX Statistical Hypothesis Testing, Paired Bootstrapping, and FDR Correction.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
from organix.evaluation.metrics import compute_regression_metrics


def paired_bootstrap_comparison(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray,
    n_bootstraps: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Patient-level paired non-parametric bootstrap test comparing Model A and Model B.
    Calculates 95% Confidence Intervals for Delta R^2, Delta RMSE, Delta MAE,
    and returns a two-sided empirical bootstrap p-value.
    """
    rng = np.random.default_rng(seed)
    yt = np.asarray(y_true, dtype=np.float64)
    ya = np.asarray(y_pred_a, dtype=np.float64)
    yb = np.asarray(y_pred_b, dtype=np.float64)
    n = len(yt)

    base_a = compute_regression_metrics(yt, ya)
    base_b = compute_regression_metrics(yt, yb)
    obs_delta_r2 = base_a["r2"] - base_b["r2"]
    obs_delta_rmse = base_a["rmse"] - base_b["rmse"]
    obs_delta_mae = base_a["mae"] - base_b["mae"]

    boot_delta_r2 = []
    boot_delta_rmse = []
    boot_delta_mae = []

    for _ in range(n_bootstraps):
        idx = rng.choice(n, size=n, replace=True)
        m_a = compute_regression_metrics(yt[idx], ya[idx])
        m_b = compute_regression_metrics(yt[idx], yb[idx])
        boot_delta_r2.append(m_a["r2"] - m_b["r2"])
        boot_delta_rmse.append(m_a["rmse"] - m_b["rmse"])
        boot_delta_mae.append(m_a["mae"] - m_b["mae"])

    boot_delta_r2 = np.array(boot_delta_r2)
    boot_delta_rmse = np.array(boot_delta_rmse)
    boot_delta_mae = np.array(boot_delta_mae)

    low_p = (alpha / 2.0) * 100
    high_p = (1.0 - alpha / 2.0) * 100

    ci_r2 = [float(np.percentile(boot_delta_r2, low_p)), float(np.percentile(boot_delta_r2, high_p))]
    ci_rmse = [float(np.percentile(boot_delta_rmse, low_p)), float(np.percentile(boot_delta_rmse, high_p))]
    ci_mae = [float(np.percentile(boot_delta_mae, low_p)), float(np.percentile(boot_delta_mae, high_p))]

    # Two-sided empirical p-value
    prop_leq_0 = np.mean(boot_delta_r2 <= 0)
    prop_geq_0 = np.mean(boot_delta_r2 >= 0)
    p_value = float(min(1.0, 2.0 * min(prop_leq_0, prop_geq_0)))

    return {
        "observed_delta_r2": float(obs_delta_r2),
        "ci_r2": ci_r2,
        "observed_delta_rmse": float(obs_delta_rmse),
        "ci_rmse": ci_rmse,
        "observed_delta_mae": float(obs_delta_mae),
        "ci_mae": ci_mae,
        "p_value": p_value,
        "a_significantly_better_r2": bool(ci_r2[0] > 0),
        "b_significantly_better_r2": bool(ci_r2[1] < 0),
    }


def apply_holm_bonferroni(p_values: List[float], alpha: float = 0.05) -> Tuple[List[float], List[bool]]:
    """
    Applies the step-down Holm-Bonferroni Family-Wise Error Rate (FWER) correction.
    """
    m = len(p_values)
    sorted_indices = np.argsort(p_values)
    adjusted_p = np.zeros(m)
    significant = np.zeros(m, dtype=bool)

    running_max = 0.0
    for rank, idx in enumerate(sorted_indices):
        raw_p = p_values[idx]
        adj_p = min(1.0, raw_p * (m - rank))
        running_max = max(running_max, adj_p)
        adjusted_p[idx] = min(1.0, running_max)
        significant[idx] = (adjusted_p[idx] < alpha)

    return adjusted_p.tolist(), significant.tolist()


def apply_benjamini_hochberg(p_values: List[float], fdr: float = 0.05) -> Tuple[List[float], List[bool]]:
    """
    Applies the Benjamini-Hochberg False Discovery Rate (FDR) procedure.
    """
    m = len(p_values)
    sorted_indices = np.argsort(p_values)
    adjusted_p = np.zeros(m)

    for rank, idx in enumerate(reversed(sorted_indices)):
        k = m - rank
        raw_p = p_values[idx]
        adj_p = min(1.0, raw_p * m / k)
        if rank > 0:
            adj_p = min(adj_p, adjusted_p[sorted_indices[k]])
        adjusted_p[idx] = adj_p

    significant = [p < fdr for p in adjusted_p]
    return adjusted_p.tolist(), significant
