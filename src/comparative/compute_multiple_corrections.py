import os, sys, json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('.'))
from src.comparative.metrics import compute_regression_metrics

EXP6_DIR = r"results/comparative/exp6_ablations"
SEED = 42
N_BOOTSTRAPS = 2000

def compute_paired_bootstrap_pvalue(y_true, y_pred_a, y_pred_b, n_bootstraps=2000, seed=42):
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    y_pred_a = np.asarray(y_pred_a)
    y_pred_b = np.asarray(y_pred_b)
    n = len(y_true)

    base_a = compute_regression_metrics(y_true, y_pred_a)
    base_b = compute_regression_metrics(y_true, y_pred_b)
    obs_delta_r2 = base_a['r2'] - base_b['r2']
    obs_delta_rmse = base_a['rmse'] - base_b['rmse']
    obs_delta_mae = base_a['mae'] - base_b['mae']

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

    boot_delta_r2 = np.array(boot_delta_r2)
    boot_delta_rmse = np.array(boot_delta_rmse)
    boot_delta_mae = np.array(boot_delta_mae)

    ci_r2 = [float(np.percentile(boot_delta_r2, 2.5)), float(np.percentile(boot_delta_r2, 97.5))]
    ci_rmse = [float(np.percentile(boot_delta_rmse, 2.5)), float(np.percentile(boot_delta_rmse, 97.5))]
    ci_mae = [float(np.percentile(boot_delta_mae, 2.5)), float(np.percentile(boot_delta_mae, 97.5))]

    # Two-sided empirical bootstrap p-value
    prop_leq_0 = np.mean(boot_delta_r2 <= 0)
    prop_geq_0 = np.mean(boot_delta_r2 >= 0)
    raw_p = float(min(1.0, 2.0 * min(prop_leq_0, prop_geq_0)))

    return {
        "observed_delta_r2": float(obs_delta_r2),
        "ci_r2": ci_r2,
        "observed_delta_rmse": float(obs_delta_rmse),
        "ci_rmse": ci_rmse,
        "observed_delta_mae": float(obs_delta_mae),
        "ci_mae": ci_mae,
        "raw_p_value": raw_p,
        "a_significantly_better_r2": bool(ci_r2[0] > 0),
        "b_significantly_better_r2": bool(ci_r2[1] < 0)
    }

def holm_bonferroni_correction(results_dict):
    """
    Apply Holm-Bonferroni step-down correction to a dict of test results.
    Each value in results_dict must have 'raw_p_value'.
    """
    keys = list(results_dict.keys())
    p_vals = [results_dict[k]["raw_p_value"] for k in keys]
    m = len(keys)

    # Sort indices by p-value ascending
    sorted_indices = np.argsort(p_vals)
    sorted_keys = [keys[i] for i in sorted_indices]
    sorted_p = [p_vals[i] for i in sorted_indices]

    # Compute step-down adjusted p-values
    adj_p = [0.0] * m
    running_max = 0.0
    for rank, (k, p) in enumerate(zip(sorted_keys, sorted_p)):
        mult = m - rank
        val = min(1.0, mult * p)
        running_max = max(running_max, val)
        adj_p[rank] = min(1.0, running_max)

    # Put back into dict
    corrected = {}
    for orig_idx, k in enumerate(keys):
        # find position in sorted_keys
        pos = sorted_keys.index(k)
        res = dict(results_dict[k])
        res["holm_p_value"] = float(adj_p[pos])
        res["holm_significant_05"] = bool(adj_p[pos] < 0.05)
        corrected[k] = res

    return corrected

