"""
Experiment 2: Advanced Gradient Boosting Models with Inner-Validation Early Stopping
Models: XGBoost (re-tuned), LightGBM, CatBoost, HistGradientBoosting
- Fold-safe preprocessing: imputer + scaler fit strictly on train portion of each outer fold
- Inner 20% holdout split for early stopping (never touches outer val)
- XGBoost, LightGBM, CatBoost: native early stopping on inner holdout
- HistGradientBoosting: sklearn validation_fraction early stopping
- OOF predictions saved keyed by SEQN
"""
import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

from src.comparative.pipeline import FINAL_COHORT_PATH, get_leak_free_feature_list
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics, aggregate_fold_metrics

EXP2_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp2_boosting"
os.makedirs(EXP2_OUT_DIR, exist_ok=True)

SEED = 42
INNER_VAL_FRAC = 0.20       # 20% of training fold used as early-stopping holdout
EARLY_STOP_ROUNDS = 50
MAX_ROUNDS_XGBOOST   = 2000
MAX_ROUNDS_LGBM      = 2000
MAX_ROUNDS_CATBOOST  = 2000
MAX_ROUNDS_HISTGB    = 2000

# ── Shared hyperparameter configs ─────────────────────────────────────────────
CONFIGS = {
    "XGBoost_tuned": {
        "n_estimators": MAX_ROUNDS_XGBOOST,
        "max_depth": 5,
        "learning_rate": 0.03,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 3,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "tree_method": "hist",
        "early_stopping_rounds": EARLY_STOP_ROUNDS,
        "random_state": SEED,
        "n_jobs": -1
    },
    "LightGBM": {
        "n_estimators": MAX_ROUNDS_LGBM,
        "max_depth": 6,
        "num_leaves": 31,
        "learning_rate": 0.03,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_samples": 20,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": SEED,
        "n_jobs": -1,
        "verbose": -1
    },
    "CatBoost": {
        "iterations": MAX_ROUNDS_CATBOOST,
        "depth": 6,
        "learning_rate": 0.03,
        "l2_leaf_reg": 3.0,
        "subsample": 0.8,
        "random_seed": SEED,
        "verbose": 0
    },
    "HistGradientBoosting": {
        "max_iter": MAX_ROUNDS_HISTGB,
        "max_depth": 6,
        "learning_rate": 0.03,
        "max_leaf_nodes": 31,
        "min_samples_leaf": 20,
        "l2_regularization": 0.1,
        "early_stopping": True,
        "validation_fraction": INNER_VAL_FRAC,
        "n_iter_no_change": EARLY_STOP_ROUNDS,
        "random_state": SEED
    }
}


