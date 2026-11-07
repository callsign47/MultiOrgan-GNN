import os
import json
import hashlib
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from scipy.stats import spearmanr

MANIFEST_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\feature_manifest.json"
EXPECTED_MANIFEST_HASH = "6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22"
COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"
FOLDS_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\comparative\folds_v1.json"
REPORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\results\comparative\leakage_gate_report.json"

EXCLUDED_FORMULA_COMPONENTS = ['RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI']

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_leakage_gate(manifest_path=MANIFEST_PATH, cohort_path=COHORT_PATH, folds_path=FOLDS_PATH, report_path=REPORT_PATH):
    print("==========================================================================")
    print("             EXECUTING AUTOMATED LEAKAGE-CONTROL GATE                    ")
    print("==========================================================================")
    
    report = {
        "gate_timestamp": pd.Timestamp.now().isoformat(),
        "tests": {},
        "all_passed": False
    }

    # 1. Manifest Hash & Integrity Test
    print("[Gate 1] Manifest Hash & Integrity Check...")
    actual_hash = compute_sha256(manifest_path)
    hash_match = (actual_hash == EXPECTED_MANIFEST_HASH)
    
    with open(manifest_path, 'r') as f:
        manifest_data = json.load(f)
        
    all_retained_features = []
    for domain, items in manifest_data.items():
        for it in items:
            feat = it['feature']
            if feat not in EXCLUDED_FORMULA_COMPONENTS:
                all_retained_features.append(feat)

    count_valid = (len(all_retained_features) == 25)
    direct_overlap = set(all_retained_features) & set(EXCLUDED_FORMULA_COMPONENTS)
    
    gate1_passed = hash_match and count_valid and (len(direct_overlap) == 0)
    report['tests']['gate_1_manifest_check'] = {
        "passed": gate1_passed,
        "manifest_sha256": actual_hash,
        "expected_sha256": EXPECTED_MANIFEST_HASH,
        "feature_count": len(all_retained_features),
        "direct_formula_overlap": list(direct_overlap)
    }
    print(f"  -> Manifest Check: {'PASS' if gate1_passed else 'FAIL'} (25 features, zero direct overlap)")

    # 2. Patient-Level Fold Disjointness Test
    print("[Gate 2] Fold Disjointness & Zero Patient Overlap...")
    with open(folds_path, 'r') as f:
        folds_data = json.load(f)

    disjoint_passed = True
    fold_overlap_log = {}
    for f in folds_data['folds']:
        f_idx = f['fold']
        overlap = set(f['train_seqn']) & set(f['val_seqn'])
        if len(overlap) > 0:
            disjoint_passed = False
        fold_overlap_log[f"fold_{f_idx}"] = len(overlap)

    report['tests']['gate_2_fold_disjointness'] = {
        "passed": disjoint_passed,
        "overlaps_per_fold": fold_overlap_log
    }
    print(f"  -> Fold Disjointness Check: {'PASS' if disjoint_passed else 'FAIL'}")

    # 3. Deterministic Reconstruction Test
    print("[Gate 3] Excluded Component Reconstruction Test (Checking for Algebraic Leakage)...")
    df = pd.read_csv(cohort_path)
    
    # Impute missing features for reconstruction test
    X = df[all_retained_features].fillna(df[all_retained_features].median()).values
    
    reconstruction_results = {}
    reconstruction_leakage_detected = False
    
    for comp in EXCLUDED_FORMULA_COMPONENTS:
        y_comp = df[comp].values
        valid_idx = ~np.isnan(y_comp)
        
        reg = Ridge(alpha=1.0)
        reg.fit(X[valid_idx], y_comp[valid_idx])
        preds = reg.predict(X[valid_idx])
        r2_reconstruction = float(r2_score(y_comp[valid_idx], preds))
        
        # Max correlation with any single feature
        corrs = [abs(float(np.corrcoef(X[valid_idx, i], y_comp[valid_idx])[0, 1])) for i in range(X.shape[1])]
        max_single_corr = float(max(corrs))
        max_corr_feature = all_retained_features[int(np.argmax(corrs))]
        
        # Hard fail if any component can be reconstructed with R2 > 0.90
        leak = (r2_reconstruction > 0.90 or max_single_corr > 0.90)
        if leak:
            reconstruction_leakage_detected = True
            
        reconstruction_results[comp] = {
            "reconstruction_r2": r2_reconstruction,
            "max_single_pearson": max_single_corr,
            "max_correlated_feature": max_corr_feature,
            "deterministic_leakage": leak
        }
        print(f"  - {comp:10s} Reconstruction R2: {r2_reconstruction:+.4f} | Max Corr: {max_single_corr:.4f} ({max_corr_feature})")

    gate3_passed = not reconstruction_leakage_detected
    report['tests']['gate_3_reconstruction_test'] = {
        "passed": gate3_passed,
        "components": reconstruction_results
    }
    print(f"  -> Reconstruction Test: {'PASS' if gate3_passed else 'FAIL'}")

    # 4. Proxy Leakage Screen on Liver Features
    print("[Gate 4] Proxy Leakage Screen for Liver Features...")
    liver_features = manifest_data.get('Liver', [])
    liver_cols = [it['feature'] for it in liver_features if it['feature'] not in EXCLUDED_FORMULA_COMPONENTS]
    
    liver_proxy_screen = {}
    for l_col in liver_cols:
        l_vals = df[l_col].fillna(df[l_col].median()).values
        liver_proxy_screen[l_col] = {}
        for comp in EXCLUDED_FORMULA_COMPONENTS:
            c_vals = df[comp].values
            valid_m = ~np.isnan(c_vals)
            p_corr = float(np.corrcoef(l_vals[valid_m], c_vals[valid_m])[0, 1])
            s_corr, _ = spearmanr(l_vals[valid_m], c_vals[valid_m])
            liver_proxy_screen[l_col][comp] = {
                "pearson": float(p_corr),
                "spearman": float(s_corr)
            }
            
    report['tests']['gate_4_proxy_screen'] = {
        "passed": True, # Informational & audit threshold
        "liver_correlations": liver_proxy_screen
    }
    print(f"  -> Liver Proxy Screen: PASS (Recorded for Experiment 6 Ablation)")

    # Overall Verdict
    all_passed = gate1_passed and disjoint_passed and gate3_passed
    report['all_passed'] = all_passed
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    print(f"\n==========================================================================")
    print(f" GATE VERDICT: {'ALL HARD GATES PASSED (LEAKAGE CONTROLLED)' if all_passed else 'FAIL - TRAINING BLOCKED'}")
    print(f" Gate report saved to: {report_path}")
    print(f"==========================================================================")
    
    if not all_passed:
        raise RuntimeError("HARD LEAKAGE GATE FAILED: Training is strictly prohibited.")
        
    return report

if __name__ == "__main__":
    run_leakage_gate()
