# HSGIN 3-Organ Phase 1 Dataset & Missingness Audit Report

**Cycle Scope**: NHANES August 2021–August 2023  
**Experimental Focus**: Patient-Level Heterogeneous Graph for Liver–Kidney–Heart Interaction  
**Target Variable**: True FIB-4 Score (Alanine/Aspartate Aminotransferase & Platelet count based)  

---
## 1. Executive Summary & Hard Validation Gates

- **Final Locked Cohort Size**: **6,277 patients** (Satisfies $\ge 5,000$ patient threshold).
- **Patient Identity Format**: `patient_uid = P_000001` ... `P_006277` (Strict SEQN merge).
- **Target Distribution**: Mean **1.0590 ± 0.7748**, Median **0.9028** (IQR: 0.5091–1.4023). Range: [0.0634, 13.9971].
- **Hard Validation Gates**: ALL PASSED (Zero SEQN duplicates, Zero NaN/Inf, True FIB-4 formula verified, Brain/Gut nodes excluded).

---
## 2. Cohort Attrition Flow

| Step | Description | Remaining N | Excluded N |
|---|---|---:|---:|
| 1 | Initial NHANES August 2021–August 2023 Participants | 11,933 | 0 |
| 2 | Demographic availability (Age & Gender complete) | 11,933 | 0 |
| 3 | Liver enzymes availability (ALT & AST complete & >0) | 6,308 | 5,625 |
| 4 | Platelet count availability (LBXPLTSI complete & >0) | 6,282 | 26 |
| 5 | Kidney baseline availability (Serum Creatinine & BUN complete) | 6,277 | 5 |
| 6 | Cardiovascular baseline availability (HDL & Total Cholesterol complete) | 6,277 | 0 |


---
## 3. Data Source Ingestion Summary

| File Key | Subdirectory | Description | Total Rows | Unique SEQN | SEQN Unique? | Features |
|---|---|---|---:|---:|:---:|---:|
| `DEMO_L` | DEMO G | Demographics | 11,933 | 11,933 | Pass | 27 |
| `BIOPRO_L` | LABORATORY | Biochemistry Profile | 7,199 | 7,199 | Pass | 42 |
| `CBC_L` | LABORATORY | Complete Blood Count | 8,727 | 8,727 | Pass | 23 |
| `ALB_CR_L` | LABORATORY | Albumin & Creatinine - Urine | 8,493 | 8,493 | Pass | 8 |
| `HDL_L` | LABORATORY | HDL Cholesterol | 8,068 | 8,068 | Pass | 4 |
| `TRIGLY_L` | LABORATORY | Triglycerides | 3,996 | 3,996 | Pass | 10 |
| `TCHOL_L` | LABORATORY | Total Cholesterol | 8,068 | 8,068 | Pass | 4 |
| `HSCRP_L` | LABORATORY | High-Sensitivity C-Reactive Protein | 8,727 | 8,727 | Pass | 4 |
| `GLU_L` | LABORATORY | Fasting Glucose | 3,996 | 3,996 | Pass | 4 |
| `INS_L` | LABORATORY | Insulin | 3,996 | 3,996 | Pass | 5 |
| `GHB_L` | LABORATORY | Glycohemoglobin | 7,199 | 7,199 | Pass | 3 |
| `HEPA_L` | LABORATORY | Hepatitis A | 8,611 | 8,611 | Pass | 3 |
| `HEPBD_L` | LABORATORY | Hepatitis B Surface/Core Antibody | 8,068 | 8,068 | Pass | 5 |
| `HEPC_L` | LABORATORY | Hepatitis C | 8,068 | 8,068 | Pass | 5 |
| `HEPE_L` | LABORATORY | Hepatitis E | 8,068 | 8,068 | Pass | 4 |
| `BMX_L` | EXAMINATION | Body Measures | 8,860 | 8,860 | Pass | 22 |
| `BPXO_L` | EXAMINATION | Blood Pressure - Oscillometric | 7,801 | 7,801 | Pass | 12 |
| `LUX_L` | EXAMINATION | Liver Ultrasound Elastography | 7,199 | 7,199 | Pass | 13 |
| `BPQ_L` | QUESTIONNAIRE | Blood Pressure Questionnaire | 8,501 | 8,501 | Pass | 6 |
| `KIQ_U_L` | QUESTIONNAIRE | Kidney Conditions Questionnaire | 7,809 | 7,809 | Pass | 9 |
| `MCQ_L` | QUESTIONNAIRE | Medical Conditions Questionnaire | 11,744 | 11,744 | Pass | 35 |
| `DIQ_L` | QUESTIONNAIRE | Diabetes Questionnaire | 11,744 | 11,744 | Pass | 9 |
| `HEQ_L` | QUESTIONNAIRE | Hepatitis Questionnaire | 10,696 | 10,696 | Pass | 2 |
| `FNQ_L` | QUESTIONNAIRE | Functioning Questionnaire | 10,942 | 10,942 | Pass | 32 |
| `DPQ_L` | QUESTIONNAIRE | Depression Screening Questionnaire | 6,337 | 6,337 | Pass | 11 |
| `SLQ_L` | QUESTIONNAIRE | Sleep Disorders Questionnaire | 8,501 | 8,501 | Pass | 7 |
| `DBQ_L` | QUESTIONNAIRE | Diet Behavior Questionnaire | 11,933 | 11,933 | Pass | 27 |


