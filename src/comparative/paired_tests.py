import os
import sys
import json
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath('.'))
from src.comparative.metrics import paired_bootstrap_comparison

exp0_dir = r"results/comparative/exp0_reproduction"
exp1_dir = r"results/comparative/exp1_linear_trees"
exp2_dir = r"results/comparative/exp2_boosting"

oof_files = {
    'HSGIN': os.path.join(exp0_dir, 'HSGIN_oof_predictions.csv'),
    'Classical_HGNN': os.path.join(exp0_dir, 'Classical_HGNN_oof_predictions.csv'),
    'XGBoost_Exp0': os.path.join(exp0_dir, 'XGBoost_oof_predictions.csv'),
    'Random_Forest_Exp0': os.path.join(exp0_dir, 'Random_Forest_oof_predictions.csv'),
    'Ridge_Exp0': os.path.join(exp0_dir, 'Ridge_Regression_oof_predictions.csv'),
    'MLP_Exp0': os.path.join(exp0_dir, 'MLP_Regressor_oof_predictions.csv'),
    'Ridge_tuned': os.path.join(exp1_dir, 'Ridge_oof_predictions.csv'),
    'ElasticNet': os.path.join(exp1_dir, 'ElasticNet_oof_predictions.csv'),
    'RandomForest_tuned': os.path.join(exp1_dir, 'RandomForest_oof_predictions.csv'),
    'ExtraTrees': os.path.join(exp1_dir, 'ExtraTrees_oof_predictions.csv'),
    'XGBoost_tuned': os.path.join(exp2_dir, 'XGBoost_tuned_oof_predictions.csv'),
    'LightGBM': os.path.join(exp2_dir, 'LightGBM_oof_predictions.csv'),
    'CatBoost': os.path.join(exp2_dir, 'CatBoost_oof_predictions.csv'),
    'HistGradientBoosting': os.path.join(exp2_dir, 'HistGradientBoosting_oof_predictions.csv')
}

dfs = {}
for name, p in oof_files.items():
    df = pd.read_csv(p)
    df = df.sort_values('SEQN').reset_index(drop=True)
    dfs[name] = df

ref_seqn = dfs['HSGIN']['SEQN'].values
y_true = dfs['HSGIN']['y_true'].values
for name, df in dfs.items():
    assert np.array_equal(df['SEQN'].values, ref_seqn), f"SEQN mismatch in {name}"
    assert np.allclose(df['y_true'].values, y_true), f"y_true mismatch in {name}"

pairs_to_test = [
    ('HSGIN', 'XGBoost_tuned'),
    ('HSGIN', 'CatBoost'),
    ('HSGIN', 'Classical_HGNN'),
    ('HSGIN', 'ExtraTrees'),
    ('XGBoost_tuned', 'CatBoost'),
    ('XGBoost_tuned', 'LightGBM'),
    ('XGBoost_tuned', 'HistGradientBoosting'),
    ('XGBoost_tuned', 'XGBoost_Exp0'),
    ('CatBoost', 'XGBoost_Exp0'),
    ('ExtraTrees', 'RandomForest_tuned'),
    ('RandomForest_tuned', 'Random_Forest_Exp0'),
    ('Ridge_tuned', 'Ridge_Exp0'),
    ('ElasticNet', 'Ridge_tuned')
]

print("=== PAIRED BOOTSTRAP COMPARISONS (2,000 resamples, 95% CI) ===")
results = {}
for m_a, m_b in pairs_to_test:
    p_a = dfs[m_a]['y_pred'].values
    p_b = dfs[m_b]['y_pred'].values
    res = paired_bootstrap_comparison(y_true, p_a, p_b, n_bootstraps=2000, seed=42)
    results[f"{m_a} vs {m_b}"] = res
    ci_low = res["ci_r2"][0]
    ci_high = res["ci_r2"][1]
    d_r2 = res["observed_delta_r2"]
    d_rmse = res["observed_delta_rmse"]
    sig = "SIG DIFF (excludes 0)" if (ci_low > 0 or ci_high < 0) else "NOT SIGNIFICANT (overlaps 0)"
    print(f"{m_a:20s} vs {m_b:20s} | Delta R2: {d_r2:+.4f} [{ci_low:+.4f}, {ci_high:+.4f}] | Delta RMSE: {d_rmse:+.4f} | {sig}")

out_json = r"results/comparative/paired_bootstrap_phase3.json"
with open(out_json, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved detailed paired bootstrap comparisons to: {out_json}")
