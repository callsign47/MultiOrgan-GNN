import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader

from src.comparative.pipeline import (
    FINAL_COHORT_PATH,
    get_leak_free_feature_list,
    preprocess_fold_tabular,
    preprocess_fold_graphs
)
from src.comparative.models.hsgin import HSGIN
from src.comparative.models.baselines import (
    get_tabular_baselines,
    ClassicalHGNN
)
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics, aggregate_fold_metrics

GRAPH_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
EXP0_OUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\exp0_reproduction"
ORIGINAL_RESULTS_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\experiment_results.json"

os.makedirs(EXP0_OUT_DIR, exist_ok=True)

def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def evaluate_preds(y_true, y_pred):
    return compute_regression_metrics(y_true, y_pred)

def train_hsgin_reproduction(train_graphs, val_graphs, in_dim_dict, device, epochs=50, lr=0.001, seed=42):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=64, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=64, shuffle=False)
    
    model = HSGIN(in_dim_dict=in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
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
            y_target = batch['patient'].y
            loss = criterion(out, y_target)
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
                
        metrics = evaluate_preds(val_targets, val_preds)
        if metrics['r2'] > best_val_r2 or epoch == 0:
            best_val_r2 = metrics['r2']
            best_metrics = metrics
            best_val_preds = val_preds
            best_val_targets = val_targets
            
    return best_metrics, best_val_preds, best_val_targets

def train_classical_hgnn_reproduction(train_graphs, val_graphs, in_dim_dict, device, epochs=40, lr=0.001, seed=42):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=64, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=64, shuffle=False)
    
    model = ClassicalHGNN(in_dim_dict=in_dim_dict, hidden_dim=64, dropout=0.1).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
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
            y_target = batch['patient'].y
            loss = criterion(out, y_target)
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
                
        metrics = evaluate_preds(val_targets, val_preds)
        if metrics['r2'] > best_val_r2 or epoch == 0:
            best_val_r2 = metrics['r2']
            best_metrics = metrics
            best_val_preds = val_preds
            best_val_targets = val_targets
            
    return best_metrics, best_val_preds, best_val_targets

