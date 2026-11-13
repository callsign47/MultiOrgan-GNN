import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import copy
import json
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from pytorch_tabnet.tab_model import TabNetRegressor

from src.comparative.pipeline import FINAL_COHORT_PATH, get_leak_free_feature_list
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics, aggregate_fold_metrics
from src.comparative.deep_tabular import MLPRegressorPyTorch, FTTransformer

EXP3_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp3_deep_tabular"
CONFIG_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp3_deep_tabular"
os.makedirs(EXP3_OUT_DIR, exist_ok=True)
os.makedirs(CONFIG_OUT_DIR, exist_ok=True)

SEEDS = [42, 43, 44]
INNER_VAL_FRAC = 0.20
BATCH_SIZE = 64
MAX_EPOCHS = 100
PATIENCE = 15

CONFIGS = {
    "MLP_Retuned": {
        "hidden_dims": [128, 64, 32],
        "dropout": 0.2,
        "lr": 0.001,
        "weight_decay": 1e-4,
        "max_epochs": MAX_EPOCHS,
        "patience": PATIENCE
    },
    "FT_Transformer": {
        "embed_dim": 32,
        "num_heads": 4,
        "num_layers": 2,
        "ffn_dim": 64,
        "dropout": 0.1,
        "lr": 0.001,
        "weight_decay": 1e-4,
        "max_epochs": MAX_EPOCHS,
        "patience": PATIENCE
    },
    "TabNet": {
        "n_d": 16,
        "n_a": 16,
        "n_steps": 3,
        "gamma": 1.3,
        "lambda_sparse": 1e-4,
        "lr": 0.02,
        "max_epochs": MAX_EPOCHS,
        "patience": PATIENCE
    }
}

# Save configs
with open(os.path.join(CONFIG_OUT_DIR, "deep_tabular_configs.json"), "w") as f:
    json.dump(CONFIGS, f, indent=2)

def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def train_pytorch_model(model_cls, model_kwargs, X_tr, y_tr, X_val_inner, y_val_inner, X_test, device, lr=0.001, weight_decay=1e-4, max_epochs=100, patience=15, seed=42):
    set_seed(seed)
    model = model_cls(**model_kwargs).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max_epochs, eta_min=1e-5)
    criterion = nn.SmoothL1Loss()

    train_ds = TensorDataset(torch.tensor(X_tr, dtype=torch.float32), torch.tensor(y_tr, dtype=torch.float32))
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)

    val_x = torch.tensor(X_val_inner, dtype=torch.float32).to(device)
    val_y = torch.tensor(y_val_inner, dtype=torch.float32).to(device)
    test_x = torch.tensor(X_test, dtype=torch.float32).to(device)

    best_val_loss = float('inf')
    best_weights = None
    epochs_no_improve = 0

    for epoch in range(max_epochs):
        model.train()
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
        scheduler.step()

        model.eval()
        with torch.no_grad():
            val_out = model(val_x)
            val_loss = criterion(val_out, val_y).item()

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = copy.deepcopy(model.state_dict())
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                break

    model.load_state_dict(best_weights)
    model.eval()
    with torch.no_grad():
        test_preds = model(test_x).cpu().numpy()

    return test_preds, epoch + 1

