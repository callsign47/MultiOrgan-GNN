import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import json
import numpy as np
import pandas as pd
import torch

from src.pipeline import (
    FINAL_COHORT_PATH,
    get_5fold_splits,
    preprocess_fold_graphs
)
from src.graph_builder import OUTPUT_DIR
from src.train import train_hsgin_fold, evaluate_predictions

GRAPH_PATH = os.path.join(OUTPUT_DIR, "patient_graphs.pt")
RESULTS_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\experiment_results.json"

ABLATION_CONFIGS = {
    'A': {
        'name': 'Liver Only',
        'nodes': ['patient', 'liver', 'biomarker']
    },
    'B': {
        'name': 'Liver + Kidney',
        'nodes': ['patient', 'liver', 'kidney', 'biomarker']
    },
    'C': {
        'name': 'Liver + Heart',
        'nodes': ['patient', 'liver', 'heart', 'biomarker']
    },
    'D': {
        'name': 'Full 3-Organ (Liver + Kidney + Heart)',
        'nodes': ['patient', 'liver', 'kidney', 'heart', 'biomarker']
    }
}

def create_subgraph_for_config(g, active_nodes):
    sub_g = g.clone()

    # Remove node types not in active_nodes
    all_node_types = list(g.node_types)
    for ntype in all_node_types:
        if ntype not in active_nodes:
            del sub_g[ntype]

    # Remove edge types where src or dst is not in active_nodes
    all_edge_types = list(g.edge_types)
    for edge_type in all_edge_types:
        src, rel, dst = edge_type
        if src not in active_nodes or dst not in active_nodes:
            del sub_g[edge_type]

    return sub_g

