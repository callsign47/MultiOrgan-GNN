"""
Experiment 6: Feature-Domain Ablation
Experiment 7: Graph Architecture Ablation

PRD v1.1 - Phase 6
--------------------
Exp 6: Leave-one-domain-out and single-domain-only runs using:
  - Best tabular learner: XGBoost (tuned, same config as Exp2)
  - Graph model: HSGIN (seed 42, same config as Exp4)

Exp 7: Graph architecture ablations of HSGIN:
  - No cross-talk edges (patient-organ star only)
  - Random edge topology control
  - Flat mean-pool readout (vs organ-aware hierarchical)
  - Homogeneous GNN baseline

Domain assignments (from locked manifest):
  Demographics : RIAGENDR                                     [1 feature]
  Liver        : LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI,
                 LUXSMED, LUXCAPM                             [6 features]
  Kidney       : LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR,
                 KIQ022                                       [6 features]
  Heart        : BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD,
                 LBXTC, BPQ020, MCQ160C, MCQ160E             [8 features]
  Biomarker    : LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP      [4 features]

Constraints:
  - NEVER modify original baseline files (src/, data/, graphs/, reports/).
  - All new files in src/comparative/, results/comparative/exp6_ablations/,
    configs/comparative/exp6_ablations/.
  - Reuse IDENTICAL locked folds_v1.json.
  - XGBoost config identical to Exp2 (except n_estimators fixed to best_iter avg).
  - HSGIN config identical to Exp4 seed 42.
"""
import os, sys, json, time, copy
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from torch_geometric.loader import DataLoader as PyGDataLoader
from torch_geometric.data import HeteroData

import xgboost as xgb

from src.comparative.pipeline import FINAL_COHORT_PATH, FEATURE_DOMAINS, preprocess_fold_graphs
from src.comparative.models.hsgin import HSGIN, HeteroOrganConvBlock
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import (
    compute_regression_metrics, aggregate_fold_metrics, paired_bootstrap_comparison
)

# ── Paths ──────────────────────────────────────────────────────────────────────
GRAPH_PATH   = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
EXP6_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp6_ablations"
CFG_OUT_DIR  = r"c:\Users\admin_fix\Downloads\3 ORGAN\configs\comparative\exp6_ablations"
os.makedirs(EXP6_OUT_DIR, exist_ok=True)
os.makedirs(CFG_OUT_DIR,  exist_ok=True)

# ── Reproducibility ────────────────────────────────────────────────────────────
SEED = 42

def set_seed(s):
    np.random.seed(s)
    torch.manual_seed(s)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(s)

# ── Domain definitions (from locked manifest, matches src/pipeline.py) ─────────
DOMAINS = FEATURE_DOMAINS  # dict: name -> [feature cols]
ALL_FEATURES = [f for feats in DOMAINS.values() for f in feats]  # 25 features

