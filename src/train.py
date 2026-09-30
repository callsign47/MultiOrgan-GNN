import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from src.pipeline import (
    FINAL_COHORT_PATH,
    get_leak_free_feature_list,
    get_5fold_splits,
    preprocess_fold_tabular,
    preprocess_fold_graphs
)
from src.graph_builder import build_all_graphs, OUTPUT_DIR
from src.models.hsgin import HSGIN
from src.models.baselines import (
    get_tabular_baselines,
    StandardGNNBaseline,
    ClassicalHGNN
)
from src.ablation import run_organ_ablation_study
from src.y_randomization import run_in_fold_y_randomization

GRAPH_PATH = os.path.join(OUTPUT_DIR, "patient_graphs.pt")
RESULTS_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\experiment_results.json"
REPORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\reports\experiment_report.md"

def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def evaluate_predictions(y_true, y_pred):
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(root_mean_squared_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    return {'mae': mae, 'rmse': rmse, 'r2': r2}

def train_hsgin_fold(train_graphs, val_graphs, in_dim_dict, device, epochs=50, lr=0.001, seed=42):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=64, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=64, shuffle=False)
    
    model = HSGIN(in_dim_dict=in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.SmoothL1Loss()
    
    best_val_r2 = -999.0
    best_metrics = None
    
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
                
        metrics = evaluate_predictions(val_targets, val_preds)
        if metrics['r2'] > best_val_r2 or epoch == 0:
            best_val_r2 = metrics['r2']
            best_metrics = metrics
            
    return best_metrics

def train_classical_hgnn_fold(train_graphs, val_graphs, in_dim_dict, device, epochs=50, lr=0.001, seed=42):
    set_seed(seed)
    train_loader = PyGDataLoader(train_graphs, batch_size=64, shuffle=True)
    val_loader = PyGDataLoader(val_graphs, batch_size=64, shuffle=False)
    
    model = ClassicalHGNN(in_dim_dict=in_dim_dict, hidden_dim=64, dropout=0.1).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.SmoothL1Loss()
    
    best_val_r2 = -999.0
    best_metrics = None
    
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
                
        metrics = evaluate_predictions(val_targets, val_preds)
        if metrics['r2'] > best_val_r2 or epoch == 0:
            best_val_r2 = metrics['r2']
            best_metrics = metrics
            
    return best_metrics

def run_phase_2_pipeline():
    print("==========================================================================")
    print("    STARTING PHASE 2: HSGIN 3-ORGAN PIPELINE EXPERIMENTAL SUITE           ")
    print("==========================================================================")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device locked for execution: {device}")
    if torch.cuda.is_available():
        print(f"GPU Model: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB VRAM)")
        
    df = pd.read_csv(FINAL_COHORT_PATH)
    splits = get_5fold_splits(df)
    
    if os.path.exists(GRAPH_PATH):
        print(f"Loading pre-built PyG HeteroData graphs from {GRAPH_PATH}...")
        graph_list = torch.load(GRAPH_PATH)
    else:
        graph_list, _ = build_all_graphs()
        
    in_dim_dict = {ntype: graph_list[0][ntype].x.shape[1] for ntype in graph_list[0].node_types}
    print(f"Node Dimension Dictionary: {in_dim_dict}")
    
    experiment_results = {}
    
    # --------------------------------------------------------------------------
    # 1. TABULAR BASELINE BENCHMARKS (5-FOLD CV)
    # --------------------------------------------------------------------------
    print("\n--- 1. Tabular Baseline Evaluation (5-Fold CV) ---")
    tabular_models = get_tabular_baselines()
    feature_cols = get_leak_free_feature_list()
    
    tabular_results = {}
    for name, model_init in tabular_models.items():
        maes, rmses, r2s = [], [], []
        for train_uids, val_uids in splits:
            X_tr, y_tr, X_va, y_va, _, _ = preprocess_fold_tabular(df, train_uids, val_uids, feature_cols)
            model_init.fit(X_tr, y_tr)
            preds = model_init.predict(X_va)
            m = evaluate_predictions(y_va, preds)
            maes.append(m['mae'])
            rmses.append(m['rmse'])
            r2s.append(m['r2'])
            
        tabular_results[name] = {
            'mae_mean': float(np.mean(maes)), 'mae_std': float(np.std(maes)),
            'rmse_mean': float(np.mean(rmses)), 'rmse_std': float(np.std(rmses)),
            'r2_mean': float(np.mean(r2s)), 'r2_std': float(np.std(r2s))
        }
        print(f"  {name:20s} | MAE: {np.mean(maes):.4f}±{np.std(maes):.4f} | RMSE: {np.mean(rmses):.4f}±{np.std(rmses):.4f} | R²: {np.mean(r2s):.4f}±{np.std(r2s):.4f}")
        
    experiment_results['tabular_baselines'] = tabular_results
    
    # --------------------------------------------------------------------------
    # 2. CLASSICAL HGNN BASELINE (5-FOLD CV)
    # --------------------------------------------------------------------------
    print("\n--- 2. Classical HGNN Baseline Evaluation (5-Fold CV) ---")
    hgnn_maes, hgnn_rmses, hgnn_r2s = [], [], []
    for fold, (train_uids, val_uids) in enumerate(splits):
        tr_graphs, va_graphs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        metrics = train_classical_hgnn_fold(tr_graphs, va_graphs, in_dim_dict, device, epochs=40, seed=42+fold)
        hgnn_maes.append(metrics['mae'])
        hgnn_rmses.append(metrics['rmse'])
        hgnn_r2s.append(metrics['r2'])
        print(f"  Fold {fold+1} -> Val MAE: {metrics['mae']:.4f} | Val RMSE: {metrics['rmse']:.4f} | Val R²: {metrics['r2']:.4f}")
        
    experiment_results['classical_hgnn'] = {
        'mae_mean': float(np.mean(hgnn_maes)), 'mae_std': float(np.std(hgnn_maes)),
        'rmse_mean': float(np.mean(hgnn_rmses)), 'rmse_std': float(np.std(hgnn_rmses)),
        'r2_mean': float(np.mean(hgnn_r2s)), 'r2_std': float(np.std(hgnn_r2s))
    }
    print(f"  Classical HGNN Aggregate -> MAE: {np.mean(hgnn_maes):.4f}±{np.std(hgnn_maes):.4f} | RMSE: {np.mean(hgnn_rmses):.4f}±{np.std(hgnn_rmses):.4f} | R²: {np.mean(hgnn_r2s):.4f}±{np.std(hgnn_r2s):.4f}")
    
    # --------------------------------------------------------------------------
    # 3. PROPOSED HSGIN GRAPH NEURAL NETWORK (5-FOLD CV)
    # --------------------------------------------------------------------------
    print("\n--- 3. Proposed HSGIN Heterogeneous Architecture Evaluation (5-Fold CV) ---")
    hsgin_maes, hsgin_rmses, hsgin_r2s = [], [], []
    for fold, (train_uids, val_uids) in enumerate(splits):
        tr_graphs, va_graphs = preprocess_fold_graphs(graph_list, train_uids, val_uids)
        metrics = train_hsgin_fold(tr_graphs, va_graphs, in_dim_dict, device, epochs=50, seed=42+fold)
        hsgin_maes.append(metrics['mae'])
        hsgin_rmses.append(metrics['rmse'])
        hsgin_r2s.append(metrics['r2'])
        print(f"  Fold {fold+1} -> Val MAE: {metrics['mae']:.4f} | Val RMSE: {metrics['rmse']:.4f} | Val R²: {metrics['r2']:.4f}")
        
    experiment_results['hsgin_proposed'] = {
        'mae_mean': float(np.mean(hsgin_maes)), 'mae_std': float(np.std(hsgin_maes)),
        'rmse_mean': float(np.mean(hsgin_rmses)), 'rmse_std': float(np.std(hsgin_rmses)),
        'r2_mean': float(np.mean(hsgin_r2s)), 'r2_std': float(np.std(hsgin_r2s))
    }
    print(f"\n  HSGIN Aggregate -> MAE: {np.mean(hsgin_maes):.4f}±{np.std(hsgin_maes):.4f} | RMSE: {np.mean(hsgin_rmses):.4f}±{np.std(hsgin_rmses):.4f} | R²: {np.mean(hsgin_r2s):.4f}±{np.std(hsgin_r2s):.4f}")
    
    # --------------------------------------------------------------------------
    # 4. A–D ORGAN ABLATION STUDY
    # --------------------------------------------------------------------------
    print("\n--- 4. Executing Organ Ablation Study ---")
    ablation_results = run_organ_ablation_study(FINAL_COHORT_PATH)
    experiment_results['ablation_study'] = ablation_results
    
    # --------------------------------------------------------------------------
    # 5. IN-FOLD TARGET Y-RANDOMIZATION CHECK
    # --------------------------------------------------------------------------
    print("\n--- 5. Executing In-Fold Y-Randomization Validation ---")
    y_rand_results = run_in_fold_y_randomization(FINAL_COHORT_PATH)
    experiment_results['y_randomization'] = y_rand_results
    
    # Save raw JSON results
    with open(RESULTS_PATH, 'w') as f:
        json.dump(experiment_results, f, indent=2)
    print(f"\nSaved raw JSON experiment results to: {RESULTS_PATH}")
    
    return experiment_results

if __name__ == "__main__":
    run_phase_2_pipeline()
