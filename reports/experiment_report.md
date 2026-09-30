# HSGIN Phase 2 Final Experiment & Audit Report: Leakage-Free 3-Organ Systemic Disease Modeling

**Project**: Heterogeneous Systemic Graph Interaction Network (HSGIN) for Multi-Organ Disease Modeling  
**Target Variable**: Continuous FIB-4 Score ($N = 6,277$ Patients)  
**Cohort Source**: NHANES August 2021–August 2023  
**Configuration**: Locked Experiment 3 (Leakage-Free Non-FIB-4 Feature Manifest)  
**Evaluation Protocol**: 5-Fold Cross-Validation with Fold-Safe Preprocessing  

---

## 1. Executive Summary

This report documents the finalized Phase 2 training, baseline benchmarks, 5-fold cross-validation, A–D tabular organ-ablation study, and in-fold target Y-randomization validation for the **HSGIN (Heterogeneous Systemic Graph Interaction Network)** pipeline.

Following target-leakage controls established in Phase 1, **all direct mathematical inputs to FIB-4 (Age, AST, ALT, and Platelet count)** were strictly excluded from the graph node features. The model predicts systemic liver fibrosis risk (FIB-4) using non-FIB-4 Liver markers, Kidney function, Cardiovascular/Heart indicators, and systemic Inflammatory biomarkers.

### Key Performance Findings
1. **HSGIN Performance**: The proposed **HSGIN architecture achieved an $R^2$ of $0.4976 \pm 0.0285$** (MAE: $0.3509 \pm 0.0091$, RMSE: $0.5478 \pm 0.0287$), outperforming the strongest tabular baseline (**XGBoost $R^2 = 0.4519$**) by **$+0.0457$ $R^2$ points** and the **Classical HGNN ($R^2 = 0.4681$)** by **$+0.0295$ $R^2$ points**.
2. **Incremental Predictive Value across Feature Domains**: The A–D tabular organ-ablation study (evaluated via XGBoost) demonstrated that expanding from Liver + Biomarker features ($R^2 = 0.1948$) to Full 3-Organ features ($R^2 = 0.4519$) yields an incremental **$+0.2572$ gain in $R^2$** and a **$0.1151$ reduction in MAE**, demonstrating substantial incremental predictive value from non-liver organs.
3. **Absence of Direct Mathematical Target Leakage**: In-fold Y-randomization yielded an **$R^2$ of $-0.0281 \pm 0.0291$** ($\approx 0$), supporting the absence of direct mathematical target leakage under the tested configuration.

---

## 2. Leakage-Free Feature Manifest (Experiment 3 Locked)

The feature set comprises **25 domain features** categorized into 5 node types across the patient graph:

| Node Type / Domain | Features Included | Excluded Direct FIB-4 Inputs |
| :--- | :--- | :--- |
| **Demographics** | `RIAGENDR` (Gender) | `RIDAGEYR` (Age) |
| **Liver** | `LBXSGTSI` (GGT), `LBXSAL` (Albumin), `LBXSTB` (Total Bilirubin), `LBXSAPSI` (Alkaline Phosphatase), `LUXSMED` (FibroScan Median Stiffness), `LUXCAPM` (CAP Attenuation) | `LBXSASSI` (AST), `LBXSATSI` (ALT) |
| **Kidney** | `LBXSCR` (Creatinine), `LBXSBU` (BUN), `LBXSUA` (Uric Acid), `URXUMA` (Microalbumin), `URXUCR` (Urine Creatinine), `KIQ022` (Kidney Disease History) | None |
| **Heart / Cardio** | `BPXOSY1` (Systolic BP), `BPXODI1` (Diastolic BP), `BPXOPLS1` (Pulse Rate), `LBDHDD` (HDL Cholesterol), `LBXTC` (Total Cholesterol), `BPQ020` (Hypertension History), `MCQ160C` (Coronary Heart Disease), `MCQ160E` (Heart Attack) | None |
| **Biomarker** | `LBXWBCSI` (WBC Count), `LBXRBCSI` (RBC Count), `LBXHGB` (Hemoglobin), `LBXHSCRP` (hs-CRP) | `LBXPLTSI` (Platelet Count) |

---

## 3. Comprehensive Model Performance Comparison (5-Fold CV)

All models were evaluated under identical 5-fold splits ($N=6,277$ total cohort; ~5,021 training / 1,256 validation per fold) using fold-isolated median imputation and standard scaling.

