import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader

from src.comparative.pipeline import FINAL_COHORT_PATH, FEATURE_DOMAINS, preprocess_fold_graphs
from src.comparative.models.hsgin import HSGIN
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import (
    compute_regression_metrics, aggregate_fold_metrics, paired_bootstrap_comparison
)

GRAPH_PATH   = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
EXP6_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp6_ablations"
CFG_OUT_DIR  = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp6_ablations"
EXP4_HSGIN_CSV = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp4_gnn\HSGIN_seed42_oof_predictions.csv"

os.makedirs(EXP6_OUT_DIR, exist_ok=True)
os.makedirs(CFG_OUT_DIR,  exist_ok=True)

SEED = 42
EPOCHS = 30
BATCH_SIZE = 64
LR = 0.001
WEIGHT_DECAY = 1e-4

DOMAIN_TO_NODE = {
    "Demographics": "patient",
    "Liver": "liver",
    "Kidney": "kidney",
    "Heart": "heart",
    "Biomarker": "biomarker"
}

def set_seed(s):
    np.random.seed(s)
    torch.manual_seed(s)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(s)

def train_hsgin_fold(train_graphs, val_graphs, in_dim_dict, device, seed):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = PyGDataLoader(val_graphs,   batch_size=BATCH_SIZE, shuffle=False)

    model = HSGIN(in_dim_dict=in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    criterion = nn.SmoothL1Loss()

    best_r2 = -999.0
    best_preds, best_tgts = None, None

    for epoch in range(EPOCHS):
        model.train()
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            loss = criterion(model(batch), batch["patient"].y)
            loss.backward()
            optimizer.step()

        model.eval()
        preds_list, tgts_list = [], []
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                preds_list.extend(model(batch).cpu().numpy().flatten())
                tgts_list.extend(batch["patient"].y.cpu().numpy().flatten())

        fm = compute_regression_metrics(tgts_list, preds_list)
        if fm["r2"] > best_r2 or epoch == 0:
            best_r2 = fm["r2"]
            best_preds = preds_list[:]
            best_tgts = tgts_list[:]

    return best_preds, best_tgts

def apply_node_mask(graphs, masked_nodes):
    """Zero out specified node features in-place."""
    for g in graphs:
        for nt in masked_nodes:
            if nt in g.node_types:
                g[nt].x.zero_()

def run_ablation_cv(graph_list, folds_info, in_dim_dict, device, masked_nodes, label):
    print(f"\n--- Running 5-fold CV for {label} (Masking: {masked_nodes}) ---")
    t0 = time.time()
    fold_metrics, oof_records = [], []

    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        t_fold = time.time()
        train_uids = list(fd["train_patient_uids"])
        val_uids   = list(fd["val_patient_uids"])
        val_seqns  = fd["val_seqn"]

        tr_gs, va_gs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        if masked_nodes:
            apply_node_mask(tr_gs, masked_nodes)
            apply_node_mask(va_gs, masked_nodes)

        preds, tgts = train_hsgin_fold(tr_gs, va_gs, in_dim_dict, device, seed=SEED + f_num - 1)
        fm = compute_regression_metrics(tgts, preds)
        fold_metrics.append(fm)

        for i, (seqn, yt, yp) in enumerate(zip(val_seqns, tgts, preds)):
            oof_records.append({
                "SEQN": seqn, "patient_uid": va_gs[i].patient_uid, "fold": f_num,
                "y_true": float(yt), "y_pred": float(yp)
            })
        print(f"  Fold {f_num} -> R2={fm['r2']:+.4f} | MAE={fm['mae']:.4f} | RMSE={fm['rmse']:.4f} [{time.time()-t_fold:.1f}s]")

    agg = aggregate_fold_metrics(fold_metrics)
    pooled = compute_regression_metrics(
        [r["y_true"] for r in oof_records], [r["y_pred"] for r in oof_records]
    )
    el = time.time() - t0
    print(f"  [{label}] Summary -> Pooled R2={pooled['r2']:.4f} | Mean R2={agg['r2_mean']:.4f}+-{agg['r2_std']:.4f} | RMSE={pooled['rmse']:.4f} [{el:.1f}s]")
    return oof_records, fold_metrics, agg, pooled, el

def main():
    print("=" * 74)
    print("  EXPERIMENT 6b: HSGIN FEATURE-DOMAIN ABLATION")
    print("=" * 74)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Hardware locked: {device}")

    print("Loading pre-built patient graphs...")
    graph_list = torch.load(GRAPH_PATH, weights_only=False)
    in_dim_dict = {nt: graph_list[0][nt].x.shape[1] for nt in graph_list[0].node_types}
    folds_info = generate_or_load_folds()

    # 1. Full reference (from Exp4 Seed 42)
    print("\nLoading Full 25-Feature Reference from Exp4 Seed 42...")
    ref_df = pd.read_csv(EXP4_HSGIN_CSV)
    full_csv = os.path.join(EXP6_OUT_DIR, "HSGIN_FULL_25_oof.csv")
    ref_df.to_csv(full_csv, index=False)
    full_true = ref_df["y_true"].values
    full_preds = ref_df["y_pred"].values
    full_pooled = compute_regression_metrics(full_true, full_preds)

    # Compute fold metrics for full
    full_fold_metrics = []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        f_df = ref_df[ref_df["fold"] == f_num]
        full_fold_metrics.append(compute_regression_metrics(f_df["y_true"], f_df["y_pred"]))
    full_agg = aggregate_fold_metrics(full_fold_metrics)
    print(f"  HSGIN_FULL_25 -> Pooled R2={full_pooled['r2']:.4f} | Mean R2={full_agg['r2_mean']:.4f}+-{full_agg['r2_std']:.4f} | RMSE={full_pooled['rmse']:.4f}")

    results = {
        "experiment": "Exp6b_HSGIN_FeatureDomainAblation",
        "device": str(device),
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "ablations": {
            "FULL_25": {
                "masked_nodes": [],
                "fold_metrics": full_fold_metrics,
                "aggregate": full_agg,
                "pooled": full_pooled,
                "oof_csv": full_csv,
                "elapsed_sec": 0.0
            }
        },
        "bootstrap_vs_full": {}
    }

    results_json = os.path.join(EXP6_OUT_DIR, "exp6_hsgin_results.json")
    with open(results_json, "w") as f:
        json.dump(results, f, indent=2)

    # 2. Leave-One-Domain-Out Ablations
    # Domain order: Liver (expected largest), Biomarker, Kidney, Heart, Demographics
    domain_order = ["Liver", "Biomarker", "Kidney", "Heart", "Demographics"]

    for dn in domain_order:
        node_type = DOMAIN_TO_NODE[dn]
        abl_name = f"LOO_{dn}"
        oof_recs, fold_ms, agg, pooled, el = run_ablation_cv(
            graph_list, folds_info, in_dim_dict, device, [node_type], abl_name
        )
        oof_csv = os.path.join(EXP6_OUT_DIR, f"HSGIN_{abl_name}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        abl_preds = np.array([r["y_pred"] for r in oof_recs])
        bt = paired_bootstrap_comparison(full_true, full_preds, abl_preds, n_bootstraps=2000, seed=SEED)

        results["ablations"][abl_name] = {
            "masked_nodes": [node_type],
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv,
            "elapsed_sec": round(el, 2)
        }
        results["bootstrap_vs_full"][abl_name] = bt

        # Save checkpoint
        with open(results_json, "w") as f:
            json.dump(results, f, indent=2)

        sig = "YES" if bt["a_significantly_better_r2"] else "NO"
        print(f"  >>> CHECKPOINT: {abl_name} saved | Delta R2={bt['observed_delta_r2']:+.4f} | 95% CI=[{bt['ci_r2'][0]:+.4f}, {bt['ci_r2'][1]:+.4f}] | Sig: {sig}")

    print("\n" + "=" * 74)
    print("  ALL 5 HSGIN LEAVE-ONE-OUT ABLATIONS COMPLETE!")
    print(f"  Master JSON saved: {results_json}")
    print("=" * 74)

if __name__ == "__main__":
    main()