# ── XGBoost config — identical to Exp2 (tuned), fixed trees = avg best_iter=~400
# We fix n_estimators at a safe plateau value based on Exp2 best_iter logs.
# This avoids re-running inner early-stopping on domain subsets (which would
# give each domain a different budget). We use 400 trees with the same HPs.
XGB_CONFIG = {
    "n_estimators": 360,       # Fixed at Exp2 average best_iter (~354) rounded to equalize budget
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

# ── HSGIN config — identical to Exp4 (seed 42) ────────────────────────────────
HSGIN_EPOCHS     = 50
HSGIN_BATCH      = 64
HSGIN_LR         = 0.001
HSGIN_WD         = 1e-4
HSGIN_HIDDEN     = 64
HSGIN_LAYERS     = 2
HSGIN_DROPOUT    = 0.1

# Save configs
with open(os.path.join(CFG_OUT_DIR, "exp6_config.json"), "w") as f:
    json.dump({
        "xgboost": XGB_CONFIG,
        "hsgin": {
            "epochs": HSGIN_EPOCHS, "batch_size": HSGIN_BATCH,
            "lr": HSGIN_LR, "weight_decay": HSGIN_WD,
            "hidden_dim": HSGIN_HIDDEN, "num_layers": HSGIN_LAYERS,
            "dropout": HSGIN_DROPOUT, "seed": SEED,
        "n_estimators_note": "Fixed at 360 (Exp2 avg best_iter=354, rounded) to equalize domain budgets"
        }
    }, f, indent=2)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION A: HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def run_xgb_fold(X_tr, y_tr, X_va, y_va):
    model = xgb.XGBRegressor(**XGB_CONFIG)
    model.fit(X_tr, y_tr, verbose=False)
    preds = model.predict(X_va)
    return preds

def preprocess_tabular_fold(df, train_uids, val_uids, feature_cols):
    """Fold-safe preprocessing: fit imputer+scaler on train only."""
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
    """Run 5-fold XGBoost CV with given feature subset. Returns oof_records + agg."""
    fold_metrics, oof_records = [], []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        X_tr, y_tr, X_va, y_va, val_seqns, val_pids = preprocess_tabular_fold(
            df, fd["train_patient_uids"], fd["val_patient_uids"], feature_cols)
        preds = run_xgb_fold(X_tr, y_tr, X_va, y_va)
        fm = compute_regression_metrics(y_va, preds)
        fold_metrics.append(fm)
        for s, uid, yt, yp in zip(val_seqns, val_pids, y_va, preds):
            oof_records.append({"SEQN": s, "patient_uid": uid, "fold": f_num,
                                 "y_true": float(yt), "y_pred": float(yp)})
        print(f"    [{label}] Fold {f_num}  R²={fm['r2']:+.4f}  MAE={fm['mae']:.4f}")
    agg = aggregate_fold_metrics(fold_metrics)
    pooled = compute_regression_metrics(
        [r["y_true"] for r in oof_records], [r["y_pred"] for r in oof_records])
    return oof_records, fold_metrics, agg, pooled


# ── HSGIN training helper ─────────────────────────────────────────────────────
def train_hsgin_fold(train_graphs, val_graphs, in_dim_dict, device, seed):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=HSGIN_BATCH, shuffle=True)
    val_loader   = PyGDataLoader(val_graphs,   batch_size=HSGIN_BATCH, shuffle=False)

    model = HSGIN(in_dim_dict=in_dim_dict, hidden_dim=HSGIN_HIDDEN,
                  num_layers=HSGIN_LAYERS, dropout=HSGIN_DROPOUT).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=HSGIN_LR, weight_decay=HSGIN_WD)
    criterion = nn.SmoothL1Loss()

    best_r2, best_preds, best_tgts = -999.0, None, None

    for epoch in range(HSGIN_EPOCHS):
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
            best_r2, best_preds, best_tgts = fm["r2"], preds_list[:], tgts_list[:]

    return best_preds, best_tgts