def run_experiment_3():
    print("=" * 74)
    print("  EXPERIMENT 3: DEEP TABULAR BENCHMARK (MLP, FT-TRANSFORMER, TABNET) ")
    print("=" * 74)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device locked for execution: {device}")

    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()
    feature_cols = get_leak_free_feature_list()

    exp3_results = {
        "experiment": "Exp3_Deep_Tabular",
        "seeds": SEEDS,
        "device": str(device),
        "features": feature_cols,
        "models": {}
    }

    for model_name in ["MLP_Retuned", "FT_Transformer", "TabNet"]:
        print(f"\n{'-'*60}")
        print(f"  Model Family: {model_name}")
        print(f"{'-'*60}")
        t_model_start = time.time()

        seed_summaries = {}
        oof_by_seed = {s: [] for s in SEEDS}

        for s in SEEDS:
            print(f" -> Running Seed {s}...")
            fold_metrics = []

            for fold_data in folds_info["folds"]:
                f_num = fold_data["fold"]
                train_uids = set(fold_data["train_patient_uids"])
                val_uids = set(fold_data["val_patient_uids"])
                val_seqns = fold_data["val_seqn"]

                train_df = df[df["patient_uid"].isin(train_uids)].copy()
                val_df = df[df["patient_uid"].isin(val_uids)].copy()

                X_tr_raw = train_df[feature_cols].values
                y_tr = train_df["fib4_target"].values
                X_va_raw = val_df[feature_cols].values
                y_va = val_df["fib4_target"].values

                # Fold-safe preprocessing: fit strictly on OUTER TRAIN
                imputer = SimpleImputer(strategy="median")
                scaler = StandardScaler()
                X_tr_full = scaler.fit_transform(imputer.fit_transform(X_tr_raw))
                X_va = scaler.transform(imputer.transform(X_va_raw))

                # Inner validation split for early stopping
                X_tr_inner, X_val_inner, y_tr_inner, y_val_inner = train_test_split(
                    X_tr_full, y_tr,
                    test_size=INNER_VAL_FRAC,
                    random_state=s + f_num
                )

                if model_name == "MLP_Retuned":
                    cfg = CONFIGS["MLP_Retuned"]
                    preds, stop_epoch = train_pytorch_model(
                        MLPRegressorPyTorch,
                        {"in_features": len(feature_cols), "hidden_dims": cfg["hidden_dims"], "dropout": cfg["dropout"]},
                        X_tr_inner, y_tr_inner, X_val_inner, y_val_inner, X_va,
                        device, lr=cfg["lr"], weight_decay=cfg["weight_decay"],
                        max_epochs=cfg["max_epochs"], patience=cfg["patience"], seed=s
                    )

                elif model_name == "FT_Transformer":
                    cfg = CONFIGS["FT_Transformer"]
                    preds, stop_epoch = train_pytorch_model(
                        FTTransformer,
                        {"num_features": len(feature_cols), "embed_dim": cfg["embed_dim"], "num_heads": cfg["num_heads"], "num_layers": cfg["num_layers"], "ffn_dim": cfg["ffn_dim"], "dropout": cfg["dropout"]},
                        X_tr_inner, y_tr_inner, X_val_inner, y_val_inner, X_va,
                        device, lr=cfg["lr"], weight_decay=cfg["weight_decay"],
                        max_epochs=cfg["max_epochs"], patience=cfg["patience"], seed=s
                    )

                elif model_name == "TabNet":
                    cfg = CONFIGS["TabNet"]
                    tabnet = TabNetRegressor(
                        n_d=cfg["n_d"], n_a=cfg["n_a"], n_steps=cfg["n_steps"],
                        gamma=cfg["gamma"], lambda_sparse=cfg["lambda_sparse"],
                        optimizer_fn=torch.optim.AdamW,
                        optimizer_params=dict(lr=cfg["lr"]),
                        seed=s,
                        verbose=0
                    )
                    tabnet.fit(
                        X_tr_inner, y_tr_inner.reshape(-1, 1),
                        eval_set=[(X_val_inner, y_val_inner.reshape(-1, 1))],
                        eval_metric=['rmse'],
                        max_epochs=cfg["max_epochs"],
                        patience=cfg["patience"],
                        batch_size=BATCH_SIZE,
                        virtual_batch_size=16
                    )
                    preds = tabnet.predict(X_va).flatten()

                fm = compute_regression_metrics(y_va, preds)
                fold_metrics.append(fm)

                val_patient_uids = val_df["patient_uid"].tolist()
                for seqn, uid, y_t, y_p in zip(val_seqns, val_patient_uids, y_va, preds):
                    oof_by_seed[s].append({
                        "SEQN": seqn, "patient_uid": uid, "fold": f_num,
                        "y_true": float(y_t), "y_pred": float(y_p)
                    })

            agg = aggregate_fold_metrics(fold_metrics)
            pooled = compute_regression_metrics(
                [r["y_true"] for r in oof_by_seed[s]],
                [r["y_pred"] for r in oof_by_seed[s]]
            )
            seed_summaries[f"seed_{s}"] = {
                "fold_metrics": fold_metrics,
                "aggregate": agg,
                "pooled": pooled
            }
            print(f"    Seed {s} -> Fold Mean R²: {agg['r2_mean']:.4f}±{agg['r2_std']:.4f} | Pooled R²: {pooled['r2']:.4f} | MAE: {agg['mae_mean']:.4f} | RMSE: {agg['rmse_mean']:.4f}")

            # Save per-seed OOF
            seed_oof_csv = os.path.join(EXP3_OUT_DIR, f"{model_name}_seed{s}_oof_predictions.csv")
            pd.DataFrame(oof_by_seed[s]).to_csv(seed_oof_csv, index=False)

        # Compute cross-seed stability
        r2_means = [seed_summaries[f"seed_{s}"]["aggregate"]["r2_mean"] for s in SEEDS]
        mae_means = [seed_summaries[f"seed_{s}"]["aggregate"]["mae_mean"] for s in SEEDS]
        rmse_means = [seed_summaries[f"seed_{s}"]["aggregate"]["rmse_mean"] for s in SEEDS]

        # Compute seed-averaged ensemble OOF predictions
        ensemble_oof = []
        ref_records = oof_by_seed[SEEDS[0]]
        for i in range(len(ref_records)):
            seqn = ref_records[i]["SEQN"]
            uid = ref_records[i]["patient_uid"]
            f_num = ref_records[i]["fold"]
            y_t = ref_records[i]["y_true"]
            avg_p = float(np.mean([oof_by_seed[s][i]["y_pred"] for s in SEEDS]))
            ensemble_oof.append({
                "SEQN": seqn, "patient_uid": uid, "fold": f_num,
                "y_true": y_t, "y_pred": avg_p
            })

        ens_oof_csv = os.path.join(EXP3_OUT_DIR, f"{model_name}_ensemble_oof_predictions.csv")
        pd.DataFrame(ensemble_oof).to_csv(ens_oof_csv, index=False)
        ens_metrics = compute_regression_metrics([r["y_true"] for r in ensemble_oof], [r["y_pred"] for r in ensemble_oof])

        elapsed = time.time() - t_model_start
        cross_seed_summary = {
            "r2_cross_seed_mean": float(np.mean(r2_means)),
            "r2_cross_seed_std": float(np.std(r2_means)),
            "mae_cross_seed_mean": float(np.mean(mae_means)),
            "mae_cross_seed_std": float(np.std(mae_means)),
            "rmse_cross_seed_mean": float(np.mean(rmse_means)),
            "rmse_cross_seed_std": float(np.std(rmse_means)),
            "seed_averaged_ensemble_pooled": ens_metrics,
            "elapsed_sec": round(elapsed, 2)
        }

        exp3_results["models"][model_name] = {
            "seed_runs": seed_summaries,
            "cross_seed_summary": cross_seed_summary,
            "ensemble_oof_csv": ens_oof_csv
        }
        print(f"\n  {model_name} Cross-Seed Grand Mean -> R²: {cross_seed_summary['r2_cross_seed_mean']:.4f}±{cross_seed_summary['r2_cross_seed_std']:.4f} | Ensemble Pooled R²: {ens_metrics['r2']:.4f} [{elapsed:.1f}s]")

    # Save master JSON
    json_path = os.path.join(EXP3_OUT_DIR, "exp3_results.json")
    with open(json_path, "w") as f:
        json.dump(exp3_results, f, indent=2)

    # Markdown Summary
    md_path = os.path.join(EXP3_OUT_DIR, "exp3_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Experiment 3 Summary: Deep Tabular Models (Multi-Seed)\n\n")
        f.write(f"- **Seeds Evaluated**: {SEEDS}\n")
        f.write(f"- **Early Stopping**: 20% inner holdout of outer train fold (patience={PATIENCE})\n")
        f.write(f"- **Preprocessing**: Fold-safe SimpleImputer + StandardScaler on train fold only\n\n")
        f.write("| Model | Cross-Seed R² Mean ± SD | Seed Ensemble Pooled R² | Cross-Seed MAE | Cross-Seed RMSE | Delta R² vs Exp0 MLP (0.1320) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for m in ["MLP_Retuned", "FT_Transformer", "TabNet"]:
            css = exp3_results["models"][m]["cross_seed_summary"]
            f.write(f"| **{m}** | {css['r2_cross_seed_mean']:.4f} ± {css['r2_cross_seed_std']:.4f} | "
                    f"{css['seed_averaged_ensemble_pooled']['r2']:.4f} | "
                    f"{css['mae_cross_seed_mean']:.4f} | {css['rmse_cross_seed_mean']:.4f} | "
                    f"{css['r2_cross_seed_mean'] - 0.1320:+.4f} |\n")

    print(f"\n{'='*74}")
    print(f"  EXPERIMENT 3 COMPLETE!")
    print(f"  Summary JSON: {json_path}")
    print(f"  Summary MD:   {md_path}")
    print(f"{'='*74}")
    return exp3_results

if __name__ == "__main__":
    run_experiment_3()
