# HSGIN 3-Organ Disease Modeling â€” Final Master Technical Handover Report

**Document Version**: 1.0 | **Date**: 2026-08-08 | **Cohort**: NHANES August 2021â€“August 2023 (N=6,277)

---

# 1. Project Identity

- **Project Name**: HSGIN 3-Organ Disease Modeling Pipeline
- **HSGIN Full Form**: Heterogeneous Systemic Graph Interaction Network
- **Research Problem**: Can multi-organ biomarker interactions (Liver + Kidney + Heart) predict liver fibrosis risk (FIB-4) without using FIB-4's own algebraic input variables?
- **Research Motivation**: Traditional liver fibrosis assessment relies on single-organ markers. Systemic disease processes involve inter-organ metabolic interactions that single-organ models cannot capture.
- **Original 5-Organ North Star**: Liver + Kidney + Heart + Gut + Brain
- **Current Validated 3-Organ Scope**: Liver + Kidney + Heart/Cardiovascular
- **Why Reduced from 5 to 3**: NHANES August 2021â€“August 2023 lacks validated, patient-level gut microbiome and neuroimaging/cognitive variables mappable via SEQN. Brain and Gut were deferred to future work pending suitable data sources.
- **Current Research Hypothesis**: Non-FIB-4 features from Liver, Kidney, and Heart/Cardiovascular domains, modeled as a heterogeneous graph, provide incremental predictive value for continuous FIB-4 score estimation beyond what single-organ or flat tabular models achieve.
- **Current Prediction Target**: Continuous FIB-4 score (regression)

---

# 2. Executive Summary

We built a heterogeneous graph neural network (HSGIN) that predicts continuous FIB-4 liver fibrosis scores from 25 non-FIB-4 features spanning 3 organ systems (Liver, Kidney, Heart) plus systemic biomarkers, using N=6,277 patients from NHANES August 2021â€“August 2023.

**What was built**: An end-to-end pipeline from raw NHANES XPT files â†’ SEQN-linked master table â†’ cohort construction â†’ target leakage audit â†’ leakage-free feature locking â†’ PyG HeteroData graph construction â†’ 5-fold CV training of tabular baselines, Classical HGNN, and HSGIN â†’ tabular organ ablation â†’ Y-randomization validation.

**Key results**: HSGIN achieved RÂ²=0.4976Â±0.0285, outperforming XGBoost (RÂ²=0.4519) by +0.0457 RÂ² and Classical HGNN (RÂ²=0.4681) by +0.0295 RÂ². The tabular Aâ€“D ablation showed Liver-only RÂ²=0.1948 vs Full 3-Organ RÂ²=0.4519, a +0.2572 RÂ² gain. Y-randomization yielded RÂ²=âˆ’0.0281, supporting absence of direct mathematical target leakage.

**State of the project**: Phase 1 (data/audit) and Phase 2 (training/evaluation) are complete. All metrics are finalized in `data/experiment_results.json`. No HSGIN-specific organ ablation was performed (ablation used XGBoost). No formal statistical significance testing was conducted. External validation has not been performed.

---

# 3. Research Evolution / Decision History

| Decision | Rationale |
|:---|:---|
| Original 5-organ concept (Liver+Kidney+Heart+Gut+Brain) | Capture full systemic disease interactions |
| Gut/Brain set aside | No patient-level NHANES variables for gut microbiome or neuroimaging via SEQN |
| NHANES Aug 2021â€“Aug 2023 selected | Contains FibroScan elastography (LUX_L), comprehensive biochemistry, blood pressure, questionnaires; all linkable via unique SEQN |
| Same-patient SEQN strategy | Outer-join on SEQN ensures all features belong to the same individual |
| Cohort expanded to ~6.3K | Sequential inclusion filtering yielded N=6,277 with complete FIB-4 inputs + kidney/cardio baselines |
| FIB-4 as continuous target | Clinically validated non-invasive liver fibrosis index; continuous regression avoids information loss from binarization |
| Target leakage discovery | FIB-4 = (AgeÃ—AST)/(PlateletsÃ—âˆšALT); including Age/AST/ALT/Platelets as model inputs creates mathematical identity leakage |
| 3-experiment leakage audit | Quantified leakage severity: Exp1 (all features) RÂ²=0.93, Exp2 (remove AST/ALT/Platelets) RÂ²=0.61, Exp3 (remove all 4) RÂ²=0.44 |
| Experiment 3 locked | Only configuration where no direct FIB-4 algebraic input is available to the model |
| Graph redesign | Each patient becomes a HeteroData graph with 5 node types and 14 edge types encoding organ relationships |
| HSGIN with organ-aware readout | Concatenates patient + mean-pooled organ + biomarker embeddings rather than using patient-node-only readout |
| GATConv add_self_loops=False | Required fix: HeteroConv with bipartite edges (different src/dst node counts) cannot use self-loops |
| 5-fold patient-level CV | Standard evaluation with fold-safe preprocessing |

---

# 4. Dataset & Provenance

**Source**: NHANES August 2021â€“August 2023 (CDC public release)
**Initial participants**: 11,933 unique SEQN
**Final cohort**: N=6,277 after sequential inclusion filtering
**Linkage**: All files joined on SEQN (verified unique per file via `ingestion_summary.csv`)

### Source Files Used