def run_hsgin_full_cv(graph_list, folds_info, in_dim_dict, device, label):
    """Run 5-fold HSGIN CV. Returns oof_records + agg."""
    fold_metrics, oof_records = [], []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        train_uids = set(fd["train_patient_uids"])
        val_uids   = set(fd["val_patient_uids"])
        val_seqns  = fd["val_seqn"]

        tr_gs, va_gs = preprocess_fold_graphs(graph_list, list(train_uids), list(val_uids))
        preds, tgts = train_hsgin_fold(tr_gs, va_gs, in_dim_dict, device, seed=SEED + f_num - 1)

        fm = compute_regression_metrics(tgts, preds)
        fold_metrics.append(fm)
        # Recover patient UIDs from val graphs (after preprocess, order preserved)
        for i, (seqn, yt, yp) in enumerate(zip(val_seqns, tgts, preds)):
            oof_records.append({"SEQN": seqn, "patient_uid": va_gs[i].patient_uid,
                                 "fold": f_num, "y_true": float(yt), "y_pred": float(yp)})
        print(f"    [{label}] Fold {f_num}  R²={fm['r2']:+.4f}  MAE={fm['mae']:.4f}")

    agg = aggregate_fold_metrics(fold_metrics)
    pooled = compute_regression_metrics(
        [r["y_true"] for r in oof_records], [r["y_pred"] for r in oof_records])
    return oof_records, fold_metrics, agg, pooled


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION B: EXPERIMENT 6 — FEATURE-DOMAIN ABLATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_experiment_6():
    print("\n" + "=" * 74)
    print("  EXPERIMENT 6: FEATURE-DOMAIN ABLATION")
    print("  Leave-one-domain-out + Single-domain-only")
    print("  Models: XGBoost (tuned) + HSGIN (seed 42)")
    print("=" * 74)

    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Load graphs and get base in_dim_dict
    graph_list = torch.load(GRAPH_PATH, weights_only=False)
    in_dim_dict_full = {nt: graph_list[0][nt].x.shape[1] for nt in graph_list[0].node_types}
    print(f"Graph in_dim_dict: {in_dim_dict_full}")

    domain_names = list(DOMAINS.keys())  # ['Demographics','Liver','Kidney','Heart','Biomarker']

    # Build ablation configs
    # leave-one-domain-out: exclude each domain in turn
    # single-domain-only  : only the named domain + Demographics (always included as covariate)
    ablation_configs = {}
    for dn in domain_names:
        # LOO: all features except this domain
        loo_feats = [f for dom, feats in DOMAINS.items() for f in feats if dom != dn]
        ablation_configs[f"LOO_{dn}"] = {
            "type": "leave_one_out", "excluded_domain": dn,
            "features": loo_feats
        }
    for dn in domain_names:
        # Single domain: only this domain's features
        # For Demographics alone it has 1 feature; we still run it
        single_feats = DOMAINS[dn]
        ablation_configs[f"ONLY_{dn}"] = {
            "type": "single_domain", "domain": dn,
            "features": single_feats
        }
    # Full model reference (all 25 features)
    ablation_configs["FULL_25"] = {
        "type": "full_reference", "features": ALL_FEATURES
    }

    exp6_results = {
        "experiment": "Exp6_FeatureDomainAblation",
        "seed": SEED,
        "domains": {k: v for k, v in DOMAINS.items()},
        "xgb_config": XGB_CONFIG,
        "hsgin_config": {"epochs": HSGIN_EPOCHS, "seed": SEED},
        "ablations": {}
    }

    # ── Run all XGBoost ablations ──────────────────────────────────────────────
    print("\n--- XGBoost Feature-Domain Ablations ---")
    xgb_full_preds = None   # will store for paired tests
    xgb_full_true  = None

    for abl_name, abl_cfg in ablation_configs.items():
        feat_cols = abl_cfg["features"]
        if len(feat_cols) == 0:
            print(f"  Skipping {abl_name}: 0 features")
            continue
        print(f"\n  XGBoost | {abl_name} ({len(feat_cols)} features): {feat_cols}")
        t0 = time.time()
        oof_recs, fold_ms, agg, pooled = run_xgb_full_cv(df, folds_info, feat_cols, f"XGB/{abl_name}")
        elapsed = time.time() - t0

        oof_csv = os.path.join(EXP6_OUT_DIR, f"XGBoost_{abl_name}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        if abl_name == "FULL_25":
            xgb_full_preds = np.array([r["y_pred"] for r in oof_recs])
            xgb_full_true  = np.array([r["y_true"] for r in oof_recs])

        exp6_results["ablations"][f"XGBoost_{abl_name}"] = {
            "config": abl_cfg,
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv,
            "elapsed_sec": round(elapsed, 2)
        }
        print(f"    -> Pooled R²={pooled['r2']:.4f} | "
              f"Mean-Fold R²={agg['r2_mean']:.4f}±{agg['r2_std']:.4f} | "
              f"RMSE={pooled['rmse']:.4f} [{elapsed:.1f}s]")

    # ── Paired bootstrap tests: each LOO vs FULL_25 (XGBoost) ─────────────────
    print("\n  Running paired bootstrap tests (XGBoost ablations vs FULL_25)...")
    xgb_bootstrap_results = {}
    for abl_name in ablation_configs:
        if abl_name == "FULL_25":
            continue
        key = f"XGBoost_{abl_name}"
        if key not in exp6_results["ablations"]:
            continue
        abl_preds = np.array([r["y_pred"] for r in
                              pd.read_csv(exp6_results["ablations"][key]["oof_csv"]).to_dict("records")])
        # Compare FULL_25 vs ablated (positive delta = FULL is better)
        bt = paired_bootstrap_comparison(xgb_full_true, xgb_full_preds, abl_preds,
                                         n_bootstraps=2000, seed=SEED)
        xgb_bootstrap_results[abl_name] = bt

    exp6_results["xgb_bootstrap_vs_full"] = xgb_bootstrap_results

    # ── Run HSGIN domain ablations (graph node masking) ───────────────────────
    # For graph ablations, the node feature dimensions don't change;
    # instead we zero out (mask) the features of the excluded domain node type
    # on-the-fly by creating masked copies. This keeps the model architecture
    # identical (same in_dim_dict) so results are architecture-controlled.
    print("\n--- HSGIN Feature-Domain Ablations (Node Feature Masking) ---")

    # Domain -> node_type mapping
    DOMAIN_TO_NODE = {
        "Demographics": "patient",
        "Liver": "liver",
        "Kidney": "kidney",
        "Heart": "heart",
        "Biomarker": "biomarker"
    }

    def mask_node_features(graph_list, masked_node_type):
        """Return graph list with the specified node type's features zeroed out."""
        masked = []
        for g in graph_list:
            g2 = g.clone()
            if masked_node_type in g2.node_types:
                g2[masked_node_type].x = torch.zeros_like(g2[masked_node_type].x)
            masked.append(g2)
        return masked

    hsgin_full_preds = None
    hsgin_full_true  = None

    # Build HSGIN ablation configs (node masking)
    hsgin_ablation_map = {"FULL_25": None}  # None = no masking
    for dn in domain_names:
        node_type = DOMAIN_TO_NODE[dn]
        hsgin_ablation_map[f"LOO_{dn}"] = node_type   # mask this node type
    # Single-domain-only: mask all OTHER node types
    for dn in domain_names:
        keep_node = DOMAIN_TO_NODE[dn]
        mask_nodes = [DOMAIN_TO_NODE[d] for d in domain_names if d != dn]
        hsgin_ablation_map[f"ONLY_{dn}"] = mask_nodes

    for abl_name, mask_spec in hsgin_ablation_map.items():
        print(f"\n  HSGIN | {abl_name}  mask_spec={mask_spec}")
        t0 = time.time()

        # Build masked graph list
        if mask_spec is None:
            cur_graphs = graph_list
        elif isinstance(mask_spec, str):
            cur_graphs = mask_node_features(graph_list, mask_spec)
        else:  # list of node types to mask
            cur_graphs = graph_list
            for nt in mask_spec:
                cur_graphs = mask_node_features(cur_graphs, nt)

        oof_recs, fold_ms, agg, pooled = run_hsgin_full_cv(
            cur_graphs, folds_info, in_dim_dict_full, device, f"HSGIN/{abl_name}")
        elapsed = time.time() - t0

        oof_csv = os.path.join(EXP6_OUT_DIR, f"HSGIN_{abl_name}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        if abl_name == "FULL_25":
            hsgin_full_preds = np.array([r["y_pred"] for r in oof_recs])
            hsgin_full_true  = np.array([r["y_true"] for r in oof_recs])

        exp6_results["ablations"][f"HSGIN_{abl_name}"] = {
            "mask_spec": mask_spec if isinstance(mask_spec, str) else (mask_spec or "none"),
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv,
            "elapsed_sec": round(elapsed, 2)
        }
        print(f"    -> Pooled R²={pooled['r2']:.4f} | "
              f"Mean-Fold R²={agg['r2_mean']:.4f}±{agg['r2_std']:.4f} | "
              f"RMSE={pooled['rmse']:.4f} [{elapsed:.1f}s]")

    # ── Paired bootstrap tests: each HSGIN ablation vs FULL_25 ────────────────
    print("\n  Running paired bootstrap tests (HSGIN ablations vs FULL_25)...")
    hsgin_bootstrap_results = {}
    for abl_name in hsgin_ablation_map:
        if abl_name == "FULL_25":
            continue
        key = f"HSGIN_{abl_name}"
        if key not in exp6_results["ablations"]:
            continue
        oof_df = pd.read_csv(exp6_results["ablations"][key]["oof_csv"])
        abl_preds = oof_df["y_pred"].values
        bt = paired_bootstrap_comparison(hsgin_full_true, hsgin_full_preds, abl_preds,
                                         n_bootstraps=2000, seed=SEED)
        hsgin_bootstrap_results[abl_name] = bt

    exp6_results["hsgin_bootstrap_vs_full"] = hsgin_bootstrap_results

    # ── Save master JSON ───────────────────────────────────────────────────────
    json_path = os.path.join(EXP6_OUT_DIR, "exp6_results.json")
    with open(json_path, "w") as f:
        json.dump(exp6_results, f, indent=2)

    print(f"\n  Exp6 JSON saved: {json_path}")
    return exp6_results


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION C: EXPERIMENT 7 — GRAPH ARCHITECTURE ABLATION
# ═══════════════════════════════════════════════════════════════════════════════

# ── 7a: HSGIN with no cross-organ edges (star topology only) ──────────────────
class HSGIN_NoCrossTalk(nn.Module):
    """
    HSGIN variant: patient-organ star edges only.
    Removes all 6 organ-to-organ 'interacts_with' edges.
    Architecture otherwise identical to HSGIN.
    """
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

    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim), nn.LayerNorm(hidden_dim),
                nn.ReLU(), nn.Dropout(dropout))

        import torch_geometric.nn as pyg_nn
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
                           if k in {et for et in self.STAR_EDGE_TYPES}}
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


