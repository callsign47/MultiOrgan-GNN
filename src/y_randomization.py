import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from src.pipeline import get_leak_free_feature_list, get_5fold_splits, preprocess_fold_tabular

FINAL_COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"

def run_in_fold_y_randomization(cohort_path=FINAL_COHORT_PATH, seed=42):
    print("--- Executing In-Fold Target Y-Randomization Validation ---")
    df = pd.read_csv(cohort_path)
    feature_cols = get_leak_free_feature_list()
    splits = get_5fold_splits(df)
    
    fold_maes, fold_rmses, fold_r2s = [], [], []
    
    for fold, (train_uids, val_uids) in enumerate(splits):
        X_train, y_train, X_val, y_val, _, _ = preprocess_fold_tabular(df, train_uids, val_uids, feature_cols)
        
        # PERMUTE Y STRICTLY WITHIN TRAINING FOLD ONLY
        np.random.seed(seed + fold)
        y_train_shuffled = np.random.permutation(y_train)
        
        model = XGBRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=42)
        model.fit(X_train, y_train_shuffled)
        
        # Evaluate on UNTOUCHED true validation target y_val
        preds = model.predict(X_val)
        
        mae = mean_absolute_error(y_val, preds)
        rmse = root_mean_squared_error(y_val, preds)
        r2 = r2_score(y_val, preds)
        
        fold_maes.append(mae)
        fold_rmses.append(rmse)
        fold_r2s.append(r2)
        print(f"  Fold {fold+1} (Y-Permuted Train) -> Val MAE: {mae:.4f} | Val RMSE: {rmse:.4f} | Val R²: {r2:.4f}")
        
    mean_mae, std_mae = np.mean(fold_maes), np.std(fold_maes)
    mean_rmse, std_rmse = np.mean(fold_rmses), np.std(fold_rmses)
    mean_r2, std_r2 = np.mean(fold_r2s), np.std(fold_r2s)
    
    results = {
        'mae_mean': float(mean_mae), 'mae_std': float(std_mae),
        'rmse_mean': float(mean_rmse), 'rmse_std': float(std_rmse),
        'r2_mean': float(mean_r2), 'r2_std': float(std_r2)
    }
    
    print(f"\nIn-Fold Y-Randomization Aggregate Results:")
    print(f"  MAE: {mean_mae:.4f} ± {std_mae:.4f}")
    print(f"  RMSE: {mean_rmse:.4f} ± {std_rmse:.4f}")
    print(f"  R²: {mean_r2:.4f} ± {std_r2:.4f}")
    if mean_r2 <= 0.05:
        print("  -> SANITY CHECK PASSED: R² ~ 0 under Y-randomization proves zero target leakage!")
    else:
        print("  -> WARNING: Unexpected positive R² under Y-randomization.")
        
    return results

if __name__ == "__main__":
    run_in_fold_y_randomization()
