# The Locked 25-Feature Manifest and Leakage-Exclusion Specification

**Manifest Source**: [`data/feature_manifest.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/feature_manifest.json)  
**Cryptographic Fingerprint**: SHA-256 = `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22`  
**Governing Rule**: Three-Source Agreement Verified (Manifest JSON $\equiv$ Feature Matrix Columns $\equiv$ Graph Builder Code)  
**Total Features in Registry**: 29 Variables Across 5 Biological Domains  
**Direct Formula Leakage Exclusions**: 4 Algebraic Components (Age, AST, ALT, Platelet Count)  
**Locked Predictor Set**: Exactly 25 Non-Formula Features  

---

## 1. The 4 Excluded Formula Components (Target Leakage Control)

To prevent direct mathematical identity leakage, the four input variables that algebraically compose the FIB-4 index are strictly quarantined. Under PRD Section 13.1, an automated assertion gate prevents these variables or any aliases from entering the training matrix:

| Excluded Variable | NHANES Source File | Domain | Clinical Description | Conventional Units | Mathematical Role in FIB-4 | Rationale for Exclusion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RIDAGEYR` | `DEMO_L.xpt` | Demographics | Chronological Age of Participant | Years | Numerator factor ($\text{Age}$) | Direct algebraic identity component |
| `LBXSASSI` | `BIOPRO_L.xpt` | Liver | Aspartate Aminotransferase (AST) | U/L | Numerator factor ($\text{AST}$) | Direct algebraic identity component |
| `LBXSATSI` | `BIOPRO_L.xpt` | Liver | Alanine Aminotransferase (ALT) | U/L | Denominator factor ($\sqrt{\text{ALT}}$) | Direct algebraic identity component |
| `LBXPLTSI` | `CBC_L.xpt` | Biomarker | Platelet Count | $10^9/\text{L}$ ($10^3/\mu\text{L}$) | Denominator factor ($\text{Platelets}$) | Direct algebraic identity component |

*Audit Verification*: [`src/comparative/leakage_gate.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/leakage_gate.py#L16-L63) asserts that direct formula overlap equals exactly 0 across all benchmarked models.

---

## 2. Full Specification of the 25 Locked Predictor Features

All 25 features are grouped into their physiological organ domains. Missing values are imputed strictly within each outer training fold using median values fitted on training data:

| # | Physiological Domain | Feature Name | NHANES Variable Code | Source File | Description & Clinical Measurement | Units | Cohort Missing % | Raw Survey Missing % | Fold Imputation Strategy |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | **Demographics** | `RIAGENDR` | `RIAGENDR` | `DEMO_L.xpt` | Biological Sex (1 = Male, 2 = Female) | Categorical (1/2) | **0.00%** | 0.00% | None (100% complete) |
| **2** | **Liver** | `LBXSGTSI` | `LBXSGTSI` | `BIOPRO_L.xpt` | Gamma Glutamyl Transferase (GGT) | U/L | **0.00%** | 46.98% | Fold-safe median |
| **3** | **Liver** | `LBXSAL` | `LBXSAL` | `BIOPRO_L.xpt` | Serum Albumin | g/dL | **0.00%** | 46.65% | Fold-safe median |
| **4** | **Liver** | `LBXSTB` | `LBXSTB` | `BIOPRO_L.xpt` | Total Bilirubin | mg/dL | **0.05%** | 47.00% | Fold-safe median |
| **5** | **Liver** | `LBXSAPSI` | `LBXSAPSI` | `BIOPRO_L.xpt` | Alkaline Phosphatase (ALP) | U/L | **0.00%** | 46.98% | Fold-safe median |
| **6** | **Liver** | `LUXSMED` | `LUXSMED` | `LUX_L.xpt` | Liver Stiffness Median (FibroScan) | kPa | **6.21%** | 43.85% | Fold-safe median |
| **7** | **Liver** | `LUXCAPM` | `LUXCAPM` | `LUX_L.xpt` | Controlled Attenuation Parameter (CAP) | dB/m | **6.21%** | 43.86% | Fold-safe median |
| **8** | **Kidney** | `LBXSCR` | `LBXSCR` | `BIOPRO_L.xpt` | Serum Creatinine | mg/dL | **0.03%** | 46.99% | Fold-safe median |
| **9** | **Kidney** | `LBXSBU` | `LBXSBU` | `BIOPRO_L.xpt` | Blood Urea Nitrogen (BUN) | mg/dL | **0.05%** | 46.99% | Fold-safe median |
| **10** | **Kidney** | `LBXSUA` | `LBXSUA` | `BIOPRO_L.xpt` | Serum Uric Acid | mg/dL | **0.00%** | 46.96% | Fold-safe median |
| **11** | **Kidney** | `URXUMA` | `URXUMA` | `ALB_CR_L.xpt` | Albumin - Urine | $\mu\text{g}/\text{mL}$ | **1.97%** | 31.68% | Fold-safe median |
| **12** | **Kidney** | `URXUCR` | `URXUCR` | `ALB_CR_L.xpt` | Creatinine - Urine | mg/dL | **1.96%** | 31.67% | Fold-safe median |
| **13** | **Kidney** | `KIQ022` | `KIQ022` | `KIQ_U_L.xpt` | Kidney Failure / Disease History (1=Yes, 2=No) | Categorical (1/2) | **13.98%** | 34.58% | Fold-safe median |
| **14** | **Heart** | `BPXOSY1` | `BPXOSY1` | `BPXO_L.xpt` | Systolic Blood Pressure (Reading 1) | mmHg | **3.07%** | 37.01% | Fold-safe median |
| **15** | **Heart** | `BPXODI1` | `BPXODI1` | `BPXO_L.xpt` | Diastolic Blood Pressure (Reading 1) | mmHg | **3.07%** | 37.01% | Fold-safe median |
| **16** | **Heart** | `BPXOPLS1` | `BPXOPLS1` | `BPXO_L.xpt` | Pulse Rate (Reading 1) | beats/min | **3.07%** | 37.01% | Fold-safe median |
| **17** | **Heart** | `LBDHDD` | `LBDHDD` | `HDL_L.xpt` | High-Density Lipoprotein (HDL) Cholesterol | mg/dL | **0.00%** | 42.26% | Fold-safe median |
| **18** | **Heart** | `LBXTC` | `LBXTC` | `TCHOL_L.xpt` | Total Cholesterol | mg/dL | **0.00%** | 42.26% | Fold-safe median |
| **19** | **Heart** | `BPQ020` | `BPQ020` | `BPQ_L.xpt` | High Blood Pressure History (1=Yes, 2=No) | Categorical (1/2) | **7.07%** | 28.79% | Fold-safe median |
| **20** | **Heart** | `MCQ160C` | `MCQ160C` | `MCQ_L.xpt` | Coronary Heart Disease History (1=Yes, 2=No) | Categorical (1/2) | **13.99%** | 34.58% | Fold-safe median |
| **21** | **Heart** | `MCQ160E` | `MCQ160E` | `MCQ_L.xpt` | Heart Attack History (1=Yes, 2=No) | Categorical (1/2) | **13.99%** | 34.58% | Fold-safe median |
| **22** | **Biomarker** | `LBXWBCSI` | `LBXWBCSI` | `CBC_L.xpt` | White Blood Cell (WBC) Count | $10^9/\text{L}$ | **0.00%** | 36.37% | Fold-safe median |
| **23** | **Biomarker** | `LBXRBCSI` | `LBXRBCSI` | `CBC_L.xpt` | Red Blood Cell (RBC) Count | $10^{12}/\text{L}$ | **0.00%** | 36.37% | Fold-safe median |
| **24** | **Biomarker** | `LBXHGB` | `LBXHGB` | `CBC_L.xpt` | Hemoglobin | g/dL | **0.00%** | 36.37% | Fold-safe median |
| **25** | **Biomarker** | `LBXHSCRP` | `LBXHSCRP` | `HSCRP_L.xpt` | High-Sensitivity C-Reactive Protein (hs-CRP) | mg/L | **0.00%** | 38.98% | Fold-safe median |

*Sources*: [`data/feature_manifest.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/feature_manifest.json#L1-L186), [`data/missingness_report.csv`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/missingness_report.csv#L1-L30)

---

## 3. Domain Summary Counts

| Domain Identifier | Assigned Node in HSGIN | Retained Features ($N$) | Excluded Features ($N$) | Total Registered Variables |
| :--- | :--- | :---: | :---: | :---: |
| **Demographics** | `patient` | 1 | 1 (`RIDAGEYR`) | 2 |
| **Liver** | `liver` | 6 | 2 (`LBXSASSI`, `LBXSATSI`) | 8 |
| **Kidney** | `kidney` | 6 | 0 | 6 |
| **Heart** | `heart` | 8 | 0 | 8 |
| **Biomarker** | `biomarker` | 4 | 1 (`LBXPLTSI`) | 5 |
| **Total** | **5 Graph Nodes** | **25 Features** | **4 Excluded** | **29 Variables** |

---

## 4. Verification Check: 3-Source Agreement

As mandated by PRD Section 12.3:
1. **Manifest File**: [`data/feature_manifest.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/feature_manifest.json) has SHA-256 `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22`.
2. **Processed Training Columns**: The 25 retained column names match the order in [`src/pipeline.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/pipeline.py#L42-L54) and [`src/comparative/base_adapter.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/base_adapter.py).
3. **Graph Node Slices**: In [`src/graph_builder.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/graph_builder.py#L28-L51), the feature dimensions per node are:
   - `data['patient'].x`: shape $[1, 1]$
   - `data['liver'].x`: shape $[1, 6]$
   - `data['kidney'].x`: shape $[1, 6]$
   - `data['heart'].x`: shape $[1, 8]$
   - `data['biomarker'].x`: shape $[1, 4]$
   - **Sum of Node Feature Dimensions**: $1 + 6 + 6 + 8 + 4 = 25$ features.
   - **Agreement Status**: **100% PERFECT 3-SOURCE PARITY (PASSED)**.
