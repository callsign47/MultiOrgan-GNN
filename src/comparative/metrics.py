import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

def compute_regression_metrics(y_true, y_pred):
    """
    Compute R2, MAE, and RMSE for 1D arrays of ground truth and predictions.
    """
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(root_mean_squared_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    
    return {
        "r2": r2,
        "mae": mae,
        "rmse": rmse
    }

def aggregate_fold_metrics(fold_metrics_list):
    """
    Compute mean and std across folds for a list of fold metric dictionaries.
    """
    keys = fold_metrics_list[0].keys()
    aggregated = {}
    for k in keys:
        values = [fm[k] for fm in fold_metrics_list]
        aggregated[f"{k}_mean"] = float(np.mean(values))
        aggregated[f"{k}_std"] = float(np.std(values))
    return aggregated

def paired_bootstrap_comparison(y_true, y_pred_a, y_pred_b, n_bootstraps=2000, alpha=0.05, seed=42):
    """
    Perform paired patient-level bootstrap comparison between Model A and Model B.
    Calculates 95% confidence intervals on:
    - Delta R2: R2(A) - R2(B)
    - Delta RMSE: RMSE(A) - RMSE(B)
    - Delta MAE: MAE(A) - MAE(B)
    """
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    y_pred_a = np.asarray(y_pred_a)
    y_pred_b = np.asarray(y_pred_b)
    n = len(y_true)

    base_a = compute_regression_metrics(y_true, y_pred_a)
    base_b = compute_regression_metrics(y_true, y_pred_b)
    observed_delta_r2 = base_a['r2'] - base_b['r2']
    observed_delta_rmse = base_a['rmse'] - base_b['rmse']
    observed_delta_mae = base_a['mae'] - base_b['mae']

    boot_delta_r2 = []
    boot_delta_rmse = []
    boot_delta_mae = []

    for _ in range(n_bootstraps):
        idx = rng.choice(n, size=n, replace=True)
        m_a = compute_regression_metrics(y_true[idx], y_pred_a[idx])
        m_b = compute_regression_metrics(y_true[idx], y_pred_b[idx])
        boot_delta_r2.append(m_a['r2'] - m_b['r2'])
        boot_delta_rmse.append(m_a['rmse'] - m_b['rmse'])
        boot_delta_mae.append(m_a['mae'] - m_b['mae'])

    low_p = (alpha / 2.0) * 100
    high_p = (1.0 - alpha / 2.0) * 100

    return {
        "observed_delta_r2": float(observed_delta_r2),
        "ci_r2": [float(np.percentile(boot_delta_r2, low_p)), float(np.percentile(boot_delta_r2, high_p))],
        "observed_delta_rmse": float(observed_delta_rmse),
        "ci_rmse": [float(np.percentile(boot_delta_rmse, low_p)), float(np.percentile(boot_delta_rmse, high_p))],
        "observed_delta_mae": float(observed_delta_mae),
        "ci_mae": [float(np.percentile(boot_delta_mae, low_p)), float(np.percentile(boot_delta_mae, high_p))],
        "a_significantly_better_r2": bool(np.percentile(boot_delta_r2, low_p) > 0),
        "b_significantly_better_r2": bool(np.percentile(boot_delta_r2, high_p) < 0)
    }
