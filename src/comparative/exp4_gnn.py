import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import json
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader

from src.comparative.pipeline import (
    FINAL_COHORT_PATH,
    preprocess_fold_graphs
)
from src.comparative.models.hsgin import HSGIN
from src.comparative.models.baselines import ClassicalHGNN
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics, aggregate_fold_metrics

GRAPH_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
EXP4_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp4_gnn"
CONFIG_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp4_gnn"
os.makedirs(EXP4_OUT_DIR, exist_ok=True)
os.makedirs(CONFIG_OUT_DIR, exist_ok=True)

SEEDS = [42, 43, 44]
BATCH_SIZE = 64
LR = 0.001
WEIGHT_DECAY = 1e-4

GNN_CONFIGS = {
    "Classical_HGNN": {
        "hidden_dim": 64,
        "dropout": 0.1,
        "epochs": 40,
        "lr": LR,
        "weight_decay": WEIGHT_DECAY
    },
    "HSGIN": {
        "hidden_dim": 64,
        "num_layers": 2,
        "dropout": 0.1,
        "epochs": 50,
        "lr": LR,
        "weight_decay": WEIGHT_DECAY
    }
}

with open(os.path.join(CONFIG_OUT_DIR, "gnn_configs.json"), "w") as f:
    json.dump(GNN_CONFIGS, f, indent=2)

def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def train_gnn_model_fold(model_cls, model_kwargs, train_graphs, val_graphs, device, epochs, seed=42):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=BATCH_SIZE, shuffle=False)

    model = model_cls(**model_kwargs).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    criterion = nn.SmoothL1Loss()

    best_val_r2 = -999.0
    best_metrics = None
    best_val_preds = None
    best_val_targets = None

    for epoch in range(epochs):
        model.train()
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            out = model(batch)
            loss = criterion(out, batch['patient'].y)
            loss.backward()
            optimizer.step()

        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                out = model(batch)
                val_preds.extend(out.cpu().numpy().flatten())
                val_targets.extend(batch['patient'].y.cpu().numpy().flatten())

        metrics = compute_regression_metrics(val_targets, val_preds)
        if metrics['r2'] > best_val_r2 or epoch == 0:
            best_val_r2 = metrics['r2']
            best_metrics = metrics
            best_val_preds = val_preds
            best_val_targets = val_targets

    return best_metrics, best_val_preds, best_val_targets

