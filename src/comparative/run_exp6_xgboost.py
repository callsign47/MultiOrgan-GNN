import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

from src.comparative.pipeline import FINAL_COHORT_PATH, FEATURE_DOMAINS
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import (
    compute_regression_metrics, aggregate_fold_metrics, paired_bootstrap_comparison
)

EXP6_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp6_ablations"
CFG_OUT_DIR  = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp6_ablations"
os.makedirs(EXP6_OUT_DIR, exist_ok=True)
os.makedirs(CFG_OUT_DIR,  exist_ok=True)

SEED = 42
DOMAINS = FEATURE_DOMAINS
ALL_FEATURES = [f for feats in DOMAINS.values() for f in feats]

XGB_CONFIG = {
    "n_estimators": 360,
    "max_depth": 5,
    "learning_rate": 0.03,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 3,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "tree_method": "hist",
    "random_state": SEED,
    "n_jobs": -1
}

def preprocess_tabular_fold(df, train_uids, val_uids, feature_cols):
    train_df = df[df["patient_uid"].isin(set(train_uids))].copy()
    val_df   = df[df["patient_uid"].isin(set(val_uids))].copy()

    X_tr_raw = train_df[feature_cols].values
    y_tr     = train_df["fib4_target"].values
    X_va_raw = val_df[feature_cols].values
    y_va     = val_df["fib4_target"].values
    val_seqns   = val_df["SEQN"].tolist()
    val_pat_ids = val_df["patient_uid"].tolist()

    imp = SimpleImputer(strategy="median")
    scl = StandardScaler()
    X_tr = scl.fit_transform(imp.fit_transform(X_tr_raw))
    X_va = scl.transform(imp.transform(X_va_raw))
    return X_tr, y_tr, X_va, y_va, val_seqns, val_pat_ids

def run_xgb_full_cv(df, folds_info, feature_cols, label):
    fold_metrics, oof_records = [], []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        X_tr, y_tr, X_va, y_va, val_seqns, val_pids = preprocess_tabular_fold(
            df, fd["train_patient_uids"], fd["val_patient_uids"], feature_cols)
        model = xgb.XGBRegressor(**XGB_CONFIG)
        model.fit(X_tr, y_tr, verbose=False)
        preds = model.predict(X_va)
        fm = compute_regression_metrics(y_va, preds)
        fold_metrics.append(fm)
        for s, uid, yt, yp in zip(val_seqns, val_pids, y_va, preds):
            oof_records.append({"SEQN": s, "patient_uid": uid, "fold": f_num,
                                "y_true": float(yt), "y_pred": float(yp)})
    agg = aggregate_fold_metrics(fold_metrics)
    pooled = compute_regression_metrics(
        [r["y_true"] for r in oof_records], [r["y_pred"] for r in oof_records])
    return oof_records, fold_metrics, agg, pooled

def main():
    print("=" * 74)
    print("  RUNNING EXPERIMENT 6a: XGBOOST FEATURE-DOMAIN ABLATIONS")
    print("=" * 74)
    t0_all = time.time()
    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()

    ablation_configs = {"FULL_25": {"type": "full_reference", "features": ALL_FEATURES}}
    domain_names = list(DOMAINS.keys())
    for dn in domain_names:
        loo_feats = [f for dom, feats in DOMAINS.items() for f in feats if dom != dn]
        ablation_configs[f"LOO_{dn}"] = {"type": "leave_one_out", "excluded_domain": dn, "features": loo_feats}
    for dn in domain_names:
        ablation_configs[f"ONLY_{dn}"] = {"type": "single_domain", "domain": dn, "features": DOMAINS[dn]}

    results = {
        "experiment": "Exp6a_XGBoost_FeatureDomainAblation",
        "xgb_config": XGB_CONFIG,
        "ablations": {},
        "bootstrap_vs_full": {}
    }

    full_preds, full_true = None, None

    for abl_name, abl_cfg in ablation_configs.items():
        feat_cols = abl_cfg["features"]
        t0 = time.time()
        oof_recs, fold_ms, agg, pooled = run_xgb_full_cv(df, folds_info, feat_cols, abl_name)
        elapsed = time.time() - t0

        oof_csv = os.path.join(EXP6_OUT_DIR, f"XGBoost_{abl_name}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        if abl_name == "FULL_25":
            full_preds = np.array([r["y_pred"] for r in oof_recs])
            full_true  = np.array([r["y_true"] for r in oof_recs])

        results["ablations"][abl_name] = {
            "config": abl_cfg,
            "features_count": len(feat_cols),
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv,
            "elapsed_sec": round(elapsed, 2)
        }
        print(f"  {abl_name:<20} ({len(feat_cols):>2} feats): Pooled R2={pooled['r2']:.4f} | "
              f"Mean R2={agg['r2_mean']:.4f}+-{agg['r2_std']:.4f} | RMSE={pooled['rmse']:.4f} [{elapsed:.1f}s]")

    # Bootstrap vs full
    print("\nCalculating paired patient-level bootstrap tests vs FULL_25 (B=2,000)...")
    for abl_name in ablation_configs:
        if abl_name == "FULL_25":
            continue
        abl_df = pd.read_csv(results["ablations"][abl_name]["oof_csv"])
        bt = paired_bootstrap_comparison(full_true, full_preds, abl_df["y_pred"].values,
                                         n_bootstraps=2000, seed=SEED)
        results["bootstrap_vs_full"][abl_name] = bt
        sig = "YES (Full > Abl)" if bt["a_significantly_better_r2"] else ("YES (Abl > Full)" if bt["b_significantly_better_r2"] else "NO")
        print(f"  {abl_name:<20}: Delta R2={bt['observed_delta_r2']:+.4f} | 95% CI=[{bt['ci_r2'][0]:+.4f}, {bt['ci_r2'][1]:+.4f}] | Sig: {sig}")

    out_json = os.path.join(EXP6_OUT_DIR, "exp6_xgboost_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)

    total_el = time.time() - t0_all
    print(f"\nAll 11 XGBoost ablations completed in {total_el:.1f}s (~{total_el/60:.1f}m).")
    print(f"Results saved to: {out_json}")

if __name__ == "__main__":
    main()