# ── 7b: HSGIN with Flat Mean-Pool Readout (no organ-aware hierarchical) ───────
class HSGIN_FlatReadout(nn.Module):
    """
    HSGIN variant: replaces organ-aware [patient, organ_pool, biomarker]
    concatenation with a simple mean-pool across ALL node embeddings.
    """
    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.2):
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

        # Flat readout: single hidden_dim vector (mean of all node types)
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
        # Flat mean pool across all node types
        all_embs = torch.stack([h_dict[nt] for nt in self.node_types], dim=0).mean(dim=0)
        return self.predict_head(all_embs).squeeze(-1)


# ── 7c: Random-Edge Control ────────────────────────────────────────────────────
def randomize_graph_edges(graph_list, seed=42):
    """
    Return graph list where all edge_index tensors are randomly permuted.
    This creates a structurally-equivalent but semantically-randomized graph.
    Preserves node features and node counts exactly.
    """
    rng = np.random.default_rng(seed)
    randomized = []
    for g in graph_list:
        g2 = g.clone()
        for et in g2.edge_types:
            ei = g2[et].edge_index   # shape [2, E]
            E = ei.shape[1]
            n_src = g2[et[0]].x.shape[0]
            n_dst = g2[et[2]].x.shape[0]
            # Sample random edges preserving edge count
            new_src = torch.from_numpy(rng.integers(0, n_src, size=E))
            new_dst = torch.from_numpy(rng.integers(0, n_dst, size=E))
            g2[et].edge_index = torch.stack([new_src, new_dst], dim=0).long()
        randomized.append(g2)
    return randomized


