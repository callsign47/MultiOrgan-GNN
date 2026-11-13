"""
Experiment 1: Linear & Tree-Ensemble Models with Inner-CV Hyperparameter Tuning
Models: Ridge, ElasticNet, RandomForest, ExtraTrees
- Fold-safe preprocessing: imputer + scaler fit strictly on train portion of each outer fold
- Inner CV (3-fold) for hyperparameter selection on training data only
- OOF predictions saved keyed by SEQN
"""
import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from src.comparative.pipeline import FINAL_COHORT_PATH, get_leak_free_feature_list
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics, aggregate_fold_metrics

EXP1_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp1_linear_trees"
os.makedirs(EXP1_OUT_DIR, exist_ok=True)

SEED = 42
INNER_CV_FOLDS = 3

# ── Hyperparameter grids ───────────────────────────────────────────────────────
PARAM_GRIDS = {
    "Ridge": {
        "alpha": [0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
    },
    "ElasticNet": {
        "alpha": [0.001, 0.01, 0.05, 0.1, 0.5, 1.0],
        "l1_ratio": [0.1, 0.25, 0.5, 0.75, 0.9]
    },
    "RandomForest": {
        "n_estimators": [200],
        "max_depth": [6, 10, 15, None],
        "min_samples_leaf": [1, 2, 5],
        "max_features": [0.5, 0.75, "sqrt"]
    },
    "ExtraTrees": {
        "n_estimators": [200],
        "max_depth": [6, 10, 15, None],
        "min_samples_leaf": [1, 2, 5],
        "max_features": [0.5, 0.75, "sqrt"]
    }
}

ESTIMATORS = {
    "Ridge":        Ridge(random_state=None),
    "ElasticNet":   ElasticNet(max_iter=5000, random_state=SEED),
    "RandomForest": RandomForestRegressor(random_state=SEED, n_jobs=-1),
    "ExtraTrees":   ExtraTreesRegressor(random_state=SEED, n_jobs=-1),
}


def run_experiment_1():
    print("=" * 74)
    print("  EXPERIMENT 1: LINEAR & TREE ENSEMBLE MODELS (INNER-CV TUNED)      ")
    print("=" * 74)

    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()
    feature_cols = get_leak_free_feature_list()

    exp1_results = {
        "experiment": "Exp1_Linear_Trees",
        "seed": SEED,
        "inner_cv_folds": INNER_CV_FOLDS,
        "features": feature_cols,
        "models": {}
    }

    for model_name, estimator in ESTIMATORS.items():
        print(f"\n{'-'*60}")
        print(f"  Model: {model_name}")
        print(f"{'-'*60}")
        t_start = time.time()

        fold_metrics = []
        oof_records = []
        best_params_per_fold = []

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

            # Fold-safe: fit preprocessing on TRAIN only
            imputer = SimpleImputer(strategy="median")
            scaler  = StandardScaler()
            X_tr = scaler.fit_transform(imputer.fit_transform(X_tr_raw))
            X_va = scaler.transform(imputer.transform(X_va_raw))

            # Inner-CV grid search on TRAINING data only
            inner_cv = KFold(n_splits=INNER_CV_FOLDS, shuffle=True, random_state=SEED)
            gs = GridSearchCV(
                estimator=estimator,
                param_grid=PARAM_GRIDS[model_name],
                cv=inner_cv,
                scoring="r2",
                n_jobs=-1,
                refit=True
            )
            gs.fit(X_tr, y_tr)
            best_params = gs.best_params_
            best_estimator = gs.best_estimator_

            preds = best_estimator.predict(X_va)
            fm = compute_regression_metrics(y_va, preds)
            fold_metrics.append(fm)
            best_params_per_fold.append({"fold": f_num, "best_params": best_params})

            val_patient_uids = val_df["patient_uid"].tolist()
            for s, uid, y_t, y_p in zip(val_seqns, val_patient_uids, y_va, preds):
                oof_records.append({
                    "SEQN": s, "patient_uid": uid, "fold": f_num,
                    "y_true": float(y_t), "y_pred": float(y_p)
                })

            print(f"  Fold {f_num}  R2={fm['r2']:+.4f}  MAE={fm['mae']:.4f}  RMSE={fm['rmse']:.4f}  best={best_params}")

        agg = aggregate_fold_metrics(fold_metrics)
        oof_all_true  = [r["y_true"] for r in oof_records]
        oof_all_pred  = [r["y_pred"] for r in oof_records]
        pooled = compute_regression_metrics(oof_all_true, oof_all_pred)

        elapsed = time.time() - t_start
        print(f"\n  {model_name} Aggregate -> R2={agg['r2_mean']:.4f}±{agg['r2_std']:.4f}  "
              f"MAE={agg['mae_mean']:.4f}±{agg['mae_std']:.4f}  "
              f"RMSE={agg['rmse_mean']:.4f}±{agg['rmse_std']:.4f}  [{elapsed:.1f}s]")

        # Save OOF CSV
        oof_csv = os.path.join(EXP1_OUT_DIR, f"{model_name}_oof_predictions.csv")
        pd.DataFrame(oof_records).to_csv(oof_csv, index=False)

        exp1_results["models"][model_name] = {
            "fold_metrics": fold_metrics,
            "aggregate":    agg,
            "pooled":       pooled,
            "best_params_per_fold": best_params_per_fold,
            "elapsed_sec":  round(elapsed, 2),
            "oof_csv":      oof_csv
        }

    # Save master JSON
    json_path = os.path.join(EXP1_OUT_DIR, "exp1_results.json")
    with open(json_path, "w") as f:
        json.dump(exp1_results, f, indent=2)

    # Build comparison vs Exp0 baselines
    orig_path = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\experiment_results.json"
    with open(orig_path) as f:
        orig = json.load(f)
    baseline_r2 = {
        "Ridge_Regression": orig["tabular_baselines"]["Ridge_Regression"]["r2_mean"],
        "Random_Forest":    orig["tabular_baselines"]["Random_Forest"]["r2_mean"],
        "XGBoost":          orig["tabular_baselines"]["XGBoost"]["r2_mean"],
    }

    md_path = os.path.join(EXP1_OUT_DIR, "exp1_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Experiment 1 Summary: Linear & Tree Models\n\n")
        f.write(f"- **Inner CV**: {INNER_CV_FOLDS}-fold GridSearchCV on training data only\n")
        f.write(f"- **Preprocessing**: Median imputation + StandardScaler fit on train fold only\n")
        f.write(f"- **Folds**: 5-fold patient-level (folds_v1.json, seed=42, N=6277)\n\n")
        f.write("| Model | R2 Mean | R2 Std | MAE Mean | MAE Std | RMSE Mean | RMSE Std | Delta R2 vs Exp0 |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        # Exp0 baselines for Ridge and RF (no ElasticNet/ExtraTrees in orig)
        for m in ["Ridge","ElasticNet","RandomForest","ExtraTrees"]:
            agg = exp1_results["models"][m]["aggregate"]
            orig_key = {"Ridge": "Ridge_Regression", "RandomForest": "Random_Forest"}.get(m)
            delta = f"{agg['r2_mean'] - baseline_r2[orig_key]:+.4f}" if orig_key else "N/A (new)"
            f.write(f"| **{m}** | {agg['r2_mean']:.4f} | {agg['r2_std']:.4f} | "
                    f"{agg['mae_mean']:.4f} | {agg['mae_std']:.4f} | "
                    f"{agg['rmse_mean']:.4f} | {agg['rmse_std']:.4f} | {delta} |\n")
        f.write(f"\n> Exp0 reference baselines (untuned): Ridge R2={baseline_r2['Ridge_Regression']:.4f}, "
                f"RF R2={baseline_r2['Random_Forest']:.4f}\n")

    print(f"\n{'='*74}")
    print(f"  EXPERIMENT 1 COMPLETE")
    print(f"  Results JSON : {json_path}")
    print(f"  Summary MD   : {md_path}")
    print(f"{'='*74}")
    return exp1_results


if __name__ == "__main__":
    run_experiment_1()