def run_experiment_4():
    print("=" * 74)
    print("  EXPERIMENT 4: GRAPH NEURAL NETWORKS MULTI-SEED EVALUATION         ")
    print("=" * 74)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device locked for execution: {device}")

    print("Loading pre-built PyG HeteroData graphs...")
    graph_list = torch.load(GRAPH_PATH, weights_only=False)
    in_dim_dict = {ntype: graph_list[0][ntype].x.shape[1] for ntype in graph_list[0].node_types}
    print(f"Node Dimension Dict: {in_dim_dict}")

    folds_info = generate_or_load_folds()

    exp4_results = {
        "experiment": "Exp4_GNN_MultiSeed",
        "seeds": SEEDS,
        "device": str(device),
        "node_dims": in_dim_dict,
        "models": {}
    }

    models_to_run = [
        ("Classical_HGNN", ClassicalHGNN, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "dropout": 0.1}, 40),
        ("HSGIN", HSGIN, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1}, 50)
    ]

    for model_name, model_cls, model_kwargs, epochs in models_to_run:
        print(f"\n{'-'*60}")
        print(f"  Model Architecture: {model_name}")
        print(f"{'-'*60}")
        t_start = time.time()

        seed_summaries = {}
        oof_by_seed = {s: [] for s in SEEDS}

        for s in SEEDS:
            print(f" -> Running Seed {s}...")
            fold_metrics = []

            for fold_data in folds_info["folds"]:
                f_num = fold_data["fold"]
                train_uids = fold_data["train_patient_uids"]
                val_uids = fold_data["val_patient_uids"]
                val_seqns = fold_data["val_seqn"]

                tr_graphs, va_graphs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
                fold_seed = s + f_num - 1
                fm, preds, targets = train_gnn_model_fold(
                    model_cls, model_kwargs, tr_graphs, va_graphs, device, epochs, seed=fold_seed
                )
                fold_metrics.append(fm)

                for seqn, uid, y_t, y_p in zip(val_seqns, val_uids, targets, preds):
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
            seed_oof_csv = os.path.join(EXP4_OUT_DIR, f"{model_name}_seed{s}_oof_predictions.csv")
            pd.DataFrame(oof_by_seed[s]).to_csv(seed_oof_csv, index=False)

        # Cross-seed stability
        r2_means = [seed_summaries[f"seed_{s}"]["aggregate"]["r2_mean"] for s in SEEDS]
        mae_means = [seed_summaries[f"seed_{s}"]["aggregate"]["mae_mean"] for s in SEEDS]
        rmse_means = [seed_summaries[f"seed_{s}"]["aggregate"]["rmse_mean"] for s in SEEDS]

        # Seed ensemble
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

        ens_oof_csv = os.path.join(EXP4_OUT_DIR, f"{model_name}_ensemble_oof_predictions.csv")
        pd.DataFrame(ensemble_oof).to_csv(ens_oof_csv, index=False)
        ens_metrics = compute_regression_metrics([r["y_true"] for r in ensemble_oof], [r["y_pred"] for r in ensemble_oof])

        elapsed = time.time() - t_start
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

        exp4_results["models"][model_name] = {
            "seed_runs": seed_summaries,
            "cross_seed_summary": cross_seed_summary,
            "ensemble_oof_csv": ens_oof_csv
        }
        print(f"\n  {model_name} Cross-Seed Grand Mean -> R²: {cross_seed_summary['r2_cross_seed_mean']:.4f}±{cross_seed_summary['r2_cross_seed_std']:.4f} | Ensemble Pooled R²: {ens_metrics['r2']:.4f} [{elapsed:.1f}s]")

    # Save master JSON
    json_path = os.path.join(EXP4_OUT_DIR, "exp4_results.json")
    with open(json_path, "w") as f:
        json.dump(exp4_results, f, indent=2)

    # Markdown Summary
    md_path = os.path.join(EXP4_OUT_DIR, "exp4_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Experiment 4 Summary: Graph Neural Networks Multi-Seed Evaluation\n\n")
        f.write(f"- **Seeds Evaluated**: {SEEDS}\n")
        f.write(f"- **Folds**: 5-fold patient-level (folds_v1.json, N=6277)\n")
        f.write(f"- **Preprocessing**: Fold-safe node-level imputation + standardization strictly on train graphs\n\n")
        f.write("| Model | Cross-Seed R² Mean ± SD | Seed Ensemble Pooled R² | Cross-Seed MAE | Cross-Seed RMSE | Delta R² vs Seed 42 |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for m in ["Classical_HGNN", "HSGIN"]:
            css = exp4_results["models"][m]["cross_seed_summary"]
            s42_r2 = exp4_results["models"][m]["seed_runs"]["seed_42"]["aggregate"]["r2_mean"]
            f.write(f"| **{m}** | {css['r2_cross_seed_mean']:.4f} ± {css['r2_cross_seed_std']:.4f} | "
                    f"{css['seed_averaged_ensemble_pooled']['r2']:.4f} | "
                    f"{css['mae_cross_seed_mean']:.4f} | {css['rmse_cross_seed_mean']:.4f} | "
                    f"{css['r2_cross_seed_mean'] - s42_r2:+.4f} |\n")

    print(f"\n{'='*74}")
    print(f"  EXPERIMENT 4 COMPLETE!")
    print(f"  Summary JSON: {json_path}")
    print(f"  Summary MD:   {md_path}")
    print(f"{'='*74}")
    return exp4_results

if __name__ == "__main__":
    run_experiment_4()
