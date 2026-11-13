import os, sys, json, time
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader
import torch_geometric.nn as pyg_nn

from src.comparative.pipeline import FINAL_COHORT_PATH, preprocess_fold_graphs
from src.comparative.models.hsgin import HSGIN, HeteroOrganConvBlock
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import (
    compute_regression_metrics, aggregate_fold_metrics, paired_bootstrap_comparison
)

GRAPH_PATH     = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
EXP6_OUT_DIR   = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp6_ablations"
CFG_OUT_DIR    = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp6_ablations"
EXP4_HSGIN_CSV = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp4_gnn\HSGIN_seed42_oof_predictions.csv"

os.makedirs(EXP6_OUT_DIR, exist_ok=True)
os.makedirs(CFG_OUT_DIR,  exist_ok=True)

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

# ── 1. NoCrossTalk: Star Topology (Patient-Organ only, removes 6 cross-talk edges)
class HSGIN_NoCrossTalk(nn.Module):
    STAR_EDGE_TYPES = [
        ('patient', 'pertains_to', 'liver'),
        ('liver', 'rev_pertains_to', 'patient'),
        ('patient', 'pertains_to', 'kidney'),
        ('kidney', 'rev_pertains_to', 'patient'),
        ('patient', 'pertains_to', 'heart'),
        ('heart', 'rev_pertains_to', 'patient'),
        ('patient', 'pertains_to', 'biomarker'),
        ('biomarker', 'rev_pertains_to', 'patient'),
    ]

    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim), nn.LayerNorm(hidden_dim),
                nn.ReLU(), nn.Dropout(dropout))

        self.conv_layers = nn.ModuleList()
        dim_dict = {ntype: hidden_dim for ntype in self.node_types}
        for _ in range(num_layers):
            conv_dict = {}
            for src, rel, dst in self.STAR_EDGE_TYPES:
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
        edge_index_dict = {k: v for k, v in batch_graph.edge_index_dict.items()
                           if k in set(self.STAR_EDGE_TYPES)}
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

# ── 2. FlatReadout: Flat mean pooling across all 5 node types
class HSGIN_FlatReadout(nn.Module):
    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim), nn.LayerNorm(hidden_dim),
                nn.ReLU(), nn.Dropout(dropout))

        self.conv_layers = nn.ModuleList()
        dim_dict = {ntype: hidden_dim for ntype in self.node_types}
        for _ in range(num_layers):
            self.conv_layers.append(HeteroOrganConvBlock(dim_dict, hidden_dim, heads=2))

        self.predict_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.LayerNorm(hidden_dim),
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
        all_embs = torch.stack([h_dict[nt] for nt in self.node_types], dim=0).mean(dim=0)
        return self.predict_head(all_embs).squeeze(-1)

# ── 3. RandomEdges: Structural Null Control (Permuted Edge Indices)
def randomize_graph_edges(graph_list, seed=42):
    rng = np.random.default_rng(seed)
    randomized = []
    for g in graph_list:
        g2 = g.clone()
        for et in g2.edge_types:
            ei = g2[et].edge_index
            E = ei.shape[1]
            n_src = g2[et[0]].x.shape[0]
            n_dst = g2[et[2]].x.shape[0]
            new_src = torch.from_numpy(rng.integers(0, n_src, size=E))
            new_dst = torch.from_numpy(rng.integers(0, n_dst, size=E))
            g2[et].edge_index = torch.stack([new_src, new_dst], dim=0).long()
        randomized.append(g2)
    return randomized