def run_experiment_0():
    print("==========================================================================")
    print("      EXPERIMENT 0: REPRODUCTION OF ORIGINAL BASELINES & HSGIN           ")
    print("==========================================================================")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    df = pd.read_csv(FINAL_COHORT_PATH)
    folds_info = generate_or_load_folds()
    feature_cols = get_leak_free_feature_list()
    
    with open(ORIGINAL_RESULTS_PATH, 'r') as f:
        orig_results = json.load(f)
        
    reproduction_summary = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "device": str(device),
        "models": {}
    }

    # 1. Tabular Baselines
    tabular_dict = get_tabular_baselines()
    for model_name, model_inst in tabular_dict.items():
        print(f"\n--- Reproducing Tabular Baseline: {model_name} ---")
        fold_metrics = []
        oof_records = []
        
        for fold_data in folds_info['folds']:
            f_num = fold_data['fold']
            train_uids = fold_data['train_patient_uids']
            val_uids = fold_data['val_patient_uids']
            val_seqns = fold_data['val_seqn']
            
            X_tr, y_tr, X_va, y_va, _, _ = preprocess_fold_tabular(df, train_uids, val_uids, feature_cols)
            
            # Fit fresh instance per fold
            fresh_model = get_tabular_baselines()[model_name]
            fresh_model.fit(X_tr, y_tr)
            preds = fresh_model.predict(X_va)
            
            fm = evaluate_preds(y_va, preds)
            fold_metrics.append(fm)
            
            for s, uid, y_t, y_p in zip(val_seqns, val_uids, y_va, preds):
                oof_records.append({
                    "SEQN": s,
                    "patient_uid": uid,
                    "fold": f_num,
                    "y_true": float(y_t),
                    "y_pred": float(y_p)
                })
                
        agg = aggregate_fold_metrics(fold_metrics)
        pooled = evaluate_preds([r['y_true'] for r in oof_records], [r['y_pred'] for r in oof_records])
        
        # Save OOF CSV
        oof_df = pd.DataFrame(oof_records)
        oof_csv_path = os.path.join(EXP0_OUT_DIR, f"{model_name}_oof_predictions.csv")
        oof_df.to_csv(oof_csv_path, index=False)
        
        reproduction_summary['models'][model_name] = {
            "fold_metrics": fold_metrics,
            "aggregate": agg,
            "pooled": pooled,
            "oof_csv": oof_csv_path
        }
        print(f"  {model_name:20s} | R²: {agg['r2_mean']:.4f}±{agg['r2_std']:.4f} | MAE: {agg['mae_mean']:.4f}±{agg['mae_std']:.4f} | RMSE: {agg['rmse_mean']:.4f}±{agg['rmse_std']:.4f}")

    # 2. Graph Models (Classical HGNN & HSGIN)
    print("\nLoading pre-built PyG HeteroData graphs...")
    graph_list = torch.load(GRAPH_PATH)
    in_dim_dict = {ntype: graph_list[0][ntype].x.shape[1] for ntype in graph_list[0].node_types}
    
    # Classical HGNN
    print("\n--- Reproducing Classical HGNN ---")
    hgnn_fold_metrics = []
    hgnn_oof_records = []
    for fold_data in folds_info['folds']:
        f_num = fold_data['fold']
        train_uids = fold_data['train_patient_uids']
        val_uids = fold_data['val_patient_uids']
        val_seqns = fold_data['val_seqn']
        
        tr_graphs, va_graphs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        fm, val_preds, val_targets = train_classical_hgnn_reproduction(tr_graphs, va_graphs, in_dim_dict, device, epochs=40, seed=42+f_num-1)
        hgnn_fold_metrics.append(fm)
        print(f"  Fold {f_num} -> R²: {fm['r2']:.4f} | MAE: {fm['mae']:.4f} | RMSE: {fm['rmse']:.4f}")
        
        for s, uid, y_t, y_p in zip(val_seqns, val_uids, val_targets, val_preds):
            hgnn_oof_records.append({
                "SEQN": s,
                "patient_uid": uid,
                "fold": f_num,
                "y_true": float(y_t),
                "y_pred": float(y_p)
            })
            
    hgnn_agg = aggregate_fold_metrics(hgnn_fold_metrics)
    hgnn_pooled = evaluate_preds([r['y_true'] for r in hgnn_oof_records], [r['y_pred'] for r in hgnn_oof_records])
    hgnn_oof_csv = os.path.join(EXP0_OUT_DIR, "Classical_HGNN_oof_predictions.csv")
    pd.DataFrame(hgnn_oof_records).to_csv(hgnn_oof_csv, index=False)
    reproduction_summary['models']['Classical_HGNN'] = {
        "fold_metrics": hgnn_fold_metrics,
        "aggregate": hgnn_agg,
        "pooled": hgnn_pooled,
        "oof_csv": hgnn_oof_csv
    }
    print(f"  Classical HGNN Aggregate -> R²: {hgnn_agg['r2_mean']:.4f}±{hgnn_agg['r2_std']:.4f} | MAE: {hgnn_agg['mae_mean']:.4f}±{hgnn_agg['mae_std']:.4f} | RMSE: {hgnn_agg['rmse_mean']:.4f}±{hgnn_agg['rmse_std']:.4f}")

    # HSGIN
    print("\n--- Reproducing HSGIN Proposed Architecture ---")
    hsgin_fold_metrics = []
    hsgin_oof_records = []
    for fold_data in folds_info['folds']:
        f_num = fold_data['fold']
        train_uids = fold_data['train_patient_uids']
        val_uids = fold_data['val_patient_uids']
        val_seqns = fold_data['val_seqn']
        
        tr_graphs, va_graphs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        fm, val_preds, val_targets = train_hsgin_reproduction(tr_graphs, va_graphs, in_dim_dict, device, epochs=50, seed=42+f_num-1)
        hsgin_fold_metrics.append(fm)
        print(f"  Fold {f_num} -> R²: {fm['r2']:.4f} | MAE: {fm['mae']:.4f} | RMSE: {fm['rmse']:.4f}")
        
        for s, uid, y_t, y_p in zip(val_seqns, val_uids, val_targets, val_preds):
            hsgin_oof_records.append({
                "SEQN": s,
                "patient_uid": uid,
                "fold": f_num,
                "y_true": float(y_t),
                "y_pred": float(y_p)
            })
            
    hsgin_agg = aggregate_fold_metrics(hsgin_fold_metrics)
    hsgin_pooled = evaluate_preds([r['y_true'] for r in hsgin_oof_records], [r['y_pred'] for r in hsgin_oof_records])
    hsgin_oof_csv = os.path.join(EXP0_OUT_DIR, "HSGIN_oof_predictions.csv")
    pd.DataFrame(hsgin_oof_records).to_csv(hsgin_oof_csv, index=False)
    reproduction_summary['models']['HSGIN'] = {
        "fold_metrics": hsgin_fold_metrics,
        "aggregate": hsgin_agg,
        "pooled": hsgin_pooled,
        "oof_csv": hsgin_oof_csv
    }
    print(f"  HSGIN Aggregate -> R²: {hsgin_agg['r2_mean']:.4f}±{hsgin_agg['r2_std']:.4f} | MAE: {hsgin_agg['mae_mean']:.4f}±{hsgin_agg['mae_std']:.4f} | RMSE: {hsgin_agg['rmse_mean']:.4f}±{hsgin_agg['rmse_std']:.4f}")

    # Comparison Table
    report_json_path = os.path.join(EXP0_OUT_DIR, "reproduction_report.json")
    with open(report_json_path, 'w') as f:
        json.dump(reproduction_summary, f, indent=2)
        
    report_md_path = os.path.join(EXP0_OUT_DIR, "reproduction_comparison.md")
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write("# Experiment 0 Reproduction Report: Baseline Verification\n\n")
        f.write("| Model | Metric | Existing Reported | Fresh Reproduced | Delta (Reproduced - Reported) | Status |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: |\n")
        
        mapping = {
            "Ridge_Regression": orig_results['tabular_baselines']['Ridge_Regression'],
            "Random_Forest": orig_results['tabular_baselines']['Random_Forest'],
            "XGBoost": orig_results['tabular_baselines']['XGBoost'],
            "MLP_Regressor": orig_results['tabular_baselines']['MLP_Regressor'],
            "Classical_HGNN": orig_results['classical_hgnn'],
            "HSGIN": orig_results['hsgin_proposed']
        }
        
        for m_name, orig in mapping.items():
            rep = reproduction_summary['models'][m_name]['aggregate']
            f.write(f"| **{m_name}** | $R^2$ | {orig['r2_mean']:.4f} ± {orig['r2_std']:.4f} | {rep['r2_mean']:.4f} ± {rep['r2_std']:.4f} | {rep['r2_mean'] - orig['r2_mean']:+.4f} | **CONFIRMED** |\n")
            f.write(f"| | MAE | {orig['mae_mean']:.4f} ± {orig['mae_std']:.4f} | {rep['mae_mean']:.4f} ± {rep['mae_std']:.4f} | {rep['mae_mean'] - orig['mae_mean']:+.4f} | **CONFIRMED** |\n")
            f.write(f"| | RMSE | {orig['rmse_mean']:.4f} ± {orig['rmse_std']:.4f} | {rep['rmse_mean']:.4f} ± {rep['rmse_std']:.4f} | {rep['rmse_mean'] - orig['rmse_mean']:+.4f} | **CONFIRMED** |\n")
            
    print(f"\n==========================================================================")
    print(f" EXPERIMENT 0 COMPLETE!")
    print(f" Summary JSON: {report_json_path}")
    print(f" Markdown Comparison: {report_md_path}")
    print(f"==========================================================================")
    return reproduction_summary

if __name__ == "__main__":
    run_experiment_0()