| File Key | Category | Description | Rows | Variables Used | Organ/System |
|:---|:---|:---|:---|:---|:---|
| DEMO_L | DEMO G | Demographics | 11,933 | RIDAGEYRÂ¹, RIAGENDR | Demographics |
| BIOPRO_L | LABORATORY | Biochemistry Profile | 7,199 | LBXSASSIÂ¹, LBXSATSIÂ¹, LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LBXSCR, LBXSBU, LBXSUA | Liver, Kidney |
| CBC_L | LABORATORY | Complete Blood Count | 8,727 | LBXWBCSI, LBXRBCSI, LBXHGB, LBXPLTSIÂ¹ | Biomarker |
| ALB_CR_L | LABORATORY | Albumin & Creatinine - Urine | 8,493 | URXUMA, URXUCR | Kidney |
| HDL_L | LABORATORY | HDL Cholesterol | 8,068 | LBDHDD | Heart |
| TCHOL_L | LABORATORY | Total Cholesterol | 8,068 | LBXTC | Heart |
| HSCRP_L | LABORATORY | High-Sensitivity CRP | 8,727 | LBXHSCRP | Biomarker |
| BPXO_L | EXAMINATION | Blood Pressure - Oscillometric | 7,801 | BPXOSY1, BPXODI1, BPXOPLS1 | Heart |
| LUX_L | EXAMINATION | Liver Ultrasound Elastography | 7,199 | LUXSMED, LUXCAPM | Liver |
| BPQ_L | QUESTIONNAIRE | Blood Pressure Questionnaire | 8,501 | BPQ020 | Heart |
| KIQ_U_L | QUESTIONNAIRE | Kidney Conditions | 7,809 | KIQ022 | Kidney |
| MCQ_L | QUESTIONNAIRE | Medical Conditions | 11,744 | MCQ160C, MCQ160E | Heart |

Â¹ = Excluded from model inputs (FIB-4 algebraic components), retained only for target computation.

### Cohort Flow (from `cohort_flow.csv`)

| Step | Filter | N Remaining | N Excluded |
|:---|:---|:---|:---|
| 1 | Initial NHANES participants | 11,933 | 0 |
| 2 | Demographics complete | 11,933 | 0 |
| 3 | Liver enzymes (ALT & AST complete & >0) | 6,308 | 5,625 |
| 4 | Platelet count complete & >0 | 6,282 | 26 |
| 5 | Kidney baseline (Creatinine & BUN) | 6,277 | 5 |
| 6 | Cardiovascular baseline (HDL & Total Cholesterol) | 6,277 | 0 |

**Missingness handling**: Features with residual missingness in the final cohort (e.g., KIQ022 at 13.98%, LUXSMED at 6.21%) are imputed via fold-safe median imputation fitted strictly within each training fold.

**Provenance limitations**: Data are observational, cross-sectional, and self-reported for questionnaire items. No longitudinal follow-up. Population is US-representative (NHANES sampling design) but may not generalize to other populations.

---

# 5. Final Feature Manifest (Experiment 3 Locked)

25 features used as model inputs. 4 features excluded due to FIB-4 target leakage.

### Demographics (1 feature used, 1 excluded)

| Variable | Meaning | Source | Used | Excluded Reason |
|:---|:---|:---|:---|:---|
| RIAGENDR | Gender (1=Male, 2=Female) | DEMO_L | âœ… | â€” |
| RIDAGEYR | Age in years | DEMO_L | âŒ | Direct FIB-4 numerator component |

### Liver (6 features used, 2 excluded)

| Variable | Meaning | Source | Used | Cohort Missing % |
|:---|:---|:---|:---|:---|
| LBXSGTSI | Gamma Glutamyl Transferase GGT (U/L) | BIOPRO_L | âœ… | 0.00% |
| LBXSAL | Albumin (g/dL) | BIOPRO_L | âœ… | 0.00% |
| LBXSTB | Total Bilirubin (mg/dL) | BIOPRO_L | âœ… | 0.05% |
| LBXSAPSI | Alkaline Phosphatase ALP (U/L) | BIOPRO_L | âœ… | 0.00% |
| LUXSMED | Liver Stiffness Median kPa (FibroScan) | LUX_L | âœ… | 6.21% |
| LUXCAPM | Controlled Attenuation Parameter CAP (dB/m) | LUX_L | âœ… | 6.21% |
| LBXSASSI | AST (U/L) | BIOPRO_L | âŒ | FIB-4 numerator |
| LBXSATSI | ALT (U/L) | BIOPRO_L | âŒ | FIB-4 denominator (âˆšALT) |

### Kidney (6 features used)

| Variable | Meaning | Source | Cohort Missing % |
|:---|:---|:---|:---|
| LBXSCR | Serum Creatinine (mg/dL) | BIOPRO_L | 0.03% |
| LBXSBU | Blood Urea Nitrogen BUN (mg/dL) | BIOPRO_L | 0.05% |
| LBXSUA | Uric Acid (mg/dL) | BIOPRO_L | 0.00% |
| URXUMA | Urine Albumin (ug/mL) | ALB_CR_L | 1.97% |
| URXUCR | Urine Creatinine (mg/dL) | ALB_CR_L | 1.96% |
| KIQ022 | Ever told had kidney disease (1=Yes, 2=No) | KIQ_U_L | 13.98% |

### Heart/Cardiovascular (8 features used)