# ── 4. Homogeneous GNN: Standard GCN collapsing node and edge types
class HomogeneousGNN(nn.Module):
    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Linear(in_dim, hidden_dim)

        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            self.convs.append(pyg_nn.GCNConv(hidden_dim, hidden_dim, add_self_loops=True))

        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(hidden_dim)

        self.predict_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(), nn.Linear(hidden_dim // 2, 1))

    def forward(self, batch_graph):
        x_dict = batch_graph.x_dict
        h_dict = {nt: self.encoder_dict[nt](x_dict[nt]) for nt in self.node_types}
        h_all = torch.cat([h_dict[nt] for nt in self.node_types], dim=0)

        offsets = {}
        offset = 0
        for nt in self.node_types:
            offsets[nt] = offset
            offset += h_dict[nt].shape[0]

        edge_indices = []
        for src_type, rel, dst_type in batch_graph.edge_types:
            ei = batch_graph[src_type, rel, dst_type].edge_index
            src_off = offsets[src_type]
            dst_off = offsets[dst_type]
            edge_indices.append(ei + torch.tensor([[src_off], [dst_off]], device=ei.device))
        if edge_indices:
            edge_index = torch.cat(edge_indices, dim=1)
        else:
            edge_index = torch.zeros((2, 0), dtype=torch.long, device=h_all.device)

        h = h_all
        for conv in self.convs:
            h = conv(h, edge_index)
            h = torch.relu(h)
            h = self.dropout(h)
        h = self.norm(h)

        n_patient = h_dict["patient"].shape[0]
        h_patient = h[:n_patient]
        return self.predict_head(h_patient).squeeze(-1)


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


def run_variant_cv(graph_list, folds_info, model_cls, model_kwargs, device, label):
    print(f"\n--- Running 5-fold CV for Variant: {label} ---")
    t0 = time.time()
    fold_metrics, oof_records = [], []

    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        t_fold = time.time()
        train_uids = list(fd["train_patient_uids"])
        val_uids   = list(fd["val_patient_uids"])
        val_seqns  = fd["val_seqn"]

        tr_gs, va_gs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        preds, tgts = train_model_fold(model_cls, model_kwargs, tr_gs, va_gs, device, seed=SEED + f_num - 1)
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
    print("  EXPERIMENT 7: GRAPH ARCHITECTURE ABLATIONS")
    print("=" * 74)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Hardware locked: {device}")

    print("Loading pre-built patient graphs...")
    graph_list = torch.load(GRAPH_PATH, weights_only=False)
    in_dim_dict = {nt: graph_list[0][nt].x.shape[1] for nt in graph_list[0].node_types}
    folds_info = generate_or_load_folds()

    # Load Full HSGIN reference (from Exp4 Seed 42)
    ref_df = pd.read_csv(EXP4_HSGIN_CSV)
    full_true = ref_df["y_true"].values
    full_preds = ref_df["y_pred"].values
    full_pooled = compute_regression_metrics(full_true, full_preds)

    full_fold_metrics = []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        f_df = ref_df[ref_df["fold"] == f_num]
        full_fold_metrics.append(compute_regression_metrics(f_df["y_true"], f_df["y_pred"]))
    full_agg = aggregate_fold_metrics(full_fold_metrics)

    results = {
        "experiment": "Exp7_GraphArchitectureAblation",
        "device": str(device),
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "reference_hsgin_full": {
            "fold_metrics": full_fold_metrics,
            "aggregate": full_agg,
            "pooled": full_pooled,
            "oof_csv": EXP4_HSGIN_CSV
        },
        "variants": {},
        "bootstrap_vs_hsgin_full": {}
    }

    results_json = os.path.join(EXP6_OUT_DIR, "exp7_graph_ablation_results.json")

    variants = [
        ("NoCrossTalk", HSGIN_NoCrossTalk, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1},
         graph_list, "Star topology only; removes all 6 organ-to-organ cross-talk edges"),
        ("FlatReadout", HSGIN_FlatReadout, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1},
         graph_list, "Replaces organ-aware hierarchical readout with flat mean pooling across all nodes"),
        ("RandomEdges", HSGIN, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1},
         randomize_graph_edges(graph_list, seed=SEED), "Structural null control with randomized edge topology"),
        ("HomoGNN", HomogeneousGNN, {"in_dim_dict": in_dim_dict, "hidden_dim": 64, "num_layers": 2, "dropout": 0.1},
         graph_list, "Homogeneous GCN collapsing all node and relation types into uniform message passing")
    ]

    for vname, model_cls, model_kwargs, cur_graphs, desc in variants:
        oof_recs, fold_ms, agg, pooled, el = run_variant_cv(
            cur_graphs, folds_info, model_cls, model_kwargs, device, vname
        )
        oof_csv = os.path.join(EXP6_OUT_DIR, f"HSGIN_Variant_{vname}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        abl_preds = np.array([r["y_pred"] for r in oof_recs])
        bt = paired_bootstrap_comparison(full_true, full_preds, abl_preds, n_bootstraps=2000, seed=SEED)

        results["variants"][vname] = {
            "description": desc,
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv,
            "elapsed_sec": round(el, 2)
        }
        results["bootstrap_vs_hsgin_full"][vname] = bt

        # Save checkpoint
        with open(results_json, "w") as f:
            json.dump(results, f, indent=2)

        sig = "YES (Full > Variant)" if bt["a_significantly_better_r2"] else ("YES (Variant > Full)" if bt["b_significantly_better_r2"] else "NO")
        print(f"  >>> CHECKPOINT: {vname} saved | Delta R2={bt['observed_delta_r2']:+.4f} | 95% CI=[{bt['ci_r2'][0]:+.4f}, {bt['ci_r2'][1]:+.4f}] | Sig: {sig}")

    print("\n" + "=" * 74)
    print("  EXPERIMENT 7: ALL 4 GRAPH ARCHITECTURE VARIANTS COMPLETE!")
    print(f"  Master JSON saved: {results_json}")
    print("=" * 74)

if __name__ == "__main__":
    main()
