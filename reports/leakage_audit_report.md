# HSGIN Pre-Training Target-Leakage Audit Report

**Cycle Scope**: NHANES August 2021–August 2023 ($N=6,277$)  
**Target Variable**: True FIB-4 Score  
**Formula**: $\text{FIB-4} = \frac{\text{Age} \times \text{AST}}{\text{Platelets} \times \sqrt{\text{ALT}}}$  

---
## 1. Executive Summary & Core Scientific Findings

To ensure that cross-organ GNN interaction modeling measures genuine systemic cross-talk rather than trivial mathematical reconstruction, we conducted three controlled 5-fold cross-validation experiments before model training:

1. **Experiment 1 (All Features)**: Includes direct mathematical components (`RIDAGEYR`, `LBXSASSI`, `LBXSATSI`, `LBXPLTSI`).
2. **Experiment 2 (Remove ALT/AST/Platelets)**: Retains `RIDAGEYR` (Age), excludes liver enzymes and platelets.
3. **Experiment 3 (Complete Leakage-Free)**: Excludes **ALL 4** direct mathematical FIB-4 inputs.

### Key Takeaways
- **Mathematical Leakage Effect**: In Experiment 1, models achieve near-reconstruction performance ($R^2 \approx 0.85–0.93$), which reflects the non-linear algebraic identity of FIB-4 rather than novel biological discovery.
- **Partial Leakage**: In Experiment 2, removing ALT/AST/Platelets drops $R^2$ significantly, showing Age alone carries general baseline trajectory but lacks organ specificity.
- **Leakage-Free Predictive Signal**: In Experiment 3 (Leakage-Free), remaining multi-organ features (GGT, Albumin, Bilirubin, ALP, Stiffness, CAP, Creatinine, BUN, Uric Acid, Urine Albumin, BP, HDL, Cholesterol, hs-CRP, WBC, RBC) achieve a genuine, leak-free predictive performance.
- **Recommendation**: **Experiment 3 (Complete Leakage-Free Configuration)** is locked as the primary scientific benchmark for HSGIN graph neural network training and organ ablations.

---
## 2. Comparative Performance Matrix Across 5-Fold Cross-Validation

| Experiment | Feature Set | Model | MAE (Mean ± Std) | RMSE (Mean ± Std) | $R^2$ (Mean ± Std) |
|---|---|---|---:|---:|---:|
| **Exp1_All_Features** (29 feats) | Experiment 1 | `Ridge_Regression` | 0.2105 ± 0.0039 | 0.3832 ± 0.0448 | **0.7550 ± 0.0323** |
| **Exp1_All_Features** (29 feats) | Experiment 1 | `Random_Forest` | 0.1060 ± 0.0061 | 0.2304 ± 0.0509 | **0.9105 ± 0.0310** |
| **Exp1_All_Features** (29 feats) | Experiment 1 | `XGBoost` | 0.0897 ± 0.0024 | 0.2031 ± 0.0474 | **0.9302 ± 0.0259** |
| **Exp1_All_Features** (29 feats) | Experiment 1 | `MLP_Regressor` | 0.0912 ± 0.0051 | 0.2012 ± 0.0414 | **0.9313 ± 0.0226** |
| **Exp2_Remove_Enzymes_Platelets** (26 feats) | Experiment 2 | `Ridge_Regression` | 0.3058 ± 0.0045 | 0.5098 ± 0.0376 | **0.5662 ± 0.0209** |
| **Exp2_Remove_Enzymes_Platelets** (26 feats) | Experiment 2 | `Random_Forest` | 0.2850 ± 0.0070 | 0.4956 ± 0.0419 | **0.5900 ± 0.0306** |
| **Exp2_Remove_Enzymes_Platelets** (26 feats) | Experiment 2 | `XGBoost` | 0.2783 ± 0.0044 | 0.4844 ± 0.0369 | **0.6081 ± 0.0265** |
| **Exp2_Remove_Enzymes_Platelets** (26 feats) | Experiment 2 | `MLP_Regressor` | 0.3647 ± 0.0120 | 0.5849 ± 0.0347 | **0.4236 ± 0.0774** |
| **Exp3_Leakage_Free** (25 feats) | Experiment 3 | `Ridge_Regression` | 0.4065 ± 0.0094 | 0.6058 ± 0.0386 | **0.3869 ± 0.0222** |
| **Exp3_Leakage_Free** (25 feats) | Experiment 3 | `Random_Forest` | 0.3862 ± 0.0095 | 0.5956 ± 0.0404 | **0.4066 ± 0.0434** |
| **Exp3_Leakage_Free** (25 feats) | Experiment 3 | `XGBoost` | 0.3821 ± 0.0098 | 0.5785 ± 0.0404 | **0.4408 ± 0.0316** |
| **Exp3_Leakage_Free** (25 feats) | Experiment 3 | `MLP_Regressor` | 0.4658 ± 0.0246 | 0.7230 ± 0.0804 | **0.1258 ± 0.1217** |