| Variable | Meaning | Source | Cohort Missing % |
|:---|:---|:---|:---|
| BPXOSY1 | Systolic BP Reading 1 (mmHg) | BPXO_L | 3.07% |
| BPXODI1 | Diastolic BP Reading 1 (mmHg) | BPXO_L | 3.07% |
| BPXOPLS1 | Pulse Rate Reading 1 (bpm) | BPXO_L | 3.07% |
| LBDHDD | Direct HDL Cholesterol (mg/dL) | HDL_L | 0.00% |
| LBXTC | Total Cholesterol (mg/dL) | TCHOL_L | 0.00% |
| BPQ020 | Ever told high blood pressure (1=Yes, 2=No) | BPQ_L | 7.07% |
| MCQ160C | Ever told coronary heart disease (1=Yes, 2=No) | MCQ_L | 13.99% |
| MCQ160E | Ever told heart attack (1=Yes, 2=No) | MCQ_L | 13.99% |

### Systemic Biomarkers (3 features used, 1 excluded)

| Variable | Meaning | Source | Used | Cohort Missing % |
|:---|:---|:---|:---|:---|
| LBXWBCSI | White Blood Cell count (10â¹/L) | CBC_L | âœ… | 0.00% |
| LBXRBCSI | Red Blood Cell count (10Â¹Â²/L) | CBC_L | âœ… | 0.00% |
| LBXHGB | Hemoglobin (g/dL) | CBC_L | âœ… | 0.00% |
| LBXHSCRP | hs-CRP (mg/L) | HSCRP_L | âœ… | 0.00% |
| LBXPLTSI | Platelet Count (10â¹/L) | CBC_L | âŒ | FIB-4 denominator |

---

# 6. Target Definition

**FIB-4 Formula**: FIB-4 = (Age Ã— AST) / (Platelets Ã— âˆšALT)

| Component | NHANES Variable | Unit |
|:---|:---|:---|
| Age | RIDAGEYR | Years |
| AST | LBXSASSI | U/L |
| ALT | LBXSATSI | U/L |
| Platelets | LBXPLTSI | 10â¹/L |

**Why FIB-4**: Clinically validated non-invasive liver fibrosis score. Widely used in hepatology. Continuous formulation preserves full distributional information.

**Target distribution** (from `fib4_target_validation.json`): Mean=1.0590, Std=0.7748, Median=0.9028, Min=0.0634, Max=13.9971, Skewness=2.9236. N=6,277. All validation gates passed (no NaN/Inf, unique SEQN/patient_uid).

**Why direct components were removed**: FIB-4 is a deterministic algebraic function of Age, AST, ALT, Platelets. Including any of these as model inputs creates mathematical identity leakage â€” the model can reconstruct FIB-4 from its own formula inputs rather than learning genuine multi-organ associations. High RÂ² under such conditions reflects algebraic reconstruction, not biological prediction.

---

# 7. Target-Leakage Investigation

Three controlled experiments were run using 5-fold CV with 4 tabular models each (Ridge, Random Forest, XGBoost, MLP). Best model per experiment (XGBoost) reported below:

| Experiment | Features | Excluded | XGBoost RÂ² | Interpretation |
|:---|:---|:---|:---|:---|
| **Exp 1**: All Features | 27 features including Age, AST, ALT, Platelets | None | 0.9302 | Near-perfect reconstruction via algebraic identity; confirms severe leakage |
| **Exp 2**: Remove enzymes+platelets | 24 features; Age retained | LBXSASSI, LBXSATSI, LBXPLTSI | 0.6081 | Age alone carries substantial leakage (linear numerator component) |
| **Exp 3**: Complete leakage-free | 25 features; all 4 FIB-4 inputs removed | RIDAGEYR, LBXSASSI, LBXSATSI, LBXPLTSI | 0.4408 | Direct mathematical target leakage controlled |

**Experiment 3 was locked as the primary configuration** because it is the only setup where no direct algebraic input to FIB-4 is available as a model feature.

**What this audit establishes**: Direct mathematical target leakage from FIB-4's algebraic components has been controlled under the tested configuration.

**What it does NOT establish**: (1) Absence of all possible indirect/confounded leakage pathways. (2) That remaining features have no statistical correlation with excluded variables. (3) Clinical validity of the resulting predictions.

---

# 8. Final Graph Representation

Each of the N=6,277 patients is represented as an independent PyTorch Geometric `HeteroData` object.

### Node Types & Feature Dimensions

| Node Type | Features | Dimension |
|:---|:---|:---|
| `patient` | [RIAGENDR] | 1 |
| `liver` | [LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM] | 6 |
| `kidney` | [LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022] | 6 |
| `heart` | [BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E] | 8 |
| `biomarker` | [LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP] | 4 |

### Edge Types (14 total)

```
Patient-Organ (8 edges, bidirectional):
  patient --pertains_to--> liver        liver --rev_pertains_to--> patient
  patient --pertains_to--> kidney       kidney --rev_pertains_to--> patient
  patient --pertains_to--> heart        heart --rev_pertains_to--> patient
  patient --pertains_to--> biomarker    biomarker --rev_pertains_to--> patient

Inter-Organ (6 edges, bidirectional):
  liver --interacts_with--> kidney      kidney --interacts_with--> liver
  liver --interacts_with--> heart       heart --interacts_with--> liver
  kidney --interacts_with--> heart      heart --interacts_with--> kidney
```

### ASCII Graph Diagram
```
                    [Patient (1)]
                   / |    |     \
                  /  |    |      \
           [Liver(6)] [Kidney(6)] [Heart(8)] [Biomarker(4)]
                 \     |     /
                  \    |    /
              (interacts_with)
```

**Why no Brain/Gut nodes**: No validated patient-level NHANES variables for gut microbiome composition or neuroimaging/cognitive assessment are available in this dataset cycle.

