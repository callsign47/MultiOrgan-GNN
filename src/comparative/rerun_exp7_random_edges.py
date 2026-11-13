import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.data import HeteroData
from torch_geometric.loader import DataLoader as PyGDataLoader
import torch_geometric.nn as pyg_nn

from src.comparative.pipeline import FINAL_COHORT_PATH, preprocess_fold_graphs
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import (
    compute_regression_metrics, aggregate_fold_metrics, paired_bootstrap_comparison
)

GRAPH_PATH     = r"graphs/patient_graphs.pt"
EXP6_OUT_DIR   = r"results/comparative/exp6_ablations"
EXP4_HSGIN_CSV = r"results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv"
RESULTS_JSON   = os.path.join(EXP6_OUT_DIR, "exp7_graph_ablation_results.json")

SEED = 42
EPOCHS = 30
BATCH_SIZE = 64
LR = 0.001
WEIGHT_DECAY = 1e-4

def set_seed(s):
    np.random.seed(s)
    torch.manual_seed(s)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(s)

class HSGIN_RandomTopology(nn.Module):
    def __init__(self, in_dim_dict, edge_types, hidden_dim=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())
        self.edge_types = edge_types

        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim), nn.LayerNorm(hidden_dim),
                nn.ReLU(), nn.Dropout(dropout))

        self.conv_layers = nn.ModuleList()
        dim_dict = {ntype: hidden_dim for ntype in self.node_types}
        for _ in range(num_layers):
            conv_dict = {}
            for src, rel, dst in self.edge_types:
                if src in dim_dict and dst in dim_dict:
                    conv_dict[(src, rel, dst)] = pyg_nn.GATConv(
                        in_channels=dim_dict[src],
                        out_channels=hidden_dim // 2, heads=2,
                        concat=True, add_self_loops=False)
            self.conv_layers.append(pyg_nn.HeteroConv(conv_dict, aggr='mean'))

        readout_dim = hidden_dim * 3
        self.predict_head = nn.Sequential(
            nn.Linear(readout_dim, hidden_dim), nn.LayerNorm(hidden_dim),
            nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(), nn.Linear(hidden_dim // 2, 1))

    def forward(self, batch_graph):
        x_dict = batch_graph.x_dict
        edge_index_dict = batch_graph.edge_index_dict
        h_dict = {nt: self.encoder_dict[nt](x_dict[nt]) for nt in self.node_types}
        for conv in self.conv_layers:
            h_new = conv(h_dict, edge_index_dict)
            for nt in h_dict:
                if nt in h_new:
                    h_dict[nt] = nn.functional.relu(h_dict[nt] + h_new[nt])
        h_patient = h_dict["patient"]
        h_biomarker = h_dict["biomarker"]
        active = [h_dict[nt] for nt in ["liver", "kidney", "heart"] if nt in h_dict]
        h_organ_pool = torch.stack(active, dim=0).mean(dim=0) if active else torch.zeros_like(h_patient)
        h_repr = torch.cat([h_patient, h_organ_pool, h_biomarker], dim=-1)
        return self.predict_head(h_repr).squeeze(-1)

def train_model_fold(model_cls, model_kwargs, train_graphs, val_graphs, device, seed):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = PyGDataLoader(val_graphs,   batch_size=BATCH_SIZE, shuffle=False)

    model = model_cls(**model_kwargs).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    criterion = nn.SmoothL1Loss()

    best_r2 = -999.0
    best_preds, best_tgts = None, None

    for epoch in range(EPOCHS):
        model.train()
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            out = model(batch)
            loss = criterion(out, batch["patient"].y)
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

def build_random_graphs(original_graphs, random_edge_types):
    node_types = ['patient', 'liver', 'kidney', 'heart', 'biomarker']
    random_graphs = []
    for g in original_graphs:
        g_r = HeteroData()
        for nt in node_types:
            g_r[nt].x = g[nt].x.clone()
        g_r['patient'].y = g['patient'].y.clone()
        g_r.patient_uid = g.patient_uid
        for src, rel, dst in random_edge_types:
            g_r[src, rel, dst].edge_index = torch.tensor([[0], [0]], dtype=torch.long)
        random_graphs.append(g_r)
    return random_graphs

def main():
    print("=" * 74)
    print("  RERUN EXPERIMENT 7: GENUINE RANDOM EDGES STRUCTURAL NULL CONTROL")
    print("=" * 74)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Hardware locked: {device}")

    print("Loading pre-built patient graphs...")
    original_graphs = torch.load(GRAPH_PATH, weights_only=False)
    node_types = ['patient', 'liver', 'kidney', 'heart', 'biomarker']
    in_dim_dict = {nt: original_graphs[0][nt].x.shape[1] for nt in node_types}
    folds_info = generate_or_load_folds()

    # Define Erdős–Rényi random digraph on 5 nodes with E=14 matching edges
    all_possible_edges = [(u, 'interacts', v) for u in node_types for v in node_types if u != v]
    rng = np.random.default_rng(SEED)
    chosen_idx = rng.choice(len(all_possible_edges), size=14, replace=False)
    random_edge_types = [all_possible_edges[i] for i in chosen_idx]
    print(f"\nSampled 14 Random Edge Types (Erdos-Renyi G(5, 14), seed={SEED}):")
    for et in random_edge_types:
        print(f"  {et[0]} -> {et[2]}")

    print("\nConstructing randomized HeteroData graph collection...")
    rand_graphs = build_random_graphs(original_graphs, random_edge_types)
    print(f"Randomized graphs built: {len(rand_graphs)} patients, {len(rand_graphs[0].edge_types)} edge types each.")

    print("\nStarting 5-fold cross-validation with fresh model retraining from scratch...")
    t0 = time.time()
    fold_metrics, oof_records = [], []

    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        t_fold = time.time()
        train_uids = list(fd["train_patient_uids"])
        val_uids   = list(fd["val_patient_uids"])
        val_seqns  = fd["val_seqn"]

        tr_gs, va_gs = preprocess_fold_graphs(rand_graphs, train_uids, val_uids)
        preds, tgts = train_model_fold(
            HSGIN_RandomTopology,
            {"in_dim_dict": in_dim_dict, "edge_types": random_edge_types, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1},
            tr_gs, va_gs, device, seed=SEED + f_num - 1
        )
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
    print(f"\n  [RandomEdges] Pooled R2={pooled['r2']:.4f} | Mean R2={agg['r2_mean']:.4f}+-{agg['r2_std']:.4f} | RMSE={pooled['rmse']:.4f} [{el:.1f}s]")

    oof_csv = os.path.join(EXP6_OUT_DIR, "HSGIN_Variant_RandomEdges_oof.csv")
    pd.DataFrame(oof_records).to_csv(oof_csv, index=False)
    print(f"Saved OOF predictions: {oof_csv}")

    # Load Full HSGIN reference
    ref_df = pd.read_csv(EXP4_HSGIN_CSV)
    full_true = ref_df["y_true"].values
    full_preds = ref_df["y_pred"].values

    abl_preds = np.array([r["y_pred"] for r in oof_records])
    bt = paired_bootstrap_comparison(full_true, full_preds, abl_preds, n_bootstraps=2000, seed=SEED)

    print(f"\nPaired Bootstrap Comparison vs HSGIN_FULL_25:")
    print(f"  Delta R2 (Full - RandomEdges): {bt['observed_delta_r2']:+.4f} (95% CI: [{bt['ci_r2'][0]:+.4f}, {bt['ci_r2'][1]:+.4f}])")
    print(f"  Delta RMSE: {bt['observed_delta_rmse']:+.4f} (95% CI: [{bt['ci_rmse'][0]:+.4f}, {bt['ci_rmse'][1]:+.4f}])")
    print(f"  Delta MAE:  {bt['observed_delta_mae']:+.4f} (95% CI: [{bt['ci_mae'][0]:+.4f}, {bt['ci_mae'][1]:+.4f}])")

    # Update master JSON
    with open(RESULTS_JSON, "r") as f:
        master_results = json.load(f)

    master_results["variants"]["RandomEdges"] = {
        "description": "Structural null control: Erdős–Rényi random digraph on 5 organ/patient nodes with matching edge count E=14 sampled uniformly from 20 possible directed edge pairs",
        "random_edge_types": [f"{et[0]}->{et[2]}" for et in random_edge_types],
        "fold_metrics": fold_metrics,
        "aggregate": agg,
        "pooled": pooled,
        "oof_csv": oof_csv,
        "elapsed_sec": round(el, 2)
    }
    master_results["bootstrap_vs_hsgin_full"]["RandomEdges"] = bt

    with open(RESULTS_JSON, "w") as f:
        json.dump(master_results, f, indent=2)
    print(f"Successfully updated master results JSON: {RESULTS_JSON}")

if __name__ == "__main__":
    main()