---

## 3. Detailed Experiment Breakdown

### Experiment 1: All Features (Full Manifest, Includes Direct FIB-4 Inputs)
- **Description**: Full feature manifest (27 features) including Age, AST, ALT, Platelets.
- **Features Included (29 total)**: `RIDAGEYR, RIAGENDR, LBXSATSI, LBXSASSI, LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM, LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022, BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E, LBXWBCSI, LBXRBCSI, LBXHGB, LBXPLTSI, LBXHSCRP`
- **Features Excluded**: None

| Model | MAE | RMSE | $R^2$ |
|---|---:|---:|---:|
| `Ridge_Regression` | 0.2105 ± 0.0039 | 0.3832 ± 0.0448 | 0.7550 ± 0.0323 |
| `Random_Forest` | 0.1060 ± 0.0061 | 0.2304 ± 0.0509 | 0.9105 ± 0.0310 |
| `XGBoost` | 0.0897 ± 0.0024 | 0.2031 ± 0.0474 | 0.9302 ± 0.0259 |
| `MLP_Regressor` | 0.0912 ± 0.0051 | 0.2012 ± 0.0414 | 0.9313 ± 0.0226 |

### Experiment 2: Remove ALT/AST/Platelets (Retain Age)
- **Description**: Excludes ALT, AST, Platelets; retains Age and remaining multi-organ features.
- **Features Included (26 total)**: `RIDAGEYR, RIAGENDR, LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM, LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022, BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E, LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP`
- **Features Excluded (3 total)**: `LBXSASSI, LBXSATSI, LBXPLTSI`

| Model | MAE | RMSE | $R^2$ |
|---|---:|---:|---:|
| `Ridge_Regression` | 0.3058 ± 0.0045 | 0.5098 ± 0.0376 | 0.5662 ± 0.0209 |
| `Random_Forest` | 0.2850 ± 0.0070 | 0.4956 ± 0.0419 | 0.5900 ± 0.0306 |
| `XGBoost` | 0.2783 ± 0.0044 | 0.4844 ± 0.0369 | 0.6081 ± 0.0265 |
| `MLP_Regressor` | 0.3647 ± 0.0120 | 0.5849 ± 0.0347 | 0.4236 ± 0.0774 |

### Experiment 3: Complete Leakage-Free (Remove Age, AST, ALT, Platelets)
- **Description**: Excludes ALL 4 direct FIB-4 mathematical inputs. Uses Liver(other)+Kidney+Heart+Biomarkers.
- **Features Included (25 total)**: `RIAGENDR, LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM, LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022, BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E, LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP`
- **Features Excluded (4 total)**: `RIDAGEYR, LBXSASSI, LBXSATSI, LBXPLTSI`

| Model | MAE | RMSE | $R^2$ |
|---|---:|---:|---:|
| `Ridge_Regression` | 0.4065 ± 0.0094 | 0.6058 ± 0.0386 | 0.3869 ± 0.0222 |
| `Random_Forest` | 0.3862 ± 0.0095 | 0.5956 ± 0.0404 | 0.4066 ± 0.0434 |
| `XGBoost` | 0.3821 ± 0.0098 | 0.5785 ± 0.0404 | 0.4408 ± 0.0316 |
| `MLP_Regressor` | 0.4658 ± 0.0246 | 0.7230 ± 0.0804 | 0.1258 ± 0.1217 |

---
## 4. Locked Pre-Training Recommendation for Phase 2

Based on this audit, **Experiment 3 (Complete Leakage-Free Configuration)** will serve as the primary evaluation setup for HSGIN graph construction and baseline comparison:
1. Direct mathematical inputs (`RIDAGEYR`, `LBXSASSI`, `LBXSATSI`, `LBXPLTSI`) will be excluded from the feature matrices during graph node construction.
2. Liver, Kidney, Heart, and Systemic Biomarker nodes will represent non-FIB-4 clinical parameters (Stiffness, CAP, Albumin, GGT, Creatinine, BUN, Blood Pressure, Cholesterol, hs-CRP, etc.).
3. HSGIN will be evaluated on its capability to predict FIB-4 purely from systemic cross-organ interactions, ensuring 100% scientific validity.