**Graph target**: `data['patient'].y` stores the continuous FIB-4 score.

---

# 9. HSGIN Architecture

**Implementation file**: `src/models/hsgin.py`

The model is technically a **Heterogeneous GATConv network** (not HGT). It uses `torch_geometric.nn.GATConv` wrapped in `HeteroConv`, not `HGTConv`.

### Architecture Details (from source code)

| Parameter | Value | Source |
|:---|:---|:---|
| Model class | `HSGIN` (hsgin.py:44) | Verified |
| Conv layer type | `GATConv` via `HeteroConv` | hsgin.py:30 |
| Hidden dimension | 64 | train.py:51 |
| Number of conv layers | 2 | train.py:51 |
| Attention heads | 2 | hsgin.py:33 |
| Concat heads | True (output = heads Ã— out_channels) | hsgin.py:34 |
| add_self_loops | False (required for bipartite edges) | hsgin.py:35 |
| HeteroConv aggregation | 'mean' | hsgin.py:38 |
| Dropout | 0.1 (train) / 0.2 (model default, overridden) | train.py:51 |
| Activation | ReLU | hsgin.py:60,97 |
| Residual connections | Yes (h + h_new per layer) | hsgin.py:97 |
| Normalization | LayerNorm in encoder | hsgin.py:59 |
| Loss function | SmoothL1Loss (Huber) | train.py:53 |
| Optimizer | AdamW | train.py:52 |
| Learning rate | 0.001 | train.py:46 |
| Weight decay | 1e-4 | train.py:52 |
| Batch size | 64 | train.py:48 |
| Epochs | 50 per fold | train.py:203 |
| Scheduler | None | Verified |
| Early stopping | None (best RÂ² checkpoint tracked) | train.py:79 |

### Organ-Aware Readout

The readout concatenates three representations (hsgin.py:99-112):
1. `h_patient`: Patient node embedding after message passing
2. `h_organ_pool`: Mean of liver + kidney + heart embeddings (h_liver + h_kidney + h_heart) / 3
3. `h_biomarker`: Biomarker node embedding

Concatenated vector dimension: 64 Ã— 3 = 192 â†’ MLP prediction head â†’ scalar FIB-4 output.

This differs from the Classical HGNN baseline which uses patient-node-only readout.

---

# 10. Training Pipeline

### End-to-End Flow
```
Raw XPT files (NHANES Aug'21-Aug'23)
  â†’ src/dataset.py: Load 27 XPT files, verify SEQN uniqueness, outer-join â†’ data/master_patient.csv
  â†’ src/audit.py: Feature-level missingness audit â†’ data/feature_manifest.json, data/missingness_report.csv
  â†’ src/cohort.py: Sequential inclusion filtering â†’ data/final_cohort.csv (N=6,277), data/cohort_flow.csv
  â†’ src/target.py: Compute & verify FIB-4 â†’ data/fib4_target_validation.json
  â†’ src/leakage_audit.py: 3-experiment leakage audit â†’ data/leakage_audit_results.json
  â†’ src/graph_builder.py: Build HeteroData graphs â†’ graphs/patient_graphs.pt
  â†’ src/train.py: Master pipeline orchestrator:
      Phase 1: Tabular baselines (5-fold CV)
      Phase 2: Classical HGNN (5-fold CV, 40 epochs)
      Phase 3: HSGIN (5-fold CV, 50 epochs)
      Phase 4: Aâ€“D organ ablation (src/ablation.py, XGBoost)
      Phase 5: Y-randomization (src/y_randomization.py)
      â†’ data/experiment_results.json
```

### Fold-Safe Preprocessing (src/pipeline.py)

- **Tabular**: `SimpleImputer(strategy='median')` and `StandardScaler` fit strictly on training fold, transform applied to validation fold.
- **Graph**: Per-node-type imputer and scaler fit on concatenated training-fold node features, applied to both train and validation graph node matrices independently.
- **Splitting**: `KFold(n_splits=5, shuffle=True, random_state=42)` on unique `patient_uid` values.

---

# 11. Leakage Prevention Beyond Target Leakage

| Control | Implementation | Status |
|:---|:---|:---|
| Patient-level CV splits | KFold on patient_uid (no patient appears in both train and val) | âœ… Verified |
| Fold-safe scaling | StandardScaler.fit() on training fold only | âœ… Verified (pipeline.py:52) |
| Fold-safe imputation | SimpleImputer.fit() on training fold only | âœ… Verified (pipeline.py:52) |
| Target variable isolation | FIB-4 algebraic inputs excluded from all model features | âœ… Verified (graph_builder.py:14) |
| Y-randomization | Training targets permuted within-fold; validation targets untouched | âœ… Verified (y_randomization.py:26) |

**Known remaining risks**:
- Indirect statistical correlations between included features and excluded FIB-4 components (e.g., creatinine may correlate with age)
- No temporal leakage assessment (cross-sectional data; not applicable)
- Feature selection was manual/domain-driven, not formally optimized

---

# 12. Baseline Models

| Model | Type | Input | Purpose | Config |
|:---|:---|:---|:---|:---|
| Ridge Regression | Tabular | 25 flat features | Linear baseline | alpha=1.0 |
| Random Forest | Tabular | 25 flat features | Non-linear ensemble baseline | n_estimators=100, max_depth=10 |
| XGBoost | Tabular | 25 flat features | Strong gradient boosting baseline | n_estimators=150, max_depth=5, lr=0.05 |
| MLP Regressor | Tabular | 25 flat features | Neural network tabular baseline | layers=(64,32), max_iter=500 |
| Classical HGNN | Graph (HeteroConv+SAGEConv) | HeteroData graphs | Graph baseline without organ-aware readout | hidden=64, 40 epochs, patient-only readout |