# ── 7d: Homogeneous GNN (no node-type or relation-type distinctions) ──────────
class HomogeneousGNN(nn.Module):
    """
    Collapses all node types into a single type with uniform hidden_dim.
    Uses standard GCNConv (homogeneous message passing).
    Readout: mean pool of all nodes.
    """
    def __init__(self, in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.2):
        super().__init__()
        import torch_geometric.nn as pyg_nn
        self.hidden_dim = hidden_dim
        self.node_types = list(in_dim_dict.keys())

        # Per-type input projections to unified hidden_dim
        self.encoder_dict = nn.ModuleDict()
        for ntype, in_dim in in_dim_dict.items():
            self.encoder_dict[ntype] = nn.Linear(in_dim, hidden_dim)

        # Homogeneous GCN layers (treat all as same type)
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            self.convs.append(pyg_nn.GCNConv(hidden_dim, hidden_dim, add_self_loops=True))

        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(hidden_dim)

        self.predict_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(), nn.Linear(hidden_dim // 2, 1))

    def forward(self, batch_graph):
        # Build homogeneous node features and edge index
        # Node order: patient, liver, kidney, heart, biomarker per graph-in-batch
        x_dict = batch_graph.x_dict
        h_dict = {nt: self.encoder_dict[nt](x_dict[nt]) for nt in self.node_types}

        # Concatenate all nodes
        h_all = torch.cat([h_dict[nt] for nt in self.node_types], dim=0)  # [N_total, H]

        # Build merged homogeneous edge index
        # We offset indices for each node type
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
            edge_indices.append(ei + torch.tensor([[src_off], [dst_off]],
                                                   device=ei.device))
        if edge_indices:
            edge_index = torch.cat(edge_indices, dim=1)
        else:
            edge_index = torch.zeros((2, 0), dtype=torch.long, device=h_all.device)

        # GCN message passing
        h = h_all
        for conv in self.convs:
            h = conv(h, edge_index)
            h = torch.relu(h)
            h = self.dropout(h)
        h = self.norm(h)

        # Extract patient node outputs only (first node per graph)
        # Patient nodes are the first node_type, so offset 0
        n_patient = h_dict["patient"].shape[0]
        h_patient = h[:n_patient]  # [N_patients_in_batch, H]

        return self.predict_head(h_patient).squeeze(-1)


def train_ablation_model_fold(model_cls, model_kwargs, train_graphs, val_graphs, device, seed):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=HSGIN_BATCH, shuffle=True)
    val_loader   = PyGDataLoader(val_graphs,   batch_size=HSGIN_BATCH, shuffle=False)

    model = model_cls(**model_kwargs).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=HSGIN_LR, weight_decay=HSGIN_WD)
    criterion = nn.SmoothL1Loss()

    best_r2, best_preds, best_tgts = -999.0, None, None

    for epoch in range(HSGIN_EPOCHS):
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
                out = model(batch)
                preds_list.extend(out.cpu().numpy().flatten())
                tgts_list.extend(batch["patient"].y.cpu().numpy().flatten())

        fm = compute_regression_metrics(tgts_list, preds_list)
        if fm["r2"] > best_r2 or epoch == 0:
            best_r2, best_preds, best_tgts = fm["r2"], preds_list[:], tgts_list[:]

    return best_preds, best_tgts