def run_exp6a_corrections():
    print("Computing Exp 6a (XGBoost) Holm-Bonferroni corrections...")
    full_df = pd.read_csv(os.path.join(EXP6_DIR, "XGBoost_FULL_25_oof.csv"))
    y_true = full_df["y_true"].values
    full_pred = full_df["y_pred"].values

    variants = [
        "LOO_Demographics", "LOO_Liver", "LOO_Kidney", "LOO_Heart", "LOO_Biomarker",
        "ONLY_Demographics", "ONLY_Liver", "ONLY_Kidney", "ONLY_Heart", "ONLY_Biomarker"
    ]

    tests = {}
    for v in variants:
        v_df = pd.read_csv(os.path.join(EXP6_DIR, f"XGBoost_{v}_oof.csv"))
        v_pred = v_df["y_pred"].values
        tests[v] = compute_paired_bootstrap_pvalue(y_true, full_pred, v_pred, n_bootstraps=N_BOOTSTRAPS, seed=SEED)

    corrected = holm_bonferroni_correction(tests)
    return corrected

def run_exp6b_corrections():
    print("Computing Exp 6b (HSGIN) Holm-Bonferroni corrections...")
    full_df = pd.read_csv(os.path.join(EXP6_DIR, "HSGIN_FULL_25_oof.csv"))
    y_true = full_df["y_true"].values
    full_pred = full_df["y_pred"].values

    variants = ["LOO_Demographics", "LOO_Liver", "LOO_Kidney", "LOO_Heart", "LOO_Biomarker"]
    tests = {}
    for v in variants:
        v_df = pd.read_csv(os.path.join(EXP6_DIR, f"HSGIN_{v}_oof.csv"))
        v_pred = v_df["y_pred"].values
        tests[v] = compute_paired_bootstrap_pvalue(y_true, full_pred, v_pred, n_bootstraps=N_BOOTSTRAPS, seed=SEED)

    corrected = holm_bonferroni_correction(tests)
    return corrected

def run_exp7_corrections():
    print("Computing Exp 7 (Graph Architecture) Holm-Bonferroni corrections...")
    ref_df = pd.read_csv(r"results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv")
    y_true = ref_df["y_true"].values
    full_pred = ref_df["y_pred"].values

    variants = ["NoCrossTalk", "FlatReadout", "RandomEdges", "HomoGNN"]
    tests = {}
    for v in variants:
        v_csv = os.path.join(EXP6_DIR, f"HSGIN_Variant_{v}_oof.csv")
        if not os.path.exists(v_csv):
            print(f"  Warning: {v_csv} not ready yet.")
            return None
        v_df = pd.read_csv(v_csv)
        v_pred = v_df["y_pred"].values
        tests[v] = compute_paired_bootstrap_pvalue(y_true, full_pred, v_pred, n_bootstraps=N_BOOTSTRAPS, seed=SEED)

    corrected = holm_bonferroni_correction(tests)
    return corrected

if __name__ == "__main__":
    c6a = run_exp6a_corrections()
    print("\n--- Exp 6a (XGBoost) Corrected ---")
    for k, v in c6a.items():
        print(f"  {k:18s} | Delta R2={v['observed_delta_r2']:+.4f} | 95% CI=[{v['ci_r2'][0]:+.4f}, {v['ci_r2'][1]:+.4f}] | raw_p={v['raw_p_value']:.4f} | holm_p={v['holm_p_value']:.4f} | Sig: {v['holm_significant_05']}")

    c6b = run_exp6b_corrections()
    print("\n--- Exp 6b (HSGIN) Corrected ---")
    for k, v in c6b.items():
        print(f"  {k:18s} | Delta R2={v['observed_delta_r2']:+.4f} | 95% CI=[{v['ci_r2'][0]:+.4f}, {v['ci_r2'][1]:+.4f}] | raw_p={v['raw_p_value']:.4f} | holm_p={v['holm_p_value']:.4f} | Sig: {v['holm_significant_05']}")

    # Save to json
    with open(os.path.join(EXP6_DIR, "exp6a_bootstrap_holm.json"), "w") as f:
        json.dump(c6a, f, indent=2)
    with open(os.path.join(EXP6_DIR, "exp6b_bootstrap_holm.json"), "w") as f:
        json.dump(c6b, f, indent=2)
    print("Saved exp6a and exp6b corrections.")