All baselines use the same 5-fold splits, same fold-safe preprocessing, same random seeds.
# HSGIN Final Master Technical Handover Report â€” Part 2 (Sections 13â€“24)

---

# 13. Final HSGIN Results

All metrics from `data/experiment_results.json` (exact stored values):

| Model | MAE MeanÂ±STD | RMSE MeanÂ±STD | RÂ² MeanÂ±STD |
|:---|:---|:---|:---|
| Ridge Regression | 0.4065Â±0.0094 | 0.6058Â±0.0386 | 0.3869Â±0.0222 |
| Random Forest | 0.3927Â±0.0093 | 0.6019Â±0.0391 | 0.3940Â±0.0409 |
| XGBoost | 0.3740Â±0.0102 | 0.5728Â±0.0417 | 0.4519Â±0.0324 |
| MLP Regressor | 0.4679Â±0.0280 | 0.7204Â±0.0760 | 0.1320Â±0.1152 |
| Classical HGNN | 0.3648Â±0.0070 | 0.5641Â±0.0337 | 0.4681Â±0.0195 |
| **HSGIN (Proposed)** | **0.3509Â±0.0091** | **0.5478Â±0.0287** | **0.4976Â±0.0285** |

### Improvement Deltas

| Comparison | Î”RÂ² | Î”MAE | Î”RMSE |
|:---|:---|:---|:---|
| HSGIN vs XGBoost | +0.0457 | âˆ’0.0231 | âˆ’0.0250 |
| HSGIN vs Classical HGNN | +0.0295 | âˆ’0.0139 | âˆ’0.0163 |

---

# 14. Aâ€“D Organ Ablation

**CRITICAL NOTE**: This ablation was performed using **XGBoost (tabular)**, NOT HSGIN. This is verified by examining `src/ablation.py` which instantiates `XGBRegressor` (line 40). Config D RÂ²=0.4519 exactly matches the XGBoost tabular baseline, confirming this.

| Config | Feature Subset | MAE | RMSE | RÂ² | Î”MAE vs A | Î”RMSE vs A | Î”RÂ² vs A |
|:---|:---|:---|:---|:---|:---|:---|:---|
| A | Liver Only (6 feats) | 0.4891 | 0.6935 | 0.1948 | Ref | Ref | Ref |
| B | Liver+Kidney (12 feats) | 0.4274 | 0.6295 | 0.3375 | âˆ’0.0618 | âˆ’0.0640 | +0.1427 |
| C | Liver+Heart (14 feats) | 0.4127 | 0.6187 | 0.3602 | âˆ’0.0764 | âˆ’0.0747 | +0.1654 |
| D | Full 3-Organ (25 feats) | 0.3740 | 0.5728 | 0.4519 | âˆ’0.1151 | âˆ’0.1206 | +0.2572 |

**What this demonstrates**: Adding Kidney and Heart features to a tabular XGBoost model provides substantial incremental predictive value for FIB-4 estimation (+0.2572 RÂ²).

**What this does NOT demonstrate**:
- It is NOT an HSGIN-specific ablation. No claim about HSGIN-specific organ synergy can be made from this data.
- It does not establish causal biological organ interactions or mechanistic crosstalk.
- Predictive value may arise from confounding, demographic correlation, or shared risk factors rather than direct organ-to-organ biological pathways.

---

# 15. Y-Randomization

**Procedure** (from `src/y_randomization.py`):
- Within each of 5 training folds: `y_train` is randomly permuted using `np.random.permutation` with seed=42+fold
- Validation targets `y_val` are kept completely untouched
- XGBoost (n_estimators=150, max_depth=5, lr=0.05) is trained on permuted targets
- Predictions are evaluated against true `y_val`

**Results** (from `experiment_results.json`):

| Metric | MeanÂ±STD |
|:---|:---|
| MAE | 0.5569Â±0.0070 |
| RMSE | 0.7838Â±0.0351 |
| RÂ² | âˆ’0.0281Â±0.0291 |

**Interpretation**: The near-zero (slightly negative) RÂ² under target permutation supports the absence of direct mathematical target leakage under the tested Experiment 3 configuration. A model trained on randomized targets cannot predict true validation targets, indicating the features do not contain a trivial algebraic path to FIB-4.

This does NOT constitute proof of biological validity, clinical utility, or absence of all forms of indirect leakage.

---

# 16. Statistical / Evaluation Interpretation

- **5-fold CV**: Standard protocol. 5 folds provide 5 point estimates per model.
- **Reported metrics**: Mean Â± standard deviation across 5 folds.
- **Formal significance testing**: NOT performed. No paired t-tests, Wilcoxon tests, or bootstrap confidence intervals were computed.
- **Statistical superiority**: NOT formally established. The observed RÂ² differences (e.g., HSGIN vs XGBoost: +0.0457) may or may not be statistically significant.
- **Confidence intervals**: NOT calculated.
- **Limitation**: With only 5 folds, variance estimates have limited precision.
- **Recommendation for future work**: Perform paired bootstrap confidence intervals or repeated CV with multiple seeds to establish statistical significance.

---

# 17. Reproducibility

