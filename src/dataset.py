import os
import pandas as pd
import json

def get_data_dir():
    # Check inside workspace first, then parent
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(workspace_dir, "NHANES AUG'21 - AUG'23"),
        os.path.join(os.path.dirname(workspace_dir), "NHANES AUG'21 - AUG'23"),
        r"C:\Users\admin_fix\Downloads\3 ORGAN\NHANES AUG'21 - AUG'23",
        r"C:\Users\admin_fix\Downloads\NHANES AUG'21 - AUG'23"
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError("Could not locate NHANES AUG'21 - AUG'23 directory.")

DATA_DIR = get_data_dir()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of target files across subdirectories
FILE_MAPPING = {
    "DEMO_L": ("DEMO G", "Demographics"),
    "BIOPRO_L": ("LABORATORY", "Biochemistry Profile"),
    "CBC_L": ("LABORATORY", "Complete Blood Count"),
    "ALB_CR_L": ("LABORATORY", "Albumin & Creatinine - Urine"),
    "HDL_L": ("LABORATORY", "HDL Cholesterol"),
    "TRIGLY_L": ("LABORATORY", "Triglycerides"),
    "TCHOL_L": ("LABORATORY", "Total Cholesterol"),
    "HSCRP_L": ("LABORATORY", "High-Sensitivity C-Reactive Protein"),
    "GLU_L": ("LABORATORY", "Fasting Glucose"),
    "INS_L": ("LABORATORY", "Insulin"),
    "GHB_L": ("LABORATORY", "Glycohemoglobin"),
    "HEPA_L": ("LABORATORY", "Hepatitis A"),
    "HEPBD_L": ("LABORATORY", "Hepatitis B Surface/Core Antibody"),
    "HEPC_L": ("LABORATORY", "Hepatitis C"),
    "HEPE_L": ("LABORATORY", "Hepatitis E"),
    "BMX_L": ("EXAMINATION", "Body Measures"),
    "BPXO_L": ("EXAMINATION", "Blood Pressure - Oscillometric"),
    "LUX_L": ("EXAMINATION", "Liver Ultrasound Elastography"),
    "BPQ_L": ("QUESTIONNAIRE", "Blood Pressure Questionnaire"),
    "KIQ_U_L": ("QUESTIONNAIRE", "Kidney Conditions Questionnaire"),
    "MCQ_L": ("QUESTIONNAIRE", "Medical Conditions Questionnaire"),
    "DIQ_L": ("QUESTIONNAIRE", "Diabetes Questionnaire"),
    "HEQ_L": ("QUESTIONNAIRE", "Hepatitis Questionnaire"),
    "FNQ_L": ("QUESTIONNAIRE", "Functioning Questionnaire"),
    "DPQ_L": ("QUESTIONNAIRE", "Depression Screening Questionnaire"),
    "SLQ_L": ("QUESTIONNAIRE", "Sleep Disorders Questionnaire"),
    "DBQ_L": ("QUESTIONNAIRE", "Diet Behavior Questionnaire"),
}

def load_all_datasets(data_dir=None):
    if data_dir is None:
        data_dir = get_data_dir()
        
    print(f"--- Starting Data Ingestion & SEQN Verification ---")
    print(f"Data Source Directory: {data_dir}")
    
    merged_df = None
    file_stats = []
    
    for file_key, (subdir, desc) in FILE_MAPPING.items():
        file_path = os.path.join(data_dir, subdir, f"{file_key}.xpt")
        if not os.path.exists(file_path):
            print(f"WARNING: File not found: {file_path}")
            continue
        
        try:
            df = pd.read_sas(file_path, format='xport')
            # Normalize column names to uppercase
            df.columns = [c.upper() for c in df.columns]
            
            if 'SEQN' not in df.columns:
                raise ValueError(f"CRITICAL: SEQN column missing in {file_key}")
            
            num_rows = len(df)
            num_unique_seqn = df['SEQN'].nunique()
            is_unique = (num_rows == num_unique_seqn)
            
            file_stats.append({
                "file_key": file_key,
                "description": desc,
                "category": subdir,
                "num_rows": num_rows,
                "unique_seqn": num_unique_seqn,
                "is_seqn_unique": is_unique,
                "num_columns": len(df.columns)
            })
            
            if not is_unique:
                print(f"WARNING: Duplicate SEQN detected in {file_key}! Deduplicating...")
                df = df.drop_duplicates(subset=['SEQN'], keep='first')
            
            if merged_df is None:
                merged_df = df
            else:
                cols_to_use = [c for c in df.columns if c == 'SEQN' or c not in merged_df.columns]
                merged_df = pd.merge(merged_df, df[cols_to_use], on='SEQN', how='outer')
                
            print(f"Loaded {file_key:<10} | Rows: {num_rows:<6} | Unique SEQN: {num_unique_seqn:<6} | Cols: {len(df.columns)}")
            
        except Exception as e:
            print(f"ERROR reading {file_key}: {e}")
            
    stats_df = pd.DataFrame(file_stats)
    stats_df.to_csv(os.path.join(OUTPUT_DIR, "ingestion_summary.csv"), index=False)
    
    merged_df = merged_df.sort_values(by='SEQN').reset_index(drop=True)
    master_path = os.path.join(OUTPUT_DIR, "master_patient.csv")
    merged_df.to_csv(master_path, index=False)
    
    print(f"\nMaster Patient Table Created Successfully!")
    print(f"Total Unique SEQN Patients: {len(merged_df)}")
    print(f"Total Combined Features: {len(merged_df.columns)}")
    print(f"Saved to: {master_path}")
    
    return merged_df, stats_df

if __name__ == "__main__":
    load_all_datasets()
