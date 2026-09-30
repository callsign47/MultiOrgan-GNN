import os
import pandas as pd
import numpy as np
import json

MASTER_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\master_patient.csv"
OUTPUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\data"

# Comprehensive feature mapping aligned with PRD Sections 5 & 6
CANDIDATE_MAP = {
    "Demographics": {
        "RIDAGEYR": "Age in years",
        "RIAGENDR": "Gender (1=Male, 2=Female)"
    },
    "Liver": {
        "LBXSATSI": "Alanine Aminotransferase ALT (U/L)",
        "LBXSASSI": "Aspartate Aminotransferase AST (U/L)",
        "LBXSGTSI": "Gamma Glutamyl Transferase GGT (U/L)",
        "LBXSAL": "Albumin (g/dL)",
        "LBXSTB": "Total Bilirubin (mg/dL)",
        "LBXSAPSI": "Alkaline Phosphatase ALP (U/L)",
        "LUXSMED": "Liver Stiffness Median (kPa)",
        "LUXCAPM": "Controlled Attenuation Parameter CAP (dB/m)"
    },
    "Kidney": {
        "LBXSCR": "Serum Creatinine (mg/dL)",
        "LBXSBU": "Blood Urea Nitrogen BUN (mg/dL)",
        "LBXSUA": "Uric Acid (mg/dL)",
        "URXUMA": "Urine Albumin (ug/mL)",
        "URXUCR": "Urine Creatinine (mg/dL)",
        "KIQ022": "Ever told had kidney failure/disease (1=Yes, 2=No)"
    },
    "Heart": {
        "BPXOSY1": "Systolic Blood Pressure Reading 1 (mmHg)",
        "BPXODI1": "Diastolic Blood Pressure Reading 1 (mmHg)",
        "BPXOPLS1": "Pulse Reading 1 (bpm)",
        "LBDHDD": "Direct HDL Cholesterol (mg/dL)",
        "LBXTC": "Total Cholesterol (mg/dL)",
        "BPQ020": "Ever told had high blood pressure (1=Yes, 2=No)",
        "MCQ160C": "Ever told had coronary heart disease (1=Yes, 2=No)",
        "MCQ160E": "Ever told had heart attack (1=Yes, 2=No)"
    },
    "Biomarker": {
        "LBXWBCSI": "White Blood Cell count (10^9/L)",
        "LBXRBCSI": "Red Blood Cell count (10^12/L)",
        "LBXHGB": "Hemoglobin (g/dL)",
        "LBXPLTSI": "Platelet Count (10^9/L)",
        "LBXHSCRP": "High-sensitivity C-Reactive Protein hs-CRP (mg/L)"
    }
}

def audit_features(master_path=MASTER_PATH):
    print("--- Starting Comprehensive Feature Missingness & Availability Audit ---")
    df = pd.read_csv(master_path)
    total_raw_patients = len(df)
    
    # Define target cohort (valid FIB-4 inputs: Age, AST, ALT, Platelets)
    target_cohort = df.dropna(subset=['RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI']).copy()
    target_cohort = target_cohort[(target_cohort['LBXSATSI'] > 0) & (target_cohort['LBXPLTSI'] > 0)]
    total_target_patients = len(target_cohort)
    
    print(f"Total Raw NHANES Participants: {total_raw_patients}")
    print(f"Total Target-Eligible Participants (FIB-4 complete): {total_target_patients}\n")
    
    audit_rows = []
    locked_manifest = {}
    
    for organ, feature_dict in CANDIDATE_MAP.items():
        locked_manifest[organ] = []
        for feat, desc in feature_dict.items():
            # Raw stats
            raw_avail = df[feat].notna().sum() if feat in df.columns else 0
            raw_missing_pct = (1.0 - raw_avail / total_raw_patients) * 100.0
            
            # Target cohort stats
            cohort_avail = target_cohort[feat].notna().sum() if feat in target_cohort.columns else 0
            cohort_missing_pct = (1.0 - cohort_avail / total_target_patients) * 100.0
            
            # Retention rule: Cohort missingness <= 30%
            is_retained = (cohort_missing_pct <= 30.0)
            status = "RETAINED" if is_retained else "EXCLUDED (>30% missing in target cohort)"
            
            if is_retained:
                locked_manifest[organ].append({
                    "feature": feat,
                    "description": desc,
                    "cohort_missing_pct": round(cohort_missing_pct, 2),
                    "raw_missing_pct": round(raw_missing_pct, 2)
                })
                
            audit_rows.append({
                "organ": organ,
                "feature": feat,
                "description": desc,
                "raw_total": total_raw_patients,
                "raw_available": raw_avail,
                "raw_missing_percent": round(raw_missing_pct, 2),
                "cohort_total": total_target_patients,
                "cohort_available": cohort_avail,
                "cohort_missing_percent": round(cohort_missing_pct, 2),
                "status": status
            })
            
            print(f"[{organ:<10}] {feat:<10} | Raw Avail: {raw_avail:5d} ({100-raw_missing_pct:5.1f}%) | Cohort Avail: {cohort_avail:5d} ({100-cohort_missing_pct:5.1f}%) | Status: {status}")
            
    audit_df = pd.DataFrame(audit_rows)
    audit_csv_path = os.path.join(OUTPUT_DIR, "missingness_report.csv")
    audit_df.to_csv(audit_csv_path, index=False)
    
    manifest_path = os.path.join(OUTPUT_DIR, "feature_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(locked_manifest, f, indent=2)
        
    print(f"\nMissingness Audit Completed!")
    print(f"Audit Report saved to: {audit_csv_path}")
    print(f"Locked Feature Manifest saved to: {manifest_path}")
    
    return audit_df, locked_manifest

if __name__ == "__main__":
    audit_features()