### Environment
- **Python**: 3.10.0
- **PyTorch**: CUDA 12.1 build (exact version: check `pip list`)
- **PyTorch Geometric**: Installed via `pip install torch-geometric` (check `pip list` for exact version)
- **XGBoost**: Installed (check `pip list`)
- **scikit-learn**: Installed (check `pip list`)
- **Hardware**: NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM), Intel CPU, Windows

### Seeds
- Global seed: 42 (set via `set_seed(42)`)
- Per-fold seed: 42 + fold_index (0-4)
- KFold random_state: 42

### Reproducibility Checklist

| Item | Path / Value | Status |
|:---|:---|:---|
| Raw NHANES data | `NHANES AUG'21 - AUG'23/` (LABORATORY/, EXAMINATION/, QUESTIONNAIRE/, DEMO G/) | âœ… |
| Ingestion script | `src/dataset.py` | âœ… |
| Cohort construction | `src/cohort.py` | âœ… |
| Target computation | `src/target.py` | âœ… |
| Feature manifest | `data/feature_manifest.json` | âœ… |
| Leakage audit | `src/leakage_audit.py` â†’ `data/leakage_audit_results.json` | âœ… |
| Graph builder | `src/graph_builder.py` â†’ `graphs/patient_graphs.pt` | âœ… |
| HSGIN model | `src/models/hsgin.py` | âœ… |
| Baselines | `src/models/baselines.py` | âœ… |
| Pipeline/preprocessing | `src/pipeline.py` | âœ… |
| Training orchestrator | `src/train.py` | âœ… |
| Ablation study | `src/ablation.py` | âœ… |
| Y-randomization | `src/y_randomization.py` | âœ… |
| Final results JSON | `data/experiment_results.json` | âœ… |
| Model checkpoints | NOT saved (models evaluated in-memory) | âš ï¸ |
| Cohort CSV | `data/final_cohort.csv` (N=6,277) | âœ… |
| Master patient CSV | `data/master_patient.csv` | âœ… |

**To reproduce**: `cd "c:\Users\admin_fix\Downloads\3 ORGAN" && python src/train.py`

---

# 18. Current Results: What We Can Actually Claim

### VERIFIED / DEFENSIBLE
- HSGIN achieves RÂ²=0.4976Â±0.0285 on 5-fold CV for FIB-4 prediction using 25 non-FIB-4 features
- HSGIN outperforms XGBoost by +0.0457 RÂ² and Classical HGNN by +0.0295 RÂ² on the same folds
- Adding Kidney and Heart features to Liver-only features increases XGBoost RÂ² by +0.2572 (tabular ablation)
- Y-randomization yields RÂ²â‰ˆ0, supporting absence of direct mathematical target leakage under Experiment 3
- The cohort contains N=6,277 NHANES patients with complete FIB-4 inputs and baseline kidney/cardio markers

### INTERPRETATION (reasonable but not directly proven)
- The organ-aware readout in HSGIN (patient + organ-pool + biomarker concatenation) may contribute to its advantage over patient-only readout (Classical HGNN)
- Multi-organ features likely carry complementary information about systemic health relevant to liver fibrosis risk
- The heterogeneous graph structure may help the model learn feature interactions that flat tabular models miss

### NOT YET PROVEN (must NOT appear as conclusions)
- âŒ Biological causality between organ systems
- âŒ Mechanistic organ-to-organ crosstalk
- âŒ Clinical utility or diagnostic validity
- âŒ HSGIN-specific organ synergy (ablation was XGBoost-based)
- âŒ Statistical significance of performance differences (no hypothesis testing)
- âŒ Generalization beyond NHANES US population
- âŒ Five-organ validation (Brain and Gut not included)
- âŒ Superiority over existing clinical FIB-4 assessment methods
- âŒ Absence of all forms of indirect leakage

---

# 19. Limitations

1. **Only 3 organ domains validated** (Liver, Kidney, Heart). Brain and Gut are absent.
2. **NHANES-specific population**: US-representative but may not generalize to other demographics/populations.
3. **FIB-4 is itself a derived target**: It is a mathematical combination of Age, AST, ALT, Platelets â€” not a direct biological measurement. Predicting a derived score is fundamentally different from predicting true liver fibrosis.
4. **Leakage control â‰  causality**: Removing FIB-4 inputs controls direct algebraic leakage but does not establish that predictions reflect genuine biological organ interactions vs. confounded statistical associations.
5. **Aâ€“D ablation is tabular (XGBoost)**: Cannot attribute organ-level contributions specifically to HSGIN's graph attention mechanism.
6. **No formal significance testing**: Performance differences are not statistically validated.
7. **Observational, cross-sectional data**: No temporal/longitudinal component. Cannot establish temporal precedence or causal direction.
8. **Potential confounding**: Included features may share unmeasured confounders with excluded FIB-4 components.
9. **Missingness**: Some features have up to 13.99% missing data (KIQ022, MCQ160C, MCQ160E), handled by median imputation which may introduce bias.
10. **No external validation**: Results are internal to NHANES Aug 2021â€“Aug 2023.
11. **No model checkpoints saved**: Models cannot be loaded for post-hoc analysis without retraining.
12. **No clinical validation**: Predictions have not been compared against biopsy-confirmed fibrosis staging.
13. **Feature selection was manual**: No automated feature selection or sensitivity analysis was performed.

---

# 20. Five-Organ Research Vision

### CURRENT VALIDATED (3 organs)
Liver + Kidney + Heart/Cardiovascular â€” fully implemented, trained, and evaluated.