def run_experiment_2():
    import lightgbm as lgb
    from catboost import CatBoostRegressor

    print("=" * 74)
    print("  EXPERIMENT 2: ADVANCED GRADIENT BOOSTING (INNER EARLY-STOPPING)   ")
    print("=" * 74)

    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()
    feature_cols = get_leak_free_feature_list()

    exp2_results = {
        "experiment": "Exp2_Boosting",
        "seed": SEED,
        "inner_val_frac": INNER_VAL_FRAC,
        "early_stopping_rounds": EARLY_STOP_ROUNDS,
        "features": feature_cols,
        "models": {}
    }

    for model_name, config in CONFIGS.items():
        print(f"\n{'-'*60}")
        print(f"  Model: {model_name}")
        print(f"{'-'*60}")
        t_start = time.time()

        fold_metrics = []
        oof_records = []
        best_iters_per_fold = []

        for fold_data in folds_info["folds"]:
            f_num = fold_data["fold"]
            train_uids = set(fold_data["train_patient_uids"])
            val_uids   = set(fold_data["val_patient_uids"])
            val_seqns  = fold_data["val_seqn"]

            train_df = df[df["patient_uid"].isin(train_uids)].copy()
            val_df   = df[df["patient_uid"].isin(val_uids)].copy()

            X_tr_raw = train_df[feature_cols].values
            y_tr     = train_df["fib4_target"].values
            X_va_raw = val_df[feature_cols].values
            y_va     = val_df["fib4_target"].values

            # Fold-safe preprocessing: fit on OUTER TRAIN only
            imputer = SimpleImputer(strategy="median")
            scaler  = StandardScaler()
            X_tr_full = scaler.fit_transform(imputer.fit_transform(X_tr_raw))
            X_va      = scaler.transform(imputer.transform(X_va_raw))

            # Inner holdout split from training data only (for early stopping)
            X_tr_es, X_inner_val, y_tr_es, y_inner_val = train_test_split(
                X_tr_full, y_tr,
                test_size=INNER_VAL_FRAC,
                random_state=SEED + f_num
            )

            best_iter = None

            if model_name == "XGBoost_tuned":
                # early_stopping_rounds is already in config (constructor kwarg for XGBoost >= 2.0)
                model = xgb.XGBRegressor(**config)
                model.fit(
                    X_tr_es, y_tr_es,
                    eval_set=[(X_inner_val, y_inner_val)],
                    verbose=False
                )
                best_iter = model.best_iteration
                preds = model.predict(X_va)

            elif model_name == "LightGBM":
                model = lgb.LGBMRegressor(**config)
                model.fit(
                    X_tr_es, y_tr_es,
                    eval_set=[(X_inner_val, y_inner_val)],
                    callbacks=[lgb.early_stopping(EARLY_STOP_ROUNDS, verbose=False),
                               lgb.log_evaluation(period=-1)]
                )
                best_iter = model.best_iteration_
                preds = model.predict(X_va)

            elif model_name == "CatBoost":
                model = CatBoostRegressor(**config)
                model.fit(
                    X_tr_es, y_tr_es,
                    eval_set=(X_inner_val, y_inner_val),
                    early_stopping_rounds=EARLY_STOP_ROUNDS,
                    use_best_model=True,
                    verbose=0
                )
                best_iter = model.get_best_iteration()
                preds = model.predict(X_va)

            elif model_name == "HistGradientBoosting":
                model = HistGradientBoostingRegressor(**config)
                # HistGB early stopping uses internal validation_fraction from X_tr_full
                model.fit(X_tr_full, y_tr)
                best_iter = model.n_iter_
                preds = model.predict(X_va)

            fm = compute_regression_metrics(y_va, preds)
            fold_metrics.append(fm)
            best_iters_per_fold.append({"fold": f_num, "best_iter": int(best_iter) if best_iter else None})

            val_patient_uids = val_df["patient_uid"].tolist()
            for s, uid, y_t, y_p in zip(val_seqns, val_patient_uids, y_va, preds):
                oof_records.append({
                    "SEQN": s, "patient_uid": uid, "fold": f_num,
                    "y_true": float(y_t), "y_pred": float(y_p)
                })

            print(f"  Fold {f_num}  R2={fm['r2']:+.4f}  MAE={fm['mae']:.4f}  "
                  f"RMSE={fm['rmse']:.4f}  best_iter={best_iter}")

        agg = aggregate_fold_metrics(fold_metrics)
        pooled = compute_regression_metrics(
            [r["y_true"] for r in oof_records],
            [r["y_pred"] for r in oof_records]
        )
        elapsed = time.time() - t_start
        print(f"\n  {model_name} Aggregate -> R2={agg['r2_mean']:.4f}±{agg['r2_std']:.4f}  "
              f"MAE={agg['mae_mean']:.4f}±{agg['mae_std']:.4f}  "
              f"RMSE={agg['rmse_mean']:.4f}±{agg['rmse_std']:.4f}  [{elapsed:.1f}s]")

        oof_csv = os.path.join(EXP2_OUT_DIR, f"{model_name}_oof_predictions.csv")
        pd.DataFrame(oof_records).to_csv(oof_csv, index=False)

        exp2_results["models"][model_name] = {
            "config": {k: str(v) for k, v in config.items()},
            "fold_metrics": fold_metrics,
            "aggregate": agg,
            "pooled": pooled,
            "best_iters_per_fold": best_iters_per_fold,
            "elapsed_sec": round(elapsed, 2),
            "oof_csv": oof_csv
        }

    # Save master JSON
    json_path = os.path.join(EXP2_OUT_DIR, "exp2_results.json")
    with open(json_path, "w") as f:
        json.dump(exp2_results, f, indent=2)

    # Build comparison vs Exp0 XGBoost baseline
    orig_path = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\experiment_results.json"
    with open(orig_path) as f:
        orig = json.load(f)
    xgb_orig_r2 = orig["tabular_baselines"]["XGBoost"]["r2_mean"]

    md_path = os.path.join(EXP2_OUT_DIR, "exp2_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Experiment 2 Summary: Advanced Gradient Boosting Models\n\n")
        f.write(f"- **Early stopping holdout**: {int(INNER_VAL_FRAC*100)}% inner split (never the outer val fold)\n")
        f.write(f"- **Early stopping rounds**: {EARLY_STOP_ROUNDS}\n")
        f.write(f"- **Preprocessing**: Median imputation + StandardScaler fit on outer train fold only\n")
        f.write(f"- **Folds**: 5-fold patient-level (folds_v1.json, seed=42, N=6277)\n\n")
        f.write("| Model | R2 Mean | R2 Std | MAE Mean | RMSE Mean | Avg Best Iter | Delta R2 vs Exp0 XGB |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for m in ["XGBoost_tuned", "LightGBM", "CatBoost", "HistGradientBoosting"]:
            agg = exp2_results["models"][m]["aggregate"]
            iters = exp2_results["models"][m]["best_iters_per_fold"]
            avg_iter = np.mean([x["best_iter"] for x in iters if x["best_iter"] is not None])
            delta = agg['r2_mean'] - xgb_orig_r2
            f.write(f"| **{m}** | {agg['r2_mean']:.4f} | {agg['r2_std']:.4f} | "
                    f"{agg['mae_mean']:.4f} | {agg['rmse_mean']:.4f} | "
                    f"{avg_iter:.0f} | {delta:+.4f} |\n")
        f.write(f"\n> Exp0 reference (untuned XGBoost): R2={xgb_orig_r2:.4f}\n")

    print(f"\n{'='*74}")
    print(f"  EXPERIMENT 2 COMPLETE")
    print(f"  Results JSON : {json_path}")
    print(f"  Summary MD   : {md_path}")
    print(f"{'='*74}")
    return exp2_results


if __name__ == "__main__":
    run_experiment_2()