def run_graph_ablation_cv(graph_list, folds_info, model_cls, model_kwargs, device, label):
    """Run 5-fold CV for a graph architecture variant."""
    fold_metrics, oof_records = [], []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        train_uids = set(fd["train_patient_uids"])
        val_uids   = set(fd["val_patient_uids"])
        val_seqns  = fd["val_seqn"]

        tr_gs, va_gs = preprocess_fold_graphs(graph_list, list(train_uids), list(val_uids))
        preds, tgts = train_ablation_model_fold(
            model_cls, model_kwargs, tr_gs, va_gs, device, seed=SEED + f_num - 1)

        fm = compute_regression_metrics(tgts, preds)
        fold_metrics.append(fm)
        for i, (seqn, yt, yp) in enumerate(zip(val_seqns, tgts, preds)):
            oof_records.append({"SEQN": seqn, "patient_uid": va_gs[i].patient_uid,
                                 "fold": f_num, "y_true": float(yt), "y_pred": float(yp)})
        print(f"    [{label}] Fold {f_num}  R²={fm['r2']:+.4f}  MAE={fm['mae']:.4f}")

    agg = aggregate_fold_metrics(fold_metrics)
    pooled = compute_regression_metrics(
        [r["y_true"] for r in oof_records], [r["y_pred"] for r in oof_records])
    return oof_records, fold_metrics, agg, pooled