def run_hsgin_ablation():
    print("==========================================================================")
    print("        RUNNING HSGIN-SPECIFIC ORGAN ABLATION STUDY (CONFIGS A - D)       ")
    print("==========================================================================")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    df = pd.read_csv(FINAL_COHORT_PATH)
    splits = get_5fold_splits(df, seed=42)

    CACHE_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\hsgin_ablation_cache.json"
    ablation_cache = {}
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, 'r') as f:
                ablation_cache = json.load(f)
            print(f"Loaded existing ablation cache from {CACHE_PATH}")
        except Exception as e:
            print(f"Could not load cache: {e}")

    print(f"Loading graphs from {GRAPH_PATH}...")
    full_graphs = torch.load(GRAPH_PATH)

    hsgin_ablation_results = {}

    for config_key, config_info in ABLATION_CONFIGS.items():
        c_name = config_info['name']
        active_nodes = config_info['nodes']
        print(f"\n>>> Running HSGIN Config {config_key}: {c_name} (Nodes: {active_nodes})")

        # Build subgraphs for this configuration
        sub_graphs = [create_subgraph_for_config(g, active_nodes) for g in full_graphs]

        in_dim_dict = {ntype: sub_graphs[0][ntype].x.shape[1] for ntype in sub_graphs[0].node_types}

        fold_maes, fold_rmses, fold_r2s = [], [], []
        fold_details = []

        cfg_cache = ablation_cache.get(config_key, {})

        for fold, (train_uids, val_uids) in enumerate(splits):
            fold_str = str(fold + 1)
            if fold_str in cfg_cache:
                metrics = cfg_cache[fold_str]
                print(f"  Fold {fold+1} [LOADED FROM CACHE] -> Val MAE: {metrics['mae']:.4f} | Val RMSE: {metrics['rmse']:.4f} | Val R²: {metrics['r2']:.4f}")
            else:
                tr_graphs, va_graphs = preprocess_fold_graphs(sub_graphs, train_uids, val_uids)

                metrics = train_hsgin_fold(
                    train_graphs=tr_graphs,
                    val_graphs=va_graphs,
                    in_dim_dict=in_dim_dict,
                    device=device,
                    epochs=50,
                    lr=0.001,
                    seed=42 + fold
                )
                if config_key not in ablation_cache:
                    ablation_cache[config_key] = {}
                ablation_cache[config_key][fold_str] = metrics
                with open(CACHE_PATH, 'w') as f:
                    json.dump(ablation_cache, f, indent=2)

                print(f"  Fold {fold+1} -> Val MAE: {metrics['mae']:.4f} | Val RMSE: {metrics['rmse']:.4f} | Val R²: {metrics['r2']:.4f}")

            fold_maes.append(metrics['mae'])
            fold_rmses.append(metrics['rmse'])
            fold_r2s.append(metrics['r2'])

            fold_details.append({
                'fold': fold + 1,
                'mae': metrics['mae'],
                'rmse': metrics['rmse'],
                'r2': metrics['r2']
            })

        hsgin_ablation_results[config_key] = {
            'config_name': c_name,
            'nodes': active_nodes,
            'mae_mean': float(np.mean(fold_maes)),
            'mae_std': float(np.std(fold_maes)),
            'rmse_mean': float(np.mean(fold_rmses)),
            'rmse_std': float(np.std(fold_rmses)),
            'r2_mean': float(np.mean(fold_r2s)),
            'r2_std': float(np.std(fold_r2s)),
            'folds': fold_details
        }

        print(f"  Config {config_key} Aggregate -> MAE: {np.mean(fold_maes):.4f}±{np.std(fold_maes):.4f} | RMSE: {np.mean(fold_rmses):.4f}±{np.std(fold_rmses):.4f} | R²: {np.mean(fold_r2s):.4f}±{np.std(fold_r2s):.4f}")

    # Compute relative deltas relative to Config A
    base_mae = hsgin_ablation_results['A']['mae_mean']
    base_rmse = hsgin_ablation_results['A']['rmse_mean']
    base_r2 = hsgin_ablation_results['A']['r2_mean']

    for cfg in ['A', 'B', 'C', 'D']:
        hsgin_ablation_results[cfg]['delta_mae'] = float(hsgin_ablation_results[cfg]['mae_mean'] - base_mae)
        hsgin_ablation_results[cfg]['delta_rmse'] = float(hsgin_ablation_results[cfg]['rmse_mean'] - base_rmse)
        hsgin_ablation_results[cfg]['delta_r2'] = float(hsgin_ablation_results[cfg]['r2_mean'] - base_r2)

    # Save to data/experiment_results.json (update hsgin_organ_ablation key)
    with open(RESULTS_PATH, 'r') as f:
        existing_results = json.load(f)

    existing_results['hsgin_organ_ablation'] = hsgin_ablation_results

    with open(RESULTS_PATH, 'w') as f:
        json.dump(existing_results, f, indent=2)

    print(f"\nSuccessfully updated {RESULTS_PATH} with 'hsgin_organ_ablation' results.")

    # Summary table output
    print("\n==========================================================================")
    print("                    HSGIN ORGAN ABLATION FINAL SUMMARY                    ")
    print("==========================================================================")
    print(f"{'Config':<8} | {'Description':<35} | {'MAE':<16} | {'RMSE':<16} | {'R²':<16} | {'ΔR² vs A':<10}")
    print("-" * 110)
    for cfg in ['A', 'B', 'C', 'D']:
        res = hsgin_ablation_results[cfg]
        mae_str = f"{res['mae_mean']:.4f}±{res['mae_std']:.4f}"
        rmse_str = f"{res['rmse_mean']:.4f}±{res['rmse_std']:.4f}"
        r2_str = f"{res['r2_mean']:.4f}±{res['r2_std']:.4f}"
        delta_str = f"{res['delta_r2']:+.4f}"
        print(f"Config {cfg:<1} | {res['config_name']:<35} | {mae_str:<16} | {rmse_str:<16} | {r2_str:<16} | {delta_str:<10}")

    return hsgin_ablation_results

if __name__ == "__main__":
    run_hsgin_ablation()
