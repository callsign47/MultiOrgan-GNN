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
SEED_42_CSV    = os.path.join(EXP6_OUT_DIR, "HSGIN_Variant_RandomEdges_oof.csv")
RESULTS_JSON   = os.path.join(EXP6_OUT_DIR, "exp7_random_edges_multiseed_results.json")

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
        if fm["r2"] > best_r2:
            best_r2 = fm["r2"]
            best_preds = preds_list[:]
            best_tgts = tgts_list[:]

    return best_preds, best_tgts

def build_random_graphs(original_graphs, random_edge_types):
    random_graphs = []
    for g in original_graphs:
        g_r = HeteroData()
        g_r.patient_uid = g.patient_uid
        for nt in g.node_types:
            g_r[nt].x = g[nt].x.clone()
            if hasattr(g[nt], 'y') and g[nt].y is not None:
                g_r[nt].y = g[nt].y.clone()
        for src, rel, dst in random_edge_types:
            g_r[src, rel, dst].edge_index = torch.tensor([[0], [0]], dtype=torch.long)
        random_graphs.append(g_r)
    return random_graphs

def run_multiseed():
    print("=" * 74)
    print("  TECHNICAL AUDIT: RANDOM EDGES MULTI-SEED ENSEMBLE EVALUATION (ISSUE 3)")
    print("=" * 74)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Hardware locked: {device}")

    original_graphs = torch.load(GRAPH_PATH, weights_only=False)
    node_types = ['patient', 'liver', 'kidney', 'heart', 'biomarker']
    in_dim_dict = {nt: original_graphs[0][nt].x.shape[1] for nt in node_types}
    folds_info = generate_or_load_folds()

    all_possible_edges = [(u, 'interacts', v) for u in node_types for v in node_types if u != v]
    rng = np.random.default_rng(42)
    chosen_idx = rng.choice(len(all_possible_edges), size=14, replace=False)
    random_edge_types = [all_possible_edges[i] for i in chosen_idx]
    
    rand_graphs = build_random_graphs(original_graphs, random_edge_types)
    print(f"Randomized graphs built: {len(rand_graphs)} patients, {len(random_edge_types)} edge types.")

    seed_runs = {}
    
    # 1. Load Seed 42 from existing verified CSV
    if os.path.exists(SEED_42_CSV):
        print(f"\n[Seed 42] Loading existing verified OOF predictions from {SEED_42_CSV}...")
        df_42 = pd.read_csv(SEED_42_CSV)
        m_42 = compute_regression_metrics(df_42["y_true"].values, df_42["y_pred"].values)
        seed_runs[42] = {
            "pooled": m_42,
            "oof_df": df_42,
            "csv_path": SEED_42_CSV
        }
        print(f"  Seed 42 -> Pooled R2 = {m_42['r2']:.4f} | RMSE = {m_42['rmse']:.4f}")
    else:
        print(f"Error: {SEED_42_CSV} not found!")
        return

    # 2. Run Seed 43 and Seed 44
    for seed in [43, 44]:
        print(f"\n[Seed {seed}] Running 5-fold cross-validation on CUDA...")
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
                tr_gs, va_gs, device, seed=seed + f_num - 1
            )
            fm = compute_regression_metrics(tgts, preds)
            fold_metrics.append(fm)

            for i, (seqn, yt, yp) in enumerate(zip(val_seqns, tgts, preds)):
                oof_records.append({
                    "SEQN": seqn, "patient_uid": va_gs[i].patient_uid, "fold": f_num,
                    "y_true": float(yt), "y_pred": float(yp)
                })
            print(f"  Seed {seed} Fold {f_num} -> R2={fm['r2']:+.4f} [{time.time()-t_fold:.1f}s]")

        df_seed = pd.DataFrame(oof_records)
        seed_csv = os.path.join(EXP6_OUT_DIR, f"HSGIN_Variant_RandomEdges_seed{seed}_oof.csv")
        df_seed.to_csv(seed_csv, index=False)

        agg = aggregate_fold_metrics(fold_metrics)
        pooled = compute_regression_metrics(df_seed["y_true"].values, df_seed["y_pred"].values)
        seed_runs[seed] = {
            "fold_metrics": fold_metrics,
            "aggregate": agg,
            "pooled": pooled,
            "oof_df": df_seed,
            "csv_path": seed_csv
        }
        print(f"  Seed {seed} COMPLETE in {time.time()-t0:.1f}s -> Pooled R2 = {pooled['r2']:.4f} | RMSE = {pooled['rmse']:.4f}")

    # 3. Compute 3-Seed Multi-Seed Summary & Ensemble
    r2_seeds = [seed_runs[s]["pooled"]["r2"] for s in [42, 43, 44]]
    mean_seed_r2 = float(np.mean(r2_seeds))
    std_seed_r2 = float(np.std(r2_seeds))

    # Ensemble OOF predictions: merge on SEQN
    df_ens = seed_runs[42]["oof_df"][["SEQN", "patient_uid", "fold", "y_true", "y_pred"]].rename(columns={"y_pred": "pred_42"})
    df_ens = df_ens.merge(seed_runs[43]["oof_df"][["SEQN", "y_pred"]].rename(columns={"y_pred": "pred_43"}), on="SEQN")
    df_ens = df_ens.merge(seed_runs[44]["oof_df"][["SEQN", "y_pred"]].rename(columns={"y_pred": "pred_44"}), on="SEQN")
    df_ens["y_pred"] = df_ens[["pred_42", "pred_43", "pred_44"]].mean(axis=1)

    ens_csv = os.path.join(EXP6_OUT_DIR, "HSGIN_Variant_RandomEdges_ensemble_oof.csv")
    df_ens[["SEQN", "patient_uid", "fold", "y_true", "y_pred"]].to_csv(ens_csv, index=False)

    m_ens = compute_regression_metrics(df_ens["y_true"].values, df_ens["y_pred"].values)

    # 4. Load HSGIN Ensemble for Paired Bootstrap Comparison
    hsgin_ens_csv = r"results/comparative/exp4_gnn/HSGIN_ensemble_oof_predictions.csv"
    hsgin_seed42_csv = r"results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv"
    
    df_hsgin_ens = pd.read_csv(hsgin_ens_csv)
    df_hsgin_42 = pd.read_csv(hsgin_seed42_csv)

    # Align HSGIN vs RandomEdges by SEQN
    comp_ens = df_hsgin_ens[["SEQN", "y_true", "y_pred"]].rename(columns={"y_pred": "hsgin"}).merge(
        df_ens[["SEQN", "y_pred"]].rename(columns={"y_pred": "random"}), on="SEQN"
    )
    bootstrap_ens = paired_bootstrap_comparison(
        comp_ens["y_true"].values, comp_ens["hsgin"].values, comp_ens["random"].values, n_bootstraps=1000, seed=42
    )

    comp_42 = df_hsgin_42[["SEQN", "y_true", "y_pred"]].rename(columns={"y_pred": "hsgin"}).merge(
        seed_runs[42]["oof_df"][["SEQN", "y_pred"]].rename(columns={"y_pred": "random"}), on="SEQN"
    )
    bootstrap_42 = paired_bootstrap_comparison(
        comp_42["y_true"].values, comp_42["hsgin"].values, comp_42["random"].values, n_bootstraps=1000, seed=42
    )

    results = {
        "description": "RandomEdges Erdős–Rényi G(5, 14) multi-seed evaluation (Seeds 42, 43, 44)",
        "seeds": {
            "seed_42": seed_runs[42]["pooled"],
            "seed_43": seed_runs[43]["pooled"],
            "seed_44": seed_runs[44]["pooled"]
        },
        "multi_seed_mean_r2": round(mean_seed_r2, 4),
        "multi_seed_std_r2": round(std_seed_r2, 4),
        "ensemble_pooled": m_ens,
        "hsgin_comparison": {
            "single_seed_42": {
                "hsgin_r2": 0.4988,
                "random_edges_r2": seed_runs[42]["pooled"]["r2"],
                "delta_r2": round(0.4988 - seed_runs[42]["pooled"]["r2"], 4),
                "bootstrap": bootstrap_42
            },
            "multi_seed_mean": {
                "hsgin_mean_r2": 0.4953,
                "random_edges_mean_r2": round(mean_seed_r2, 4),
                "delta_r2": round(0.4953 - mean_seed_r2, 4)
            },
            "three_seed_ensemble": {
                "hsgin_ensemble_r2": 0.5114,
                "random_edges_ensemble_r2": round(m_ens["r2"], 4),
                "delta_r2": round(0.5114 - m_ens["r2"], 4),
                "bootstrap": bootstrap_ens
            }
        }
    }

    with open(RESULTS_JSON, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 74)
    print("  RANDOM EDGES MULTI-SEED AUDIT RESULTS:")
    print(f"  RandomEdges Seed 42 Pooled R2:       {seed_runs[42]['pooled']['r2']:.4f}")
    print(f"  RandomEdges Seed 43 Pooled R2:       {seed_runs[43]['pooled']['r2']:.4f}")
    print(f"  RandomEdges Seed 44 Pooled R2:       {seed_runs[44]['pooled']['r2']:.4f}")
    print(f"  RandomEdges 3-Seed Mean R2:          {mean_seed_r2:.4f} \u00b1 {std_seed_r2:.4f}")
    print(f"  RandomEdges 3-Seed Ensemble R2:      {m_ens['r2']:.4f}")
    print("  ---")
    print(f"  HSGIN vs RandomEdges (Seed 42):      \u0394 R2 = {results['hsgin_comparison']['single_seed_42']['delta_r2']:+.4f} (95% CI {bootstrap_42['ci_r2']})")
    print(f"  HSGIN vs RandomEdges (3-Seed Mean):  \u0394 R2 = {results['hsgin_comparison']['multi_seed_mean']['delta_r2']:+.4f}")
    print(f"  HSGIN vs RandomEdges (3-Seed Ens):   \u0394 R2 = {results['hsgin_comparison']['three_seed_ensemble']['delta_r2']:+.4f} (95% CI {bootstrap_ens['ci_r2']})")
    print("=" * 74)

if __name__ == "__main__":
    run_multiseed()