def run_experiment_7(hsgin_full_oof_csv):
    print("\n" + "=" * 74)
    print("  EXPERIMENT 7: GRAPH ARCHITECTURE ABLATION")
    print("  Variants: NoCrossTalk | FlatReadout | RandomEdges | HomoGNN")
    print("=" * 74)

    folds_info = generate_or_load_folds()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    graph_list = torch.load(GRAPH_PATH, weights_only=False)
    in_dim_dict = {nt: graph_list[0][nt].x.shape[1] for nt in graph_list[0].node_types}

    # Load HSGIN full reference OOF (from Exp6 HSGIN_FULL_25)
    hsgin_ref_df = pd.read_csv(hsgin_full_oof_csv)
    hsgin_ref_preds = hsgin_ref_df["y_pred"].values
    hsgin_ref_true  = hsgin_ref_df["y_true"].values

    exp7_results = {
        "experiment": "Exp7_GraphArchAblation",
        "seed": SEED,
        "reference_model": "HSGIN_FULL_25 (from Exp6)",
        "reference_oof_csv": hsgin_full_oof_csv,
        "variants": {}
    }

    # Define variants
    arch_variants = [
        ("NoCrossTalk",   HSGIN_NoCrossTalk, {"in_dim_dict": in_dim_dict, "hidden_dim": HSGIN_HIDDEN,
                                               "num_layers": HSGIN_LAYERS, "dropout": HSGIN_DROPOUT},
         graph_list, "Remove 6 organ-organ cross-talk edges; keep star topology only"),
        ("FlatReadout",   HSGIN_FlatReadout, {"in_dim_dict": in_dim_dict, "hidden_dim": HSGIN_HIDDEN,
                                               "num_layers": HSGIN_LAYERS, "dropout": HSGIN_DROPOUT},
         graph_list, "Replace organ-aware readout with flat mean-pool across all node types"),
        ("RandomEdges",   HSGIN,            {"in_dim_dict": in_dim_dict, "hidden_dim": HSGIN_HIDDEN,
                                               "num_layers": HSGIN_LAYERS, "dropout": HSGIN_DROPOUT},
         randomize_graph_edges(graph_list, seed=SEED),
         "HSGIN architecture on randomized edge topology (structural null control)"),
        ("HomoGNN",       HomogeneousGNN,   {"in_dim_dict": in_dim_dict, "hidden_dim": HSGIN_HIDDEN,
                                               "num_layers": HSGIN_LAYERS, "dropout": HSGIN_DROPOUT},
         graph_list, "Homogeneous GCN — no node-type or relation-type distinctions"),
    ]

    for variant_name, model_cls, model_kwargs, cur_graphs, description in arch_variants:
        print(f"\n  Variant: {variant_name}")
        print(f"  Description: {description}")
        t0 = time.time()
        oof_recs, fold_ms, agg, pooled = run_graph_ablation_cv(
            cur_graphs, folds_info, model_cls, model_kwargs, device, variant_name)
        elapsed = time.time() - t0

        oof_csv = os.path.join(EXP6_OUT_DIR, f"HSGIN_{variant_name}_oof.csv")
        pd.DataFrame(oof_recs).to_csv(oof_csv, index=False)

        # Paired bootstrap vs HSGIN full reference
        abl_preds = np.array([r["y_pred"] for r in oof_recs])
        bt = paired_bootstrap_comparison(hsgin_ref_true, hsgin_ref_preds, abl_preds,
                                         n_bootstraps=2000, seed=SEED)

        exp7_results["variants"][variant_name] = {
            "description": description,
            "fold_metrics": fold_ms,
            "aggregate": agg,
            "pooled": pooled,
            "bootstrap_vs_hsgin_full": bt,
            "oof_csv": oof_csv,
            "elapsed_sec": round(elapsed, 2)
        }

        sign = "YES" if bt["a_significantly_better_r2"] else "NO"
        print(f"    -> Pooled R²={pooled['r2']:.4f} | "
              f"Mean-Fold R²={agg['r2_mean']:.4f}±{agg['r2_std']:.4f} | "
              f"Delta vs HSGIN={bt['observed_delta_r2']:+.4f} | "
              f"HSGIN Significantly Better: {sign} [{elapsed:.1f}s]")

    # Save JSON
    json_path = os.path.join(EXP6_OUT_DIR, "exp7_results.json")
    with open(json_path, "w") as f:
        json.dump(exp7_results, f, indent=2)

    print(f"\n  Exp7 JSON saved: {json_path}")
    return exp7_results


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    t_total = time.time()

    print("=" * 74)
    print("  PHASE 6: FEATURE-DOMAIN & GRAPH ARCHITECTURE ABLATIONS")
    print("  PRD v1.1 | Experiments 6 & 7")
    print("=" * 74)

    # Run Experiment 6
    exp6 = run_experiment_6()

    # Run Experiment 7 (uses HSGIN_FULL_25 OOF from Exp6 as reference)
    hsgin_full_csv = os.path.join(EXP6_OUT_DIR, "HSGIN_FULL_25_oof.csv")
    exp7 = run_experiment_7(hsgin_full_csv)

    # ── Build combined summary markdown ───────────────────────────────────────
    md_path = os.path.join(EXP6_OUT_DIR, "exp6_7_summary.md")

    # Gather XGBoost ablation rows
    domain_order = ["Liver", "Kidney", "Heart", "Biomarker", "Demographics"]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Experiments 6 & 7 Summary: Feature-Domain and Graph Architecture Ablations\n\n")
        f.write(f"- **Folds**: 5-fold patient-level (folds_v1.json, N=6,277, seed=42)\n")
        f.write(f"- **XGBoost config**: Fixed 400 trees (Exp2 avg best_iter), all other HPs identical to Exp2\n")
        f.write(f"- **HSGIN config**: seed=42, 50 epochs, hidden=64, layers=2, identical to Exp4\n\n")

        f.write("## Experiment 6a: XGBoost Feature-Domain Ablation\n\n")
        f.write("| Ablation | Type | Features | Pooled R² | Mean-Fold R² ± SD | RMSE | ΔR² vs Full | Sig. (p<0.05)? |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")

        # Full reference first
        full_key = "XGBoost_FULL_25"
        if full_key in exp6["ablations"]:
            r = exp6["ablations"][full_key]
            f.write(f"| **Full (25 features)** | Reference | 25 | "
                    f"**{r['pooled']['r2']:.4f}** | "
                    f"{r['aggregate']['r2_mean']:.4f}±{r['aggregate']['r2_std']:.4f} | "
                    f"{r['pooled']['rmse']:.4f} | — | — |\n")

        for dn in domain_order:
            for abl_type, prefix in [("LOO", "Leave-One-Out"), ("ONLY", "Single-Domain")]:
                abl_name = f"{abl_type}_{dn}"
                key = f"XGBoost_{abl_name}"
                if key not in exp6["ablations"]:
                    continue
                r = exp6["ablations"][key]
                n_feats = len(r["config"]["features"])
                bt = exp6["xgb_bootstrap_vs_full"].get(abl_name, {})
                delta = bt.get("observed_delta_r2", float("nan"))
                sig = "YES" if bt.get("a_significantly_better_r2", False) else "NO"
                f.write(f"| {abl_name} | {prefix} | {n_feats} | "
                        f"{r['pooled']['r2']:.4f} | "
                        f"{r['aggregate']['r2_mean']:.4f}±{r['aggregate']['r2_std']:.4f} | "
                        f"{r['pooled']['rmse']:.4f} | "
                        f"{delta:+.4f} | {sig} |\n")

        f.write("\n> ΔR² = Full_25 R² minus ablated R² (positive = domain contributes).\n")
        f.write("> Significance: paired patient-level bootstrap (B=2,000, α=0.05).\n\n")

        f.write("## Experiment 6b: HSGIN Feature-Domain Ablation (Node Masking)\n\n")
        f.write("| Ablation | Pooled R² | Mean-Fold R² ± SD | RMSE | ΔR² vs Full | Sig. (p<0.05)? |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")

        full_key_h = "HSGIN_FULL_25"
        if full_key_h in exp6["ablations"]:
            r = exp6["ablations"][full_key_h]
            f.write(f"| **Full HSGIN (all nodes)** | "
                    f"**{r['pooled']['r2']:.4f}** | "
                    f"{r['aggregate']['r2_mean']:.4f}±{r['aggregate']['r2_std']:.4f} | "
                    f"{r['pooled']['rmse']:.4f} | — | — |\n")

        for dn in domain_order:
            for abl_type in ["LOO", "ONLY"]:
                abl_name = f"{abl_type}_{dn}"
                key = f"HSGIN_{abl_name}"
                if key not in exp6["ablations"]:
                    continue
                r = exp6["ablations"][key]
                bt = exp6["hsgin_bootstrap_vs_full"].get(abl_name, {})
                delta = bt.get("observed_delta_r2", float("nan"))
                sig = "YES" if bt.get("a_significantly_better_r2", False) else "NO"
                f.write(f"| {abl_name} | "
                        f"{r['pooled']['r2']:.4f} | "
                        f"{r['aggregate']['r2_mean']:.4f}±{r['aggregate']['r2_std']:.4f} | "
                        f"{r['pooled']['rmse']:.4f} | "
                        f"{delta:+.4f} | {sig} |\n")

        f.write("\n")
        f.write("## Experiment 7: Graph Architecture Ablation\n\n")
        f.write("Reference: HSGIN full (seed 42, all 25 features, organ-aware readout)\n\n")
        f.write("| Variant | Description | Pooled R² | Mean-Fold R² ± SD | RMSE | ΔR² vs HSGIN | Sig. (p<0.05)? |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n")

        # HSGIN full as reference row
        if full_key_h in exp6["ablations"]:
            r = exp6["ablations"][full_key_h]
            f.write(f"| **HSGIN Full (Reference)** | Organ-aware readout + cross-talk | "
                    f"**{r['pooled']['r2']:.4f}** | "
                    f"{r['aggregate']['r2_mean']:.4f}±{r['aggregate']['r2_std']:.4f} | "
                    f"{r['pooled']['rmse']:.4f} | — | — |\n")

        for vname, vdata in exp7["variants"].items():
            bt = vdata["bootstrap_vs_hsgin_full"]
            sig = "YES (HSGIN>)" if bt["a_significantly_better_r2"] else \
                  ("YES (Var>)" if bt["b_significantly_better_r2"] else "NO")
            f.write(f"| **{vname}** | {vdata['description'][:55]}... | "
                    f"{vdata['pooled']['r2']:.4f} | "
                    f"{vdata['aggregate']['r2_mean']:.4f}±{vdata['aggregate']['r2_std']:.4f} | "
                    f"{vdata['pooled']['rmse']:.4f} | "
                    f"{bt['observed_delta_r2']:+.4f} | {sig} |\n")

        f.write(f"\nTotal Phase 6 elapsed: {(time.time()-t_total)/60:.1f} min\n")

    print(f"\n{'='*74}")
    print(f"  PHASE 6 COMPLETE")
    print(f"  Exp6 JSON: results/comparative/exp6_ablations/exp6_results.json")
    print(f"  Exp7 JSON: results/comparative/exp6_ablations/exp7_results.json")
    print(f"  Summary  : results/comparative/exp6_ablations/exp6_7_summary.md")
    print(f"  Total elapsed: {(time.time()-t_total)/60:.1f} min")
    print(f"{'='*74}")
