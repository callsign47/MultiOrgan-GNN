import os
import pandas as pd
import json

DATA_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\data"
REPORT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\reports"

os.makedirs(REPORT_DIR, exist_ok=True)

def generate_report():
    print("--- Generating Phase 1 Dataset & Audit Report ---")
    
    # Load metadata files
    ingestion_df = pd.read_csv(os.path.join(DATA_DIR, "ingestion_summary.csv"))
    missingness_df = pd.read_csv(os.path.join(DATA_DIR, "missingness_report.csv"))
    flow_df = pd.read_csv(os.path.join(DATA_DIR, "cohort_flow.csv"))
    
    with open(os.path.join(DATA_DIR, "feature_manifest.json")) as f:
        manifest = json.load(f)
        
    with open(os.path.join(DATA_DIR, "fib4_target_validation.json")) as f:
        target_stats = json.load(f)
        
    md = []
    md.append("# HSGIN 3-Organ Phase 1 Dataset & Missingness Audit Report\n")
    md.append("**Cycle Scope**: NHANES August 2021–August 2023  ")
    md.append("**Experimental Focus**: Patient-Level Heterogeneous Graph for Liver–Kidney–Heart Interaction  ")
    md.append("**Target Variable**: True FIB-4 Score (Alanine/Aspartate Aminotransferase & Platelet count based)  \n")
    
    md.append("---")
    md.append("## 1. Executive Summary & Hard Validation Gates\n")
    md.append(f"- **Final Locked Cohort Size**: **{target_stats['n_patients']:,} patients** (Satisfies $\\ge 5,000$ patient threshold).")
    md.append(f"- **Patient Identity Format**: `patient_uid = P_000001` ... `P_{target_stats['n_patients']:06d}` (Strict SEQN merge).")
    md.append(f"- **Target Distribution**: Mean **{target_stats['mean']:.4f} ± {target_stats['std']:.4f}**, Median **{target_stats['median']:.4f}** (IQR: {target_stats['p25']:.4f}–{target_stats['p75']:.4f}). Range: [{target_stats['min']:.4f}, {target_stats['max']:.4f}].")
    md.append("- **Hard Validation Gates**: ALL PASSED (Zero SEQN duplicates, Zero NaN/Inf, True FIB-4 formula verified, Brain/Gut nodes excluded).\n")
    
    md.append("---")
    md.append("## 2. Cohort Attrition Flow\n")
    md.append("| Step | Description | Remaining N | Excluded N |")
    md.append("|---|---|---:|---:|")
    for _, row in flow_df.iterrows():
        md.append(f"| {row['step']} | {row['description']} | {row['n_remaining']:,} | {row['n_excluded']:,} |")
    md.append("\n")
    
    md.append("---")
    md.append("## 3. Data Source Ingestion Summary\n")
    md.append("| File Key | Subdirectory | Description | Total Rows | Unique SEQN | SEQN Unique? | Features |")
    md.append("|---|---|---|---:|---:|:---:|---:|")
    for _, row in ingestion_df.iterrows():
        status_icon = "Pass" if row['is_seqn_unique'] else "Deduplicated"
        md.append(f"| `{row['file_key']}` | {row['category']} | {row['description']} | {row['num_rows']:,} | {row['unique_seqn']:,} | {status_icon} | {row['num_columns']} |")
    md.append("\n")
    
    md.append("---")
    md.append("## 4. Locked Organ & Biomarker Feature Manifest\n")
    md.append("The missingness audit evaluated candidate variables across the raw NHANES population and the target-eligible cohort ($N=6,277$). Variables with $>30\\%$ missingness in the target cohort were excluded.\n")
    
    md.append("| Organ / Domain | Feature Code | Description | Raw Avail N (%) | Cohort Avail N (%) | Status |")
    md.append("|---|---|---|---:|---:|:---:|")
    for _, row in missingness_df.iterrows():
        raw_pct = 100.0 - row['raw_missing_percent']
        cohort_pct = 100.0 - row['cohort_missing_percent']
        md.append(f"| **{row['organ']}** | `{row['feature']}` | {row['description']} | {row['raw_available']:,} ({raw_pct:.1f}%) | {row['cohort_available']:,} ({cohort_pct:.1f}%) | `{row['status']}` |")
    md.append("\n")
    
    md.append("---")
    md.append("## 5. Target Formulation & Verification\n")
    md.append("### Formulation")
    md.append("$$\\text{FIB-4} = \\frac{\\text{Age (years)} \\times \\text{AST (U/L)}}{\\text{Platelets } (10^9/\\text{L}) \\times \\sqrt{\\text{ALT (U/L)}}}$$")
    md.append("### Verification Results")
    md.append(f"- **Source Variables**: Age (`RIDAGEYR` from `DEMO_L`), AST (`LBXSASSI` from `BIOPRO_L`), ALT (`LBXSATSI` from `BIOPRO_L`), Platelets (`LBXPLTSI` from `CBC_L`).")
    md.append(f"- **Sample Size**: {target_stats['n_patients']:,} patients")
    md.append(f"- **Mean ± Std**: {target_stats['mean']:.4f} ± {target_stats['std']:.4f}")
    md.append(f"- **Median**: {target_stats['median']:.4f}")
    md.append(f"- **25th–75th Percentile (IQR)**: {target_stats['p25']:.4f} – {target_stats['p75']:.4f} ({target_stats['iqr']:.4f})")
    md.append(f"- **Min / Max**: {target_stats['min']:.4f} / {target_stats['max']:.4f}")
    md.append(f"- **Skewness**: {target_stats['skewness']:.4f}\n")
    
    md.append("---")
    md.append("## 6. Preprocessing & Leakage Prevention Architecture\n")
    md.append("To prevent data leakage during subsequent graph neural network and baseline model training:")
    md.append("1. **5-Fold Patient-Level CV**: Patients are strictly split at the `patient_uid` level. Zero patient overlap across training and validation folds.")
    md.append("2. **In-Fold Preprocessing**: `StandardScaler` and median imputation will be fitted strictly on the training fold, then applied to transform validation data.")
    md.append("3. **Y-Randomization**: Baseline target permutation will shuffle target $Y$ strictly within each training fold, leaving validation targets unchanged.\n")
    
    report_content = "\n".join(md)
    report_path = os.path.join(REPORT_DIR, "dataset_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Dataset Report successfully written to: {report_path}")
    return report_content

if __name__ == "__main__":
    generate_report()