| Model Class | Architecture / Model | Mean MAE ($\pm$ STD) | Mean RMSE ($\pm$ STD) | Mean $R^2$ ($\pm$ STD) | Relative $R^2$ vs XGBoost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tabular Baseline** | Ridge Regression | $0.4065 \pm 0.0094$ | $0.6058 \pm 0.0386$ | $0.3869 \pm 0.0222$ | $-0.0650$ |
| **Tabular Baseline** | Random Forest | $0.3927 \pm 0.0093$ | $0.6019 \pm 0.0391$ | $0.3940 \pm 0.0409$ | $-0.0579$ |
| **Tabular Baseline** | XGBoost Regressor | $0.3740 \pm 0.0102$ | $0.5728 \pm 0.0417$ | $0.4519 \pm 0.0324$ | Baseline ($0.0000$) |
| **Tabular Baseline** | MLP Regressor | $0.4679 \pm 0.0280$ | $0.7204 \pm 0.0760$ | $0.1320 \pm 0.1152$ | $-0.3199$ |
| **Classical GNN** | Heterogeneous SAGE (HGNN) | $0.3648 \pm 0.0070$ | $0.5641 \pm 0.0337$ | $0.4681 \pm 0.0195$ | $+0.0162$ |
| **Proposed Model** | **HSGIN (Hetero GAT + Organ Readout)** | $\mathbf{0.3509 \pm 0.0091}$ | $\mathbf{0.5478 \pm 0.0287}$ | $\mathbf{0.4976 \pm 0.0285}$ | $\mathbf{+0.0457}$ |

---

## 4. A–D Tabular Organ-Ablation Study (XGBoost Feature Subset Analysis)

To evaluate the incremental predictive contribution of non-liver feature domains, a tabular ablation study was conducted across 4 feature configurations using XGBoost:

| Config ID | Feature Subset | Mean MAE | Mean RMSE | Mean $R^2$ | $\Delta \text{MAE}$ vs A | $\Delta \text{RMSE}$ vs A | $\Delta R^2$ vs A |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | **Liver + Biomarker** | $0.4891$ | $0.6935$ | $0.1948$ | Ref ($0.0000$) | Ref ($0.0000$) | Ref ($0.0000$) |
| **B** | **Liver + Kidney** | $0.4274$ | $0.6295$ | $0.3375$ | $-0.0618$ | $-0.0640$ | $\mathbf{+0.1427}$ |
| **C** | **Liver + Heart** | $0.4127$ | $0.6187$ | $0.3602$ | $-0.0764$ | $-0.0747$ | $\mathbf{+0.1654}$ |
| **D** | **Full 3-Organ (Liver+Kidney+Heart)** | $\mathbf{0.3740}$ | $\mathbf{0.5728}$ | $\mathbf{0.4519}$ | $\mathbf{-0.1151}$ | $\mathbf{-0.1206}$ | $\mathbf{+0.2572}$ |

*Note: This ablation explicitly quantifies tabular feature subset performance via XGBoost. Config D matches the XGBoost tabular baseline ($R^2 = 0.4519$). The proposed HSGIN model integrates all 3 organ domains within a heterogeneous graph architecture to reach $R^2 = 0.4976$.*

### Analysis of Tabular Feature Contributions
1. **Liver Features Alone**: Non-FIB-4 Liver markers alone (GGT, Albumin, Bilirubin, FibroScan) achieve an $R^2$ of $0.1948$.
2. **Incremental Multi-Organ Signal**: Adding Kidney indicators increases $R^2$ by **$+0.1427$**, while adding Heart/Cardio features increases $R^2$ by **$+0.1654$**.
3. **Combined Multi-Organ Benefit**: Combining all three organ domains yields a total $R^2$ gain of **$+0.2572$** over Liver + Biomarker features in the tabular benchmark.

---

## 5. HSGIN Architectural Organ Ablation Study (Configs A–D)

To empirically quantify the structural contribution of each organ node type within the **HSGIN (Heterogeneous Systemic Graph Interaction Network)** architecture, a full 5-fold cross-validation ablation study was conducted. Organ node and edge types were dynamically pruned from the graph while holding the feature manifest, 5-fold CV splits, seed strategy, and training hyperparameters strictly constant:

| Config ID | Description | Active Node Types | Mean MAE ($\pm$ SD) | Mean RMSE ($\pm$ SD) | Mean $R^2$ ($\pm$ SD) | $\Delta \text{MAE}$ vs A | $\Delta \text{RMSE}$ vs A | $\Delta R^2$ vs A |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | **Liver + Biomarker** | `patient, liver, biomarker` | $0.4249 \pm 0.0088$ | $0.6210 \pm 0.0243$ | $0.3540 \pm 0.0289$ | Ref ($0.0000$) | Ref ($0.0000$) | Ref ($0.0000$) |
| **B** | **Liver + Kidney** | `patient, liver, kidney, biomarker` | $0.3809 \pm 0.0130$ | $0.5792 \pm 0.0381$ | $0.4394 \pm 0.0279$ | $-0.0440$ | $-0.0418$ | $\mathbf{+0.0854}$ |
| **C** | **Liver + Heart** | `patient, liver, heart, biomarker` | $0.3650 \pm 0.0095$ | $0.5686 \pm 0.0317$ | $0.4592 \pm 0.0247$ | $-0.0599$ | $-0.0524$ | $\mathbf{+0.1053}$ |
| **D** | **Full 3-Organ** | `patient, liver, kidney, heart, biomarker` | $\mathbf{0.3509 \pm 0.0091}$ | $\mathbf{0.5478 \pm 0.0287}$ | $\mathbf{0.4976 \pm 0.0285}$ | $\mathbf{-0.0740}$ | $\mathbf{-0.0732}$ | $\mathbf{+0.1436}$ |

### Key Architectural Findings:
1. **Liver + Biomarker Subgraph Baseline (Config A)**: When restricted solely to liver node features, HSGIN achieves $R^2 = 0.3540 \pm 0.0289$. Note that graph message passing allows HSGIN to outperform the tabular Liver + Biomarker baseline ($R^2 = 0.1948$) by $+0.1592 R^2$ points.
2. **Impact of Kidney Node Integration (Config B)**: Integrating Kidney nodes (`patient <-> kidney`) into message passing improves $R^2$ by **$+0.0854$** to $0.4394 \pm 0.0279$ and reduces MAE by $-0.0440$.
3. **Impact of Heart Node Integration (Config C)**: Integrating Heart nodes (`patient <-> heart`) improves $R^2$ by **$+0.1053$** to $0.4592 \pm 0.0247$, demonstrating that the Liver + Heart configuration provides greater incremental predictive improvement than the Liver + Kidney configuration under this experimental setup.
4. **Full Multi-Organ Integration (Config D)**: Combining all three organ domains (Liver + Kidney + Heart) yields peak predictive performance ($R^2 = 0.4976 \pm 0.0285$, MAE $= 0.3509 \pm 0.0091$), representing a **$+0.1436$ total $R^2$ enhancement** over the single-organ base network.

---

## 6. In-Fold Target Y-Randomization Validation

To test for baseline target leakage under the Experiment 3 manifest:
- Target labels ($Y = \text{FIB-4}$) were permuted **strictly within each training fold**.
- Models were trained on permuted targets and evaluated on **untouched true validation targets**.

| Validation Protocol | Mean MAE ($\pm$ STD) | Mean RMSE ($\pm$ STD) | Mean $R^2$ ($\pm$ STD) | Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **True Model (HSGIN)** | $0.3509 \pm 0.0091$ | $0.5478 \pm 0.0287$ | $\mathbf{0.4976 \pm 0.0285}$ | Standard Training |
| **Y-Randomized Control** | $0.5569 \pm 0.0070$ | $0.7838 \pm 0.0351$ | $\mathbf{-0.0280 \pm 0.0291}$ | **Supports absence of direct mathematical leakage** |

---

## 7. Execution Summary

- **Cohort Size**: $N = 6,277$ patients from **NHANES August 2021–August 2023**.
- **Hardware Platform**: NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM) & Intel CPU.
- **Preprocessing Protocol**: 5-fold cross-validation with fold-isolated median imputation and z-score standardization.

---

## 8. Conclusion

The Phase 2 evaluation demonstrates that the **Heterogeneous Systemic Graph Interaction Network (HSGIN)** achieves $R^2 = 0.4976$ for FIB-4 score estimation under a non-leaky feature configuration. Both the tabular feature ablation and the graph architectural ablation (Configs A–D) confirm that multi-organ heterogeneity—specifically the combined integration of Liver, Kidney, and Heart information—is critical for optimal performance.
