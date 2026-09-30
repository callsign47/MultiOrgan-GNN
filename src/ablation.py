import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from src.pipeline import FEATURE_DOMAINS, get_5fold_splits, preprocess_fold_tabular

FINAL_COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"

ABLATION_CONFIGS = {
    'A_Liver_Only': FEATURE_DOMAINS['Liver'],
    'B_Liver_Kidney': FEATURE_DOMAINS['Liver'] + FEATURE_DOMAINS['Kidney'],
    'C_Liver_Heart': FEATURE_DOMAINS['Liver'] + FEATURE_DOMAINS['Heart'],
    'D_Full_3Organ': (
        FEATURE_DOMAINS['Demographics'] +
        FEATURE_DOMAINS['Liver'] +
        FEATURE_DOMAINS['Kidney'] +
        FEATURE_DOMAINS['Heart'] +
        FEATURE_DOMAINS['Biomarker']
    )
}

def run_organ_ablation_study(cohort_path=FINAL_COHORT_PATH):
    print("--- Running A–D Organ Ablation Study (5-Fold CV) ---")
    df = pd.read_csv(cohort_path)
    splits = get_5fold_splits(df)
    
    results = {}
    
    for config_name, feature_cols in ABLATION_CONFIGS.items():
        print(f"\nEvaluating {config_name} ({len(feature_cols)} features)...")
        fold_maes, fold_rmses, fold_r2s = [], [], []
        
        for fold, (train_uids, val_uids) in enumerate(splits):
            X_train, y_train, X_val, y_val, _, _ = preprocess_fold_tabular(df, train_uids, val_uids, feature_cols)
            
            model = XGBRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_val)
            
            mae = mean_absolute_error(y_val, preds)
            rmse = root_mean_squared_error(y_val, preds)
            r2 = r2_score(y_val, preds)
            
            fold_maes.append(mae)
            fold_rmses.append(rmse)
            fold_r2s.append(r2)
            
        mean_mae, std_mae = np.mean(fold_maes), np.std(fold_maes)
        mean_rmse, std_rmse = np.mean(fold_rmses), np.std(fold_rmses)
        mean_r2, std_r2 = np.mean(fold_r2s), np.std(fold_r2s)
        
        results[config_name] = {
            'mae_mean': float(mean_mae), 'mae_std': float(std_mae),
            'rmse_mean': float(mean_rmse), 'rmse_std': float(std_rmse),
            'r2_mean': float(mean_r2), 'r2_std': float(std_r2)
        }
        print(f"  {config_name} -> MAE: {mean_mae:.4f}±{std_mae:.4f} | RMSE: {mean_rmse:.4f}±{std_rmse:.4f} | R²: {mean_r2:.4f}±{std_r2:.4f}")
        
    # Calculate Deltas vs Liver-Only Baseline (A_Liver_Only)
    baseline = results['A_Liver_Only']
    deltas = {}
    for config_name, res in results.items():
        delta_mae = res['mae_mean'] - baseline['mae_mean']
        delta_rmse = res['rmse_mean'] - baseline['rmse_mean']
        delta_r2 = res['r2_mean'] - baseline['r2_mean']
        
        deltas[config_name] = {
            'delta_mae': float(delta_mae),
            'delta_rmse': float(delta_rmse),
            'delta_r2': float(delta_r2)
        }
        res['deltas_vs_liver_only'] = deltas[config_name]
        
    return results

if __name__ == "__main__":
    run_organ_ablation_study()
