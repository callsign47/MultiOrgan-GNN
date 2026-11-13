"""
ORGANIX Performance Evaluation Metrics for Continuous Target Regression.
"""

from typing import Dict, List, Union
import numpy as np
from scipy.stats import spearmanr, pearsonr
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score


def compute_regression_metrics(
    y_true: Union[List[float], np.ndarray],
    y_pred: Union[List[float], np.ndarray],
) -> Dict[str, float]:
    """
    Computes primary performance metrics for continuous FIB-4 target regression:
      - R^2 (Coefficient of Determination)
      - MAE (Mean Absolute Error)
      - RMSE (Root Mean Squared Error)
      - Spearman's rho (Rank correlation)
      - Pearson's r (Linear correlation)
    """
    yt = np.asarray(y_true, dtype=np.float64)
    yp = np.asarray(y_pred, dtype=np.float64)

    mae = float(mean_absolute_error(yt, yp))
    rmse = float(root_mean_squared_error(yt, yp))
    r2 = float(r2_score(yt, yp))

    # Correlation metrics
    if len(yt) > 2 and np.std(yp) > 1e-9:
        s_rho, _ = spearmanr(yt, yp)
        p_r, _ = pearsonr(yt, yp)
    else:
        s_rho = 0.0
        p_r = 0.0

    return {
        "r2": r2,
        "mae": mae,
        "rmse": rmse,
        "spearman_rho": float(s_rho),
        "pearson_r": float(p_r),
    }


def aggregate_fold_metrics(fold_metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Aggregates fold-level metrics into mean and standard deviation across cross-validation folds.
    """
    if not fold_metrics_list:
        return {}
    keys = fold_metrics_list[0].keys()
    aggregated = {}
    for k in keys:
        values = [fm[k] for fm in fold_metrics_list]
        aggregated[f"{k}_mean"] = float(np.mean(values))
        aggregated[f"{k}_std"] = float(np.std(values))
    return aggregated
