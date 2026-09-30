import os
import pandas as pd
import numpy as np
import json

MASTER_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\master_patient.csv"
OUTPUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\data"

def build_cohort_flow(master_path=MASTER_PATH):
    print("--- Starting Cohort Selection & Flow Construction ---")
    df = pd.read_csv(master_path)
    
    flow_steps = []
    
    # 1. Initial participants
    n0 = len(df)
    flow_steps.append({"step": 1, "description": "Initial NHANES August 2021–August 2023 Participants", "n_remaining": n0, "n_excluded": 0})
    
    # 2. Demographic availability (Age & Gender)
    df1 = df.dropna(subset=['RIDAGEYR', 'RIAGENDR'])
    n1 = len(df1)
    flow_steps.append({"step": 2, "description": "Demographic availability (Age & Gender complete)", "n_remaining": n1, "n_excluded": n0 - n1})
    
    # 3. Target requirement 1: Liver enzymes (ALT, AST complete & >0)
    df2 = df1.dropna(subset=['LBXSATSI', 'LBXSASSI'])
    df2 = df2[(df2['LBXSATSI'] > 0) & (df2['LBXSASSI'] > 0)]
    n2 = len(df2)
    flow_steps.append({"step": 3, "description": "Liver enzymes availability (ALT & AST complete & >0)", "n_remaining": n2, "n_excluded": n1 - n2})
    
    # 4. Target requirement 2: Complete blood count (Platelet count complete & >0)
    df3 = df2.dropna(subset=['LBXPLTSI'])
    df3 = df3[df3['LBXPLTSI'] > 0]
    n3 = len(df3)
    flow_steps.append({"step": 4, "description": "Platelet count availability (LBXPLTSI complete & >0)", "n_remaining": n3, "n_excluded": n2 - n3})
    
    # 5. Kidney biomarker availability (Serum Creatinine & BUN complete)
    df4 = df3.dropna(subset=['LBXSCR', 'LBXSBU'])
    n4 = len(df4)
    flow_steps.append({"step": 5, "description": "Kidney baseline availability (Serum Creatinine & BUN complete)", "n_remaining": n4, "n_excluded": n3 - n4})
    
    # 6. Cardiovascular lipid availability (HDL & Total Cholesterol complete)
    df5 = df4.dropna(subset=['LBDHDD', 'LBXTC'])
    n5 = len(df5)
    flow_steps.append({"step": 6, "description": "Cardiovascular baseline availability (HDL & Total Cholesterol complete)", "n_remaining": n5, "n_excluded": n4 - n5})
    
    # Final Cohort Locking
    final_df = df5.copy().reset_index(drop=True)
    
    # Generate patient_uid = P_000001 ... P_006279
    final_df['patient_uid'] = [f"P_{i+1:06d}" for i in range(len(final_df))]
    
    # Move patient_uid to first column
    cols = ['patient_uid', 'SEQN'] + [c for c in final_df.columns if c not in ['patient_uid', 'SEQN']]
    final_df = final_df[cols]
    
    n_final = len(final_df)
    
    # Soft Threshold Check (<5000 warning)
    if n_final < 5000:
        print(f"WARNING: Final cohort size ({n_final}) is below the recommended 5,000 threshold!")
    else:
        print(f"SUCCESS: Final cohort size ({n_final}) satisfies the 5,000 patient threshold!")
        
    flow_df = pd.DataFrame(flow_steps)
    flow_csv_path = os.path.join(OUTPUT_DIR, "cohort_flow.csv")
    flow_df.to_csv(flow_csv_path, index=False)
    
    final_cohort_path = os.path.join(OUTPUT_DIR, "final_cohort.csv")
    final_df.to_csv(final_cohort_path, index=False)
    
    print(f"\nCohort Flow Construction Completed!")
    print(f"Cohort Flow Report saved to: {flow_csv_path}")
    print(f"Final Locked Cohort ({n_final} patients) saved to: {final_cohort_path}")
    
    return final_df, flow_df

if __name__ == "__main__":
    build_cohort_flow()