### FUTURE EXTENSION (2 organs)
- **Gut**: Would require gut microbiome composition data (e.g., 16S rRNA, shotgun metagenomics) linked to patient SEQN. NHANES does not currently provide this. Alternative: integrate with external gut microbiome cohorts that share demographic overlap.
- **Brain**: Would require neuroimaging (MRI volumetrics, white matter hyperintensities) or validated cognitive assessment scores. NHANES provides limited cognitive screening (CERAD, Animal Fluency, Digit Symbol) in older adults only. These could be explored as a partial brain proxy in future work.

Adding Brain/Gut nodes would extend the HeteroData schema with new node types, new edge types (patientâ†”gut, patientâ†”brain, gutâ†”liver, brainâ†”heart, etc.), and new feature vectors.

---

# 21. Poster-Ready Scientific Story

- **1-sentence problem**: Can multi-organ biomarker interactions predict liver fibrosis risk without using the target score's own mathematical components?
- **1-sentence method**: We model each patient as a heterogeneous graph with organ-specific nodes (Liver, Kidney, Heart, Biomarker) and train a GAT-based graph neural network (HSGIN) on N=6,277 NHANES patients.
- **1-sentence result**: HSGIN achieves RÂ²=0.4976 for leakage-controlled FIB-4 prediction, outperforming XGBoost (RÂ²=0.4519) and Classical HGNN (RÂ²=0.4681).
- **1-sentence significance**: Multi-organ feature integration demonstrates substantial incremental predictive value (+0.2572 RÂ² over liver-only features) for systemic liver health assessment.

**Recommended title**: "HSGIN: Heterogeneous Systemic Graph Interaction Network for Multi-Organ Liver Fibrosis Risk Prediction"

**Recommended figure sequence**: (1) Cohort flow diagram, (2) HeteroData graph schema, (3) HSGIN architecture diagram, (4) Bar chart of RÂ² across all models, (5) Aâ€“D ablation Î”RÂ² waterfall chart, (6) Y-randomization comparison

**Numbers safe for poster**: All values from experiment_results.json. All Î”RÂ² from ablation. Y-randomization RÂ²â‰ˆ0.

**Claims that should NOT be on poster**:
- "Proves biological organ crosstalk"
- "Clinically validated"
- "Zero target leakage" (say "controlled" instead)
- "5-organ validation"
- "Statistically significant improvement"

---

# 22. Supervisor / HG Handover

### What is finished
- Phase 1: Data ingestion, audit, cohort locking, target verification
- Phase 2: Full 5-fold CV of all models, tabular ablation, Y-randomization
- All results saved to JSON and documented in reports

### What is verified
- Cohort integrity (N=6,277, unique SEQN, valid FIB-4)
- Feature manifest (25 non-leaky features locked)
- Leakage audit (3 experiments completed)
- All model metrics (stored in experiment_results.json)

### What files exist
- `data/`: experiment_results.json, feature_manifest.json, leakage_audit_results.json, fib4_target_validation.json, final_cohort.csv, master_patient.csv, cohort_flow.csv, missingness_report.csv, ingestion_summary.csv
- `graphs/`: patient_graphs.pt (6,277 HeteroData objects)
- `src/`: dataset.py, audit.py, cohort.py, target.py, leakage_audit.py, graph_builder.py, pipeline.py, train.py, ablation.py, y_randomization.py
- `src/models/`: hsgin.py, baselines.py
- `reports/`: experiment_report.md, dataset_report.md, leakage_audit_report.md, Phase_1_Technical_Handoff.md, Master_Audit_Report_Handoff.md

### What should NOT be changed
- Feature manifest (Experiment 3 locked)
- Cohort filtering logic
- FIB-4 formula / target computation
- Excluded features set {RIDAGEYR, LBXSASSI, LBXSATSI, LBXPLTSI}

### What can still be improved
- Run HSGIN-specific organ ablation (mask organ nodes/edges in the graph)
- Add formal statistical significance testing (bootstrap CIs)
- Save model checkpoints for post-hoc analysis
- Hyperparameter tuning (hidden_dim, heads, epochs, lr)
- Add epoch-level progress logging with timestamps

### What experiments are optional but valuable
- HSGIN-specific graph ablation (drop organ nodes/edges)
- Feature importance / attention weight analysis
- Repeated CV with multiple random seeds
- External validation on a different NHANES cycle

### What the next researcher should do first
1. Read this report and `data/experiment_results.json`
2. Verify reproducibility by re-running `python src/train.py`
3. Decide whether HSGIN-specific organ ablation is needed for the publication claim

---

# 23. Exact Final Project Status

| Component | Status |
|:---|:---|
| Dataset | âœ… Complete (27 XPT files ingested, SEQN-verified) |
| Cohort | âœ… Locked (N=6,277, sequential inclusion filtering) |
| Target | âœ… Verified (FIB-4, mean=1.059, validation gates passed) |
| Leakage audit | âœ… Complete (3 experiments, Exp3 locked) |
| Graph | âœ… Built (6,277 HeteroData objects, 5 node types, 14 edge types) |
| HSGIN | âœ… Trained & evaluated (5-fold CV, RÂ²=0.4976) |
| Baselines | âœ… Complete (Ridge, RF, XGBoost, MLP, Classical HGNN) |
| Ablation | âœ… Complete (Aâ€“D XGBoost tabular; HSGIN-specific ablation NOT done) |
| Y-randomization | âœ… Complete (RÂ²=âˆ’0.028, supports no direct leakage) |
| Validation | âš ï¸ Internal only (no external validation) |
| Poster readiness | âš ï¸ Numbers ready; claims require careful scientific phrasing |
| Remaining work | HSGIN graph ablation, significance testing, external validation |

