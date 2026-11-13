# ORGANIX: Dataset Provenance & Cohort Preparation

## 1. Primary Data Source: NHANES August 2021–August 2023 Cycle L

All data originates from the **CDC/NCHS National Health and Nutrition Examination Survey (NHANES)** for the August 2021 to August 2023 pre-pandemic/post-pandemic release cycle.

### Raw Data Location
Raw SAS Transport (`.xpt`) files are housed under:
`data/raw/nhanes_2021_2023/`
- `DEMO_G/`: Demographics (`DEMO_L.xpt`)
- `EXAMINATION/`: Body Measures (`BMX_L.xpt`), Blood Pressure Oscillometric (`BPXO_L.xpt`), FibroScan Liver Elastography (`LUX_L.xpt`)
- `LABORATORY/`: 14 laboratory panels including standard biochemistry (`BIOPRO_L.xpt`), complete blood count (`CBC_L.xpt`), lipid profiles (`HDL_L.xpt`, `TCHOL_L.xpt`, `TRIGLY_L.xpt`), viral hepatitis (`HEPA_L.xpt`, `HEPBD_L.xpt`, `HEPC_L.xpt`, `HEPE_L.xpt`), high-sensitivity CRP (`HSCRP_L.xpt`), insulin (`INS_L.xpt`), and fasting glucose (`GLU_L.xpt`)
- `QUESTIONNAIRE/`: Health conditions, blood pressure history, diabetes, kidney conditions, medical conditions, sleep disorders, and diet

---

## 2. Cohort Filtering & Inclusion Criteria

The raw participant count across the 27 survey files is $N = 11,933$. 
The final locked cohort consists of **$N = 6,277$ patients** following a 6-step clinical attrition flow:

| Step | Criterion Description | Remaining Patients | Excluded |
| :---: | :--- | :---: | :---: |
| 1 | Raw NHANES 2021–2023 Interviewed Cohort | 11,933 | Baseline |
| 2 | Examination Cohort (MEC Examined) | 11,284 | 649 |
| 3 | Complete FIB-4 Target Inputs Available (Age, AST, ALT, Platelets) | 6,282 | 5,002 |
| 4 | Valid Physiological Ranges ($\text{ALT} > 0, \text{Platelet Count} > 0, \text{AST} > 0$) | 6,277 | 5 |
| 5 | Complete Demographic & Gender Record | 6,277 | 0 |
| 6 | **Final Locked Study Cohort** | **6,277** | — |

---

## 3. The 25 Locked Leakage-Free Features

Direct algebraic formula inputs ($\text{Age}, \text{AST}, \text{ALT}, \text{Platelets}$) are strictly withheld from model training inputs.

The 25 retained features are:
1. **Demographics (1)**: `RIAGENDR` (Gender)
2. **Liver System (6)**: `LBXSGTSI` (GGT), `LBXSAL` (Albumin), `LBXSTB` (Total Bilirubin), `LBXSAPSI` (ALP), `LUXSMED` (Liver Stiffness kPa), `LUXCAPM` (Steatosis dB/m)
3. **Kidney System (6)**: `LBXSCR` (Creatinine), `LBXSBU` (BUN), `LBXSUA` (Uric Acid), `URXUMA` (Urine Microalbumin), `URXUCR` (Urine Creatinine), `KIQ022` (Self-reported kidney disease)
4. **Cardiovascular / Heart (8)**: `BPXOSY1` (Systolic BP), `BPXODI1` (Diastolic BP), `BPXOPLS1` (Pulse), `LBDHDD` (HDL), `LBXTC` (Total Cholesterol), `BPQ020` (Hypertension diagnosis), `MCQ160C` (Coronary Heart Disease), `MCQ160E` (Heart Attack / MI)
5. **Systemic Biomarkers (4)**: `LBXWBCSI` (White Blood Cells), `LBXRBCSI` (Red Blood Cells), `LBXHGB` (Hemoglobin), `LBXHSCRP` (High-sensitivity CRP)
