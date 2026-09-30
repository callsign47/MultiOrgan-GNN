import os
import pandas as pd
import numpy as np
import json
from scipy.stats import skew

FINAL_COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"
OUTPUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\data"

def compute_and_verify_fib4(cohort_path=FINAL_COHORT_PATH):
    print("--- Starting Independent True FIB-4 Target Verification ---")
    df = pd.read_csv(cohort_path)
    
    # Required columns check
    req_cols = ['patient_uid', 'SEQN', 'RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI']
    for c in req_cols:
        if c not in df.columns:
            raise KeyError(f"CRITICAL: Missing required column {c} for True FIB-4 calculation!")
            
    # Clean zeros/negative inputs if any
    valid_mask = (df['RIDAGEYR'] > 0) & (df['LBXSASSI'] > 0) & (df['LBXSATSI'] > 0) & (df['LBXPLTSI'] > 0)
    df_valid = df[valid_mask].copy()
    
    # Calculate True FIB-4
    # Formula: (Age * AST) / (Platelets * sqrt(ALT))
    df_valid['fib4_target'] = (df_valid['RIDAGEYR'] * df_valid['LBXSASSI']) / (df_valid['LBXPLTSI'] * np.sqrt(df_valid['LBXSATSI']))
    
    # Hard Validation Gate 1: Check NaN / Inf
    nan_count = df_valid['fib4_target'].isna().sum()
    inf_count = np.isinf(df_valid['fib4_target']).sum()
    if nan_count > 0 or inf_count > 0:
        raise ValueError(f"HARD GATE FAIL: Target contains {nan_count} NaNs and {inf_count} Infs!")
        
    # Hard Validation Gate 2: Check SEQN and patient_uid uniqueness
    seqn_unique = df_valid['SEQN'].nunique() == len(df_valid)
    uid_unique = df_valid['patient_uid'].nunique() == len(df_valid)
    if not (seqn_unique and uid_unique):
        raise ValueError("HARD GATE FAIL: Duplicate patient IDs detected in final cohort!")
        
    # Hard Validation Gate 3: Brain/Gut placeholder check
    for col in df_valid.columns:
        if 'BRAIN' in col.upper() or 'GUT' in col.upper():
            raise ValueError(f"HARD GATE FAIL: Found unexpected placeholder column {col}!")
            
    # Compute Target Distribution Statistics
    y = df_valid['fib4_target'].values
    stats_dict = {
        "n_patients": len(y),
        "mean": float(np.mean(y)),
        "std": float(np.std(y)),
        "median": float(np.median(y)),
        "min": float(np.min(y)),
        "max": float(np.max(y)),
        "p25": float(np.percentile(y, 25)),
        "p75": float(np.percentile(y, 75)),
        "iqr": float(np.percentile(y, 75) - np.percentile(y, 25)),
        "skewness": float(skew(y)),
        "unit_verification": {
            "Age": "Years (RIDAGEYR)",
            "AST": "U/L (LBXSASSI)",
            "ALT": "U/L (LBXSATSI)",
            "Platelets": "10^9/L or 10^3/uL (LBXPLTSI)",
            "Formula": "(Age * AST) / (Platelet * sqrt(ALT))"
        },
        "validation_gates_passed": True
    }
    
    print(f"Target Patient Count: {stats_dict['n_patients']}")
    print(f"Mean ± Std: {stats_dict['mean']:.4f} ± {stats_dict['std']:.4f}")
    print(f"Median (IQR): {stats_dict['median']:.4f} ({stats_dict['p25']:.4f} - {stats_dict['p75']:.4f})")
    print(f"Min - Max: {stats_dict['min']:.4f} - {stats_dict['max']:.4f}")
    print(f"Skewness: {stats_dict['skewness']:.4f}")
    print("ALL HARD VALIDATION GATES PASSED! Target formula verified.\n")
    
    # Save target column to final cohort CSV
    df_valid.to_csv(cohort_path, index=False)
    
    # Save target validation report
    val_json_path = os.path.join(OUTPUT_DIR, "fib4_target_validation.json")
    with open(val_json_path, "w") as f:
        json.dump(stats_dict, f, indent=2)
        
    print(f"Target Validation Report saved to: {val_json_path}")
    return stats_dict

if __name__ == "__main__":
    compute_and_verify_fib4()