---

# 24. Appendix

### A. Complete Metric Tables
See `data/experiment_results.json` for exact float values.
See `data/leakage_audit_results.json` for all 3-experiment Ã— 4-model results.

### B. Artifact Inventory

| Artifact | Path | Size |
|:---|:---|:---|
| Master patient table | data/master_patient.csv | 11.5 MB |
| Final cohort | data/final_cohort.csv | 8.2 MB |
| Feature manifest | data/feature_manifest.json | 5.0 KB |
| Experiment results | data/experiment_results.json | 3.6 KB |
| Leakage audit results | data/leakage_audit_results.json | 6.1 KB |
| FIB-4 validation | data/fib4_target_validation.json | 570 B |
| Cohort flow | data/cohort_flow.csv | 451 B |
| Missingness report | data/missingness_report.csv | 2.7 KB |
| Ingestion summary | data/ingestion_summary.csv | 1.7 KB |
| Patient graphs | graphs/patient_graphs.pt | 19.4 MB |

### C. Glossary

| Term | Definition |
|:---|:---|
| HSGIN | Heterogeneous Systemic Graph Interaction Network |
| FIB-4 | Fibrosis-4 Index: (AgeÃ—AST)/(PlateletsÃ—âˆšALT) |
| HeteroData | PyTorch Geometric heterogeneous graph data object |
| GATConv | Graph Attention Network convolution layer |
| HeteroConv | PyG wrapper for applying different convolutions per edge type |
| SEQN | NHANES unique respondent sequence number |
| Fold-safe | Preprocessing fitted only on training fold data |

### D. Known Discrepancies

| Item | Discrepancy | Resolution |
|:---|:---|:---|
| Cohort N in missingness_report.csv | Reports N=6,282 (pre-kidney filter) | Final cohort is N=6,277 after Step 5. Missingness report was generated at Step 4. feature_manifest.json cohort_missing_pct values are from the 6,282 pre-filter stage. Authoritative N=6,277 from cohort_flow.csv and fib4_target_validation.json. |
| HSGIN dropout | Model default=0.2 (hsgin.py:49) vs train.py passes 0.1 | train.py:51 overrides: `HSGIN(..., dropout=0.1)`. Actual training used 0.1. |

---

# "ONE-PAGE MEMORY OF THE PROJECT"

**HSGIN 3-Organ Disease Modeling Pipeline â€” Technical Reference Card**

**Problem**: Predict continuous FIB-4 liver fibrosis score from non-FIB-4 multi-organ biomarkers.
**Data**: NHANES August 2021â€“August 2023. **N=6,277** patients linked via SEQN across 27 XPT files.
**Target**: FIB-4 = (AgeÃ—AST)/(PlateletsÃ—âˆšALT). Mean=1.059, Median=0.903, Skew=2.92.
**Leakage Solution**: Exclude all 4 algebraic FIB-4 inputs (Age, AST, ALT, Platelets) from model features. Verified via 3-experiment audit: Exp1 RÂ²=0.93 (leaky) â†’ Exp3 RÂ²=0.44 (controlled). Locked Experiment 3.
**Organs**: Liver (6 feats) + Kidney (6 feats) + Heart (8 feats) + Demographics (1) + Biomarker (4) = **25 features**. Brain/Gut deferred (no NHANES data).
**Graph**: Per-patient HeteroData with 5 node types, 14 edge types (patientâ†”organ bidirectional + organâ†”organ bidirectional).
**HSGIN**: 2-layer GATConv (heads=2) via HeteroConv + residual connections + organ-aware readout (patient âˆ¥ organ-pool âˆ¥ biomarker) â†’ MLP â†’ scalar. SmoothL1Loss, AdamW lr=0.001, batch=64, 50 epochs/fold.
**Baselines**: Ridge (RÂ²=0.387), RF (0.394), XGBoost (0.452), MLP (0.132), Classical HGNN (0.468).
**CV**: 5-fold patient-level, fold-safe median imputation + z-score standardization.
**Final HSGIN**: **RÂ²=0.4976Â±0.0285**, MAE=0.3509Â±0.0091, RMSE=0.5478Â±0.0287. Î”RÂ² vs XGBoost: +0.046. Î”RÂ² vs HGNN: +0.030.
**Ablation (XGBoost tabular)**: Liver-only RÂ²=0.195 â†’ +Kidney RÂ²=0.338 (+0.143) â†’ +Heart RÂ²=0.360 (+0.165) â†’ Full 3-Organ RÂ²=0.452 (+0.257).
**Y-Randomization**: RÂ²=âˆ’0.028Â±0.029 (â‰ˆ0). Supports absence of direct mathematical target leakage.
**Key Conclusion**: Multi-organ features demonstrate incremental predictive value for FIB-4 estimation. HSGIN's heterogeneous graph architecture outperforms tabular and homogeneous graph baselines under the leakage-controlled configuration.
**Limitations**: No causal claims. No HSGIN-specific ablation. No significance testing. No external validation. No clinical validation. Observational cross-sectional data only. 3/5 organs validated.
**5-Organ Future**: Integrate gut microbiome + neuroimaging/cognitive data to complete Liver+Kidney+Heart+Gut+Brain vision.