---
## 4. Locked Organ & Biomarker Feature Manifest

The missingness audit evaluated candidate variables across the raw NHANES population and the target-eligible cohort ($N=6,277$). Variables with $>30\%$ missingness in the target cohort were excluded.

| Organ / Domain | Feature Code | Description | Raw Avail N (%) | Cohort Avail N (%) | Status |
|---|---|---|---:|---:|:---:|
| **Demographics** | `RIDAGEYR` | Age in years | 11,933 (100.0%) | 6,282 (100.0%) | `RETAINED` |
| **Demographics** | `RIAGENDR` | Gender (1=Male, 2=Female) | 11,933 (100.0%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LBXSATSI` | Alanine Aminotransferase ALT (U/L) | 6,321 (53.0%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LBXSASSI` | Aspartate Aminotransferase AST (U/L) | 6,308 (52.9%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LBXSGTSI` | Gamma Glutamyl Transferase GGT (U/L) | 6,327 (53.0%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LBXSAL` | Albumin (g/dL) | 6,366 (53.4%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LBXSTB` | Total Bilirubin (mg/dL) | 6,325 (53.0%) | 6,279 (100.0%) | `RETAINED` |
| **Liver** | `LBXSAPSI` | Alkaline Phosphatase ALP (U/L) | 6,327 (53.0%) | 6,282 (100.0%) | `RETAINED` |
| **Liver** | `LUXSMED` | Liver Stiffness Median (kPa) | 6,700 (56.1%) | 5,892 (93.8%) | `RETAINED` |
| **Liver** | `LUXCAPM` | Controlled Attenuation Parameter CAP (dB/m) | 6,699 (56.1%) | 5,892 (93.8%) | `RETAINED` |
| **Kidney** | `LBXSCR` | Serum Creatinine (mg/dL) | 6,326 (53.0%) | 6,280 (100.0%) | `RETAINED` |
| **Kidney** | `LBXSBU` | Blood Urea Nitrogen BUN (mg/dL) | 6,326 (53.0%) | 6,279 (100.0%) | `RETAINED` |
| **Kidney** | `LBXSUA` | Uric Acid (mg/dL) | 6,329 (53.0%) | 6,282 (100.0%) | `RETAINED` |
| **Kidney** | `URXUMA` | Urine Albumin (ug/mL) | 8,153 (68.3%) | 6,158 (98.0%) | `RETAINED` |
| **Kidney** | `URXUCR` | Urine Creatinine (mg/dL) | 8,154 (68.3%) | 6,159 (98.0%) | `RETAINED` |
| **Kidney** | `KIQ022` | Ever told had kidney failure/disease (1=Yes, 2=No) | 7,807 (65.4%) | 5,404 (86.0%) | `RETAINED` |
| **Heart** | `BPXOSY1` | Systolic Blood Pressure Reading 1 (mmHg) | 7,517 (63.0%) | 6,089 (96.9%) | `RETAINED` |
| **Heart** | `BPXODI1` | Diastolic Blood Pressure Reading 1 (mmHg) | 7,517 (63.0%) | 6,089 (96.9%) | `RETAINED` |
| **Heart** | `BPXOPLS1` | Pulse Reading 1 (bpm) | 7,517 (63.0%) | 6,089 (96.9%) | `RETAINED` |
| **Heart** | `LBDHDD` | Direct HDL Cholesterol (mg/dL) | 6,890 (57.7%) | 6,282 (100.0%) | `RETAINED` |
| **Heart** | `LBXTC` | Total Cholesterol (mg/dL) | 6,890 (57.7%) | 6,282 (100.0%) | `RETAINED` |
| **Heart** | `BPQ020` | Ever told had high blood pressure (1=Yes, 2=No) | 8,498 (71.2%) | 5,838 (92.9%) | `RETAINED` |
| **Heart** | `MCQ160C` | Ever told had coronary heart disease (1=Yes, 2=No) | 7,807 (65.4%) | 5,403 (86.0%) | `RETAINED` |
| **Heart** | `MCQ160E` | Ever told had heart attack (1=Yes, 2=No) | 7,807 (65.4%) | 5,403 (86.0%) | `RETAINED` |
| **Biomarker** | `LBXWBCSI` | White Blood Cell count (10^9/L) | 7,593 (63.6%) | 6,282 (100.0%) | `RETAINED` |
| **Biomarker** | `LBXRBCSI` | Red Blood Cell count (10^12/L) | 7,593 (63.6%) | 6,282 (100.0%) | `RETAINED` |
| **Biomarker** | `LBXHGB` | Hemoglobin (g/dL) | 7,593 (63.6%) | 6,282 (100.0%) | `RETAINED` |
| **Biomarker** | `LBXPLTSI` | Platelet Count (10^9/L) | 7,593 (63.6%) | 6,282 (100.0%) | `RETAINED` |
| **Biomarker** | `LBXHSCRP` | High-sensitivity C-Reactive Protein hs-CRP (mg/L) | 7,282 (61.0%) | 6,282 (100.0%) | `RETAINED` |


---
## 5. Target Formulation & Verification

### Formulation
$$\text{FIB-4} = \frac{\text{Age (years)} \times \text{AST (U/L)}}{\text{Platelets } (10^9/\text{L}) \times \sqrt{\text{ALT (U/L)}}}$$
### Verification Results
- **Source Variables**: Age (`RIDAGEYR` from `DEMO_L`), AST (`LBXSASSI` from `BIOPRO_L`), ALT (`LBXSATSI` from `BIOPRO_L`), Platelets (`LBXPLTSI` from `CBC_L`).
- **Sample Size**: 6,277 patients
- **Mean ± Std**: 1.0590 ± 0.7748
- **Median**: 0.9028
- **25th–75th Percentile (IQR)**: 0.5091 – 1.4023 (0.8932)
- **Min / Max**: 0.0634 / 13.9971
- **Skewness**: 2.9236

---
## 6. Preprocessing & Leakage Prevention Architecture

To prevent data leakage during subsequent graph neural network and baseline model training:
1. **5-Fold Patient-Level CV**: Patients are strictly split at the `patient_uid` level. Zero patient overlap across training and validation folds.
2. **In-Fold Preprocessing**: `StandardScaler` and median imputation will be fitted strictly on the training fold, then applied to transform validation data.
3. **Y-Randomization**: Baseline target permutation will shuffle target $Y$ strictly within each training fold, leaving validation targets unchanged.
