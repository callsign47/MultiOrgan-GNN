# PRD: Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural Network Approaches for Leakage-Controlled FIB-4 Score Prediction Using Multi-Organ Clinical Features

Product Requirements Document, version 1.1 (for technical review; owner-provided values pending repository verification; see Appendix A for the change log)

## 1. Document Overview

| Field | Value |
| --- | --- |
| Project title | A Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural Network Approaches for Leakage-Controlled FIB-4 Score Prediction Using Multi-Organ Clinical Features |
| Document type | Implementation-oriented Product Requirements Document |
| Intended reviewers | Technical research guide, ML engineer, bioinformatics researcher |
| Data source | NHANES August 2021 to August 2023 cycle |
| Cohort (existing) | 6,277 participants, integrated from 27 NHANES XPT files, joined on SEQN |
| Predictor set (existing, locked) | 25 features |
| Target | Continuous FIB-4 score |
| Status of this document | Blueprint. Describes existing work and proposed work separately |

### 1.1 Governing Constraint: Extend, Never Replace

This project is an evolution of an existing, partially completed research implementation. It is not a fresh project and must not be rebuilt from scratch. The following rule governs every requirement in this document:

**Extend the existing project; never destroy or silently replace its original research implementation.**

Consequences that apply throughout the document:

- No existing file may be deleted, overwritten, renamed, moved, or structurally modified without explicit written approval.
- The original HSGIN experiment must remain independently executable.
- New results are never written over original results.
- If any requirement here conflicts with a preserved asset, work stops and approval is requested.

### 1.2 Evidence Labeling Convention

Every claim in this document carries one of three labels, used consistently:

| Label | Meaning |
| --- | --- |
| EXISTING-REPORTED | Reported in prior work. Not independently reproduced in this project yet |
| PROPOSED | A planned experiment or component. No result exists |
| UNKNOWN | Technical information that is missing and must be supplied, not guessed |

No experimental result appears in this document unless it is labeled EXISTING-REPORTED. Values supplied by the project owner but not yet checked against the repository are labeled USER-PROVIDED (UNVERIFIED) and must not be treated as verified.

## 2. Executive Summary

The project asks how much continuous FIB-4 variance can be explained when the four direct formula components (Age, AST, ALT, Platelet Count) are removed from the predictor matrix, using 25 non-direct multi-organ clinical features from NHANES.

The earlier phase developed HSGIN, a heterogeneous graph attention network, and reported an R2 of 0.4976 under five-fold patient-level cross-validation, against 0.4519 for XGBoost and 0.4681 for a classical heterogeneous GNN (EXISTING-REPORTED). The project is now repositioned as a comparative benchmarking study. HSGIN is one competitor among linear models, tree ensembles, gradient boosting, deep tabular models, graph models, and ensembles.

The deliverable is a controlled, reproducible comparison with identical folds, training-fold-only preprocessing, leakage audits, uncertainty estimates, and explicit limitations. An exploratory R2 target range of 0.60 to 0.70 is stated as an aspiration only. It is not an acceptance criterion and must never motivate leakage or selective reporting.

## 3. Research Background

### 3.1 FIB-4

FIB-4 is a non-invasive index used in clinical practice to estimate the likelihood of advanced liver fibrosis:

```latex
\text{FIB-4} = \frac{\text{Age} \times \text{AST}}{\text{Platelet Count} \times \sqrt{\text{ALT}}}
```

Conventional clinical units: Age in years, AST and ALT in U/L, platelet count in 10^9/L. These are the standard definitions of the formula only. The units and any rescaling used by the existing pipeline are UNKNOWN until verified from the original pipeline code and the raw variable definitions (Section 12.2). They must never be assumed.

Because the target is a deterministic function of four variables, any model given those four variables can reconstruct it almost exactly. This is direct mathematical target leakage and makes R2 meaningless as a measure of information content in the remaining features.

### 3.2 Why the Leakage-Controlled Setting Matters

With the four components removed, the prediction task becomes: do other organ-system measurements (the organ systems represented in the verified manifest, whose names are UNKNOWN until Section 12.3 is completed) carry recoverable information about a score that is computed from hepatic enzymes, platelets, and age? The achievable R2 is bounded by shared physiology and correlated risk factors, not by algebra. This is the scientifically interesting quantity.

### 3.3 NHANES Context

NHANES is a cross-sectional US survey combining interview, examination, and laboratory components. Modules are distributed as SAS transport (XPT) files keyed by SEQN. The 2021 to 2023 cycle was integrated from 27 XPT files into a single patient-level table (EXISTING-REPORTED).

## 4. Problem Statement

1. Prior reported results compare HSGIN against a small set of baselines, and the MLP baseline (R2 0.1320) is far below the others. This suggests the baseline set is not yet tuned or complete enough to support strong claims about graph models.
2. Modern strong tabular learners (CatBoost, LightGBM, Extra Trees, HistGradientBoosting, FT-Transformer) and ensembles have not been evaluated.
3. Reported results have not been independently reproduced within a versioned, auditable framework.
4. Uncertainty estimates and paired statistical comparisons are absent, so differences such as 0.4976 versus 0.4681 cannot yet be called meaningful.
5. The project risks drifting toward chasing an R2 number rather than answering a clean scientific question.

## 5. Research Motivation

- Scientific: quantify cross-organ information about a liver-fibrosis index without its direct inputs.
- Methodological: provide a template for leakage-controlled benchmarking of computed clinical indices.
- Practical: determine whether the added complexity of graph models is justified over gradient boosting on tabular data, where boosting often remains very competitive.
- Integrity: establish a protocol in which a negative or modest result is reportable and defensible.

## 6. Research Objectives

To systematically evaluate and compare conventional machine learning, ensemble learning, deep learning, and graph neural network architectures for continuous FIB-4 score prediction using non-direct, multi-organ clinical features, while preventing direct mathematical target leakage.

Specific objectives:

| ID | Objective |
| --- | --- |
| O1 | Identify which model family performs best under identical folds and preprocessing |
| O2 | Test whether graph architectures give a measurable advantage over strong tabular baselines |
| O3 | Test whether ensembling improves predictive performance |
| O4 | Identify which organ-specific feature domains contribute most |
| O5 | Assess consistency of performance across folds and repeats |
| O6 | Estimate how much FIB-4 variance is explainable without its direct components |
| O7 | Reproduce the existing baseline inside the new framework without altering it |

## 7. Research Questions and Hypotheses

| ID | Research question | Hypothesis (to be tested, not assumed) | Falsified if |
| --- | --- | --- | --- |
| RQ1 | Which model family is best? | Gradient boosting variants will cluster near XGBoost; differences among them will be small | A family differs from the others with paired CI excluding zero in the opposite direction |
| RQ2 | Do graph models add value? | HSGIN will remain at or modestly above the best tabular model | Best tabular model matches or exceeds HSGIN within uncertainty |
| RQ3 | Does ensembling help? | Stacking over diverse families will yield a small, consistent gain | Gain is within fold-to-fold noise |
| RQ4 | Which feature domains matter? | Domains defined from the verified manifest differ in contribution. Which domain dominates is not pre-specified and is determined by ablation | Domain ablation shows no domain with a significant drop |
| RQ5 | Is performance stable? | Fold standard deviation will be small relative to between-model gaps | Fold SD is comparable to between-model gaps |
| RQ6 | How much variance is explainable? | Best valid R2 will be below the 0.60 aspiration unless new information is added | Valid R2 at or above 0.60 with all leakage audits passing |

The hypotheses are deliberately stated so that either outcome is publishable.

## 8. Scope and Out-of-Scope

### 8.1 In Scope

- Reproduction of the existing baseline (Experiment 0).
- Benchmarking of the model families listed in Section 10.
- Leakage audit, Y-randomization, ablations, subgroup and robustness analysis.
- Explainability appropriate to each model family.
- External validation if a suitable dataset is available.

### 8.2 Out of Scope

| Item | Reason |
| --- | --- |
| Diagnosing liver fibrosis | No independent clinical reference standard (biopsy or elastography) |
| Causal or mechanistic biological claims | Attention and SHAP are predictive attributions only |
| Deployment, serving, APIs, dashboards | Not justified by research scope |
| Reintroducing Age, AST, ALT, or Platelet Count as predictors in primary experiments | Defeats the study design |
| Changing the cohort, target formula, or locked feature set silently | Prohibited by the governing constraint |

An optional, clearly separated sensitivity analysis that includes the four components may be run solely to demonstrate leakage behavior (see Experiment 8). It must never be reported as a predictive result.

## 9. Existing System and Baseline

### 9.1 HSGIN Architecture (EXISTING-REPORTED)

| Component | Specification |
| --- | --- |
| Message passing | Two heterogeneous GATConv layers |
| Attention heads | 2 |
| Hidden dimension | 64 |
| Skip connections | Residual |
| Readout | Organ-aware readout |
| Head | MLP regression head |
| Loss | SmoothL1 (Huber) |
| Optimizer | AdamW, learning rate 0.001 |
| Validation | Five-fold patient-level cross-validation |

### 9.2 Existing Reported Results (EXISTING-REPORTED, not independently reproduced)

| Model | MAE | RMSE | R2 | Fold SD | Status |
| --- | --: | --: | --: | --: | --- |
| Ridge Regression | 0.4065 | 0.6058 | 0.3869 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |
| Random Forest | 0.3927 | 0.6019 | 0.3940 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |
| XGBoost | 0.3740 | 0.5728 | 0.4519 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |
| MLP | 0.4679 | 0.7204 | 0.1320 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |
| Classical HGNN | 0.3648 | 0.5641 | 0.4681 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |
| HSGIN | 0.3509 | 0.5478 | 0.4976 | UNKNOWN | USER-PROVIDED (UNVERIFIED), fold means |

MAE and RMSE were supplied by the project owner as means across folds and are USER-PROVIDED (UNVERIFIED). Consistency check: RMSE squared divided by one minus R2 gives an implied target variance of about 0.598 (SD about 0.773) for all six models, so the values appear to share one target scale. This does not establish whether that scale is raw FIB-4 or a transformed target. They must be extracted from the original results files, with their units (the target scale used by the original pipeline, UNKNOWN until verified) and whether they are fold means or pooled values. They are entered as EXISTING-REPORTED only if the original outputs contain them. If the original outputs do not contain them, the cells read NOT REPORTED, the values are computed fresh in Experiment 0 and labeled REPRODUCED, and they are never back-filled into this table as if they had been reported. The R2 convention (mean of fold R2 or pooled out-of-fold R2) is also UNKNOWN and must be confirmed.

Existing validation: patient-level five-fold CV; fold-safe median imputation and standardization; direct components excluded; Y-randomization R2 approximately -0.0281; XGBoost feature ablation; HSGIN architectural ablation.

### 9.3 Observations the Reviewer Should Weigh

- The MLP result (0.1320) is an outlier against Ridge (0.3869). A neural network underperforming a linear model on tabular data usually indicates under-tuning, scaling issues, or insufficient regularization, not an inherent limit. It should be treated as an open question in Experiment 3.
- The HSGIN margin over XGBoost is 0.0457 R2. Without fold-level variance and paired tests, this margin is not established.
- Whether HSGIN and the baselines received equal tuning effort is UNKNOWN and must be documented.
- Whether all baselines used identical fold assignments is UNKNOWN and must be verified.

### 9.4 Protected Assets

Source code and model implementations; original HSGIN architecture and configuration; datasets and processed cohorts; the 25-feature manifest; FIB-4 target construction pipeline; serialized graphs; experiment results and evaluation outputs; leakage audit and Y-randomization results; checkpoints; documentation, notebooks, logs, and visualizations.

### 9.5 Existing Checkpoint Status

No saved model checkpoints were previously reported for the existing experiments. The project handover states that models were evaluated in memory and none were saved (USER-PROVIDED, UNVERIFIED). Whether any checkpoint files exist in the repository is UNKNOWN until the audit inspects it. Version 1.0 wording that implied stored weights could be loaded is corrected as follows.

- Inspection (read only): search for weight and model files (for example .pt, .pth, .ckpt, .pkl, .joblib, and serialized model dumps). Record path, size, modification time, and SHA-256 for every hit. If there are none, record "none found" explicitly, with the search patterns used.
- If none exist: "load the original HSGIN model" means instantiating it from preserved code and configuration and retraining under the original protocol. Experiment 0 then reproduces by retraining, and comparison against original predictions is possible only if the original results folder contains stored predictions (UNKNOWN).
- If some exist: they are protected assets and are never overwritten. Their provenance (run, seed, fold, configuration) must be established before use, and checkpoints without provenance are not used for any reported result.
- New checkpoints from the comparative study are written only to new paths.

## 10. Proposed Comparative Framework

### 10.1 Model Families

| Family | Model | Status |
| --- | --- | --- |
| A. Linear | Ridge Regression | Existing, to be reproduced |
| A. Linear | ElasticNet | PROPOSED |
| B. Tree-based | Random Forest | Existing, to be reproduced |
| B. Tree-based | Extra Trees | PROPOSED |
| C. Gradient boosting | XGBoost | Existing, to be reproduced |
| C. Gradient boosting | CatBoost | PROPOSED |
| C. Gradient boosting | LightGBM | PROPOSED |
| C. Gradient boosting | HistGradientBoosting | PROPOSED |
| D. Deep learning | MLP | Existing, to be reproduced and re-tuned as a separate version |
| D. Deep learning | FT-Transformer | PROPOSED |
| D. Deep learning | TabNet | PROPOSED, optional, feasibility dependent |
| E. Graph | Classical heterogeneous GNN | Existing, to be reproduced |
| E. Graph | HSGIN | Existing, to be reproduced |
| F. Ensemble | Stacking Regressor | PROPOSED |
| F. Ensemble | Weighted prediction ensemble | PROPOSED |

### 10.2 Comparison Principles

1. Identical patient-level folds for every model.
2. Identical locked 25-feature input for the primary comparison.
3. Preprocessing fitted on training folds only.
4. Equal and documented tuning budget per model, with tuning confined to inner folds.
5. Same metrics, same plots, same reporting template.
6. Original models are never retuned inside the original experiment record. Any retuned variant is a new, versioned experiment.

### 10.3 Workflow

```
NHANES XPT files -> SEQN join -> cohort + exclusion audit -> FIB-4 target
   -> locked 25-feature matrix (leakage audit gate)
   -> fixed patient-level fold assignment (versioned)
   -> per-fold: fit preprocessing on train -> tune on inner folds -> fit -> predict held-out
   -> out-of-fold predictions saved per model
   -> metrics, paired comparisons, residuals, explainability, ablations
```

## 11. Detailed Model Requirements

Hyperparameter ranges below are PROPOSED starting points to be fixed and recorded in versioned configs before any validation result is viewed.

### 11.1 Linear Models

| Model | Requirements |
| --- | --- |
| Ridge | Alpha chosen by inner CV over a log grid. Standardized inputs |
| ElasticNet | Alpha and l1 ratio chosen by inner CV. Standardized inputs. Report number of non-zero coefficients |

### 11.2 Tree-Based Models

| Model | Requirements |
| --- | --- |
| Random Forest | Number of trees, max depth, min samples leaf, max features tuned within a bounded budget. Fixed seeds |
| Extra Trees | Same search structure as Random Forest for fair comparison |

### 11.3 Gradient Boosting

| Model | Requirements |
| --- | --- |
| XGBoost | Learning rate, depth, subsample, column subsample, regularization, early stopping on an inner validation split only |
| CatBoost | Depth, learning rate, l2 leaf regularization, iterations with early stopping on inner split |
| LightGBM | Num leaves, learning rate, min child samples, feature fraction, early stopping on inner split |
| HistGradientBoosting | Learning rate, max leaf nodes, l2 regularization, early stopping on inner split |

Early stopping must never use the outer held-out fold.

### 11.4 Deep Learning

| Model | Requirements |
| --- | --- |
| MLP | Re-tuned variant explores width, depth, dropout, weight decay, batch norm, learning rate schedule. The original MLP configuration is preserved untouched |
| FT-Transformer | Feature tokenizer, small number of transformer blocks, attention heads and embedding size scaled to a roughly 5,000-row training set, strong regularization, early stopping on inner split |
| TabNet | Optional. Include only if it trains stably under the same protocol. Otherwise record as not feasible with reasons |

With about 5,000 training rows per fold, deep tabular models are at a known disadvantage against boosting. The PRD requires that this be stated in the results rather than treated as a surprise.

### 11.5 Graph Models

| Model | Requirements |
| --- | --- |
| Classical heterogeneous GNN | Reproduce as is |
| HSGIN | Reproduce as is, configuration frozen: two heterogeneous GATConv layers, 2 heads, hidden 64, residual, organ-aware readout, MLP head, SmoothL1, AdamW at 0.001 |

Any HSGIN improvement is a separately versioned experiment and must not replace the original.

### 11.6 Ensembles

| Model | Requirements |
| --- | --- |
| Stacking Regressor | Base learners drawn from diverse families. Meta-learner trained on out-of-fold base predictions generated inside the training fold only (nested). Simple meta-learner such as ridge |
| Weighted ensemble | Weights fitted on inner-fold predictions only. Compare against simple averaging |

## 12. Dataset and Feature Specifications

### 12.1 Cohort

| Item | Specification |
| --- | --- |
| Source | NHANES August 2021 to August 2023 |
| Files | 27 XPT files |
| Key | SEQN |
| Final N | 6,277 (EXISTING-REPORTED) |
| Exclusion audit | UNKNOWN: the stepwise inclusion and exclusion counts must be reconstructed and recorded as a flow table |

### 12.2 Target

FIB-4 computed with the formula in Section 3.1. Requirements:

- Unit handling for age, AST, ALT, and platelets must be verified from the original pipeline code and the raw NHANES variable definitions, never assumed, then documented and tested against an independent recomputation. The conventional units in Section 3.1 describe the formula, not what the existing pipeline did.
- Participants with non-positive ALT or platelet values handled by a documented rule (UNKNOWN whether this was applied in the existing pipeline; must be verified against it, not assumed).
- Target distribution reported (mean, median, skewness, extremes). FIB-4 is typically right-skewed. Whether the existing pipeline transformed the target (for example log transform, clipping, winsorization, or standardization) is UNKNOWN. It must be verified from the original pipeline and recorded before any new model is trained, and the absence of a transformation must not be assumed either.
- Metrics are always reported on the original target scale.

### 12.3 Locked 25-Feature Manifest

The 25 features in Table 12.3a were supplied by the project owner and are USER-PROVIDED (UNVERIFIED). They have not been checked against the repository. The manifest file in the existing project remains the single source of truth and is protected. The list becomes the locked baseline only after the three-source check below passes and the manifest SHA-256 is recorded.

**Verification procedure (required before Experiment 0).** The manifest is accepted only when three independent sources agree:

1. The manifest file in the existing project.
2. The column list of the saved processed feature matrix used for training.
3. The feature selection code or configuration that feeds HSGIN and the baselines.

Checks: exactly 25 names; identical names and order across the three sources; none of Age, AST, ALT, Platelet Count, or any alias of them; every name traceable to an NHANES file and variable; SHA-256 of the manifest file recorded. Any disagreement stops work and is reported, never resolved silently.

Table 12.3a. Manifest as provided by the project owner (UNVERIFIED until the three-source check passes)

| # | Group (owner-provided) | feature\_name | NHANES variable code | Review note | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Demographic | RIAGENDR (sex) | RIAGENDR | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 2 | Liver | GGT | UNKNOWN | Proxy-leakage screen required | USER-PROVIDED (UNVERIFIED) |
| 3 | Liver | Albumin | UNKNOWN | Proxy-leakage screen required | USER-PROVIDED (UNVERIFIED) |
| 4 | Liver | Total Bilirubin | UNKNOWN | Proxy-leakage screen required | USER-PROVIDED (UNVERIFIED) |
| 5 | Liver | ALP | UNKNOWN | Proxy-leakage screen required | USER-PROVIDED (UNVERIFIED) |
| 6 | Liver | Liver Stiffness Median | UNKNOWN | Proxy-leakage screen required; check missing rate | USER-PROVIDED (UNVERIFIED) |
| 7 | Liver | CAP | UNKNOWN | Proxy-leakage screen required; check missing rate | USER-PROVIDED (UNVERIFIED) |
| 8 | Kidney | Creatinine | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 9 | Kidney | BUN | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 10 | Kidney | Uric Acid | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 11 | Kidney | Urine Albumin | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 12 | Kidney | Urine Creatinine | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 13 | Kidney | Kidney History | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 14 | Heart/Cardio | Systolic BP | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 15 | Heart/Cardio | Diastolic BP | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 16 | Heart/Cardio | Pulse | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 17 | Heart/Cardio | HDL | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 18 | Heart/Cardio | Total Cholesterol | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 19 | Heart/Cardio | High BP History | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 20 | Heart/Cardio | Coronary Heart Disease History | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 21 | Heart/Cardio | Heart Attack History | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 22 | Biomarker | WBC | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 23 | Biomarker | RBC | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 24 | Biomarker | Hemoglobin | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |
| 25 | Biomarker | hs-CRP | UNKNOWN | Standard screen | USER-PROVIDED (UNVERIFIED) |

Group counts: Demographic 1, Liver 6, Kidney 6, Heart/Cardio 8, Biomarker 4, total 25.

Leakage note: the six liver features are not direct FIB-4 components, but liver stiffness and CAP measure fibrosis and steatosis directly, and GGT, ALP, albumin, and bilirubin are liver function tests correlated with AST, ALT, and platelets. They must pass the proxy-leakage screen in Section 13.1, and Experiment 6 must report performance with and without the liver group so that readers can see how much of the R2 comes from liver-related measurements. Missing rates (especially for elastography measures) and the effect of median imputation on them must be reported.

Manifest SHA-256: UNKNOWN. Verified by and date: UNKNOWN.

Manifest record schema (PROPOSED, for provenance):

| Field | Description |
| --- | --- |
| feature\_name | Column name in the processed table |
| source\_xpt | NHANES file of origin |
| nhanes\_variable | Original variable code |
| organ\_domain | Organ or system assignment used for graph nodes |
| unit | Measurement unit |
| missing\_rate | Fraction missing in the cohort |
| transformation | Any transformation applied, or none |
| leakage\_review | Reviewer, date, and verdict |

### 12.4 Missing Data

- Median imputation fitted on training folds only (existing protocol, preserved).
- Missingness rates per feature and per fold reported.
- Optional sensitivity experiments (for example missingness indicators, or model-native missing handling in boosting) are separate versioned experiments.

### 12.5 Patient-Level Graph Construction

- One graph per patient, nodes grouped by organ domain, edges encoding the existing relation families.
- Serialized existing graph files are preserved. New graph variants are stored separately.
- Reported schema (user-stated, NOT yet verified against source code): 5 node types and 14 directed edge types. Owner-provided node types: Patient, Liver, Kidney, Heart, Biomarker. Owner-provided directed edges: Patient to and from each of Liver, Kidney, Heart, and Biomarker (8 directed edges), plus Liver, Kidney, and Heart pairwise in both directions (6 directed edges). Biomarker has no direct edge to other organ nodes. Relation names and the node assignment of each feature are UNKNOWN. All of this is USER-PROVIDED (UNVERIFIED) until checked against the source code and a serialized graph (Tables 12.5a and 12.5b).

**Verification procedure.** Extract the schema two ways and require agreement: (a) from the graph construction code in the HSGIN source (node type definitions and every edge type tuple), and (b) from the metadata of a preserved serialized graph (node type list and edge type list). Confirm that the counts are 5 and 14, that directed and reverse edges are counted consistently, and that node feature dimensions sum to the 25 verified features. If the code, the serialized graph, and the stated counts disagree, work stops and the discrepancy is reported.

Table 12.5a. Node types (UNKNOWN until verified)

| # | node\_type | Features assigned | Verified in code | Verified in serialized graph |
| --- | --- | --- | --- | --- |
| 1 | Patient | UNKNOWN | NOT VERIFIED | NOT VERIFIED |
| 2 | Liver | UNKNOWN | NOT VERIFIED | NOT VERIFIED |
| 3 | Kidney | UNKNOWN | NOT VERIFIED | NOT VERIFIED |
| 4 | Heart | UNKNOWN | NOT VERIFIED | NOT VERIFIED |
| 5 | Biomarker | UNKNOWN | NOT VERIFIED | NOT VERIFIED |

Table 12.5b. Directed edge types (UNKNOWN until verified)

| # | source\_node\_type | relation | destination\_node\_type | Verified in code | Verified in serialized graph |
| --- | --- | --- | --- | --- | --- |
| 1 | Patient | UNKNOWN | Liver | NOT VERIFIED | NOT VERIFIED |
| 2 | Liver | UNKNOWN | Patient | NOT VERIFIED | NOT VERIFIED |
| 3 | Patient | UNKNOWN | Kidney | NOT VERIFIED | NOT VERIFIED |
| 4 | Kidney | UNKNOWN | Patient | NOT VERIFIED | NOT VERIFIED |
| 5 | Patient | UNKNOWN | Heart | NOT VERIFIED | NOT VERIFIED |
| 6 | Heart | UNKNOWN | Patient | NOT VERIFIED | NOT VERIFIED |
| 7 | Patient | UNKNOWN | Biomarker | NOT VERIFIED | NOT VERIFIED |
| 8 | Biomarker | UNKNOWN | Patient | NOT VERIFIED | NOT VERIFIED |
| 9 | Liver | UNKNOWN | Kidney | NOT VERIFIED | NOT VERIFIED |
| 10 | Kidney | UNKNOWN | Liver | NOT VERIFIED | NOT VERIFIED |
| 11 | Liver | UNKNOWN | Heart | NOT VERIFIED | NOT VERIFIED |
| 12 | Heart | UNKNOWN | Liver | NOT VERIFIED | NOT VERIFIED |
| 13 | Kidney | UNKNOWN | Heart | NOT VERIFIED | NOT VERIFIED |
| 14 | Heart | UNKNOWN | Kidney | NOT VERIFIED | NOT VERIFIED |

## 13. Leakage-Control Strategy

### 13.1 Leakage Taxonomy

| Type | Description | Control | Validation test |
| --- | --- | --- | --- |
| Direct formula leakage | Age, AST, ALT, or Platelet Count in the predictor matrix | Locked manifest with explicit exclusion list | Automated assertion that none of the four names or aliases appear in any feature matrix at fit time |
| Derived leakage | Engineered feature algebraically or near-algebraically reconstructs a component (for example a ratio containing platelets) | Feature provenance record and review | Reconstruction test: regress each excluded component on the full feature set and flag features with near-deterministic relationships |
| Proxy leakage | Variable that is a near duplicate of an excluded component (for example another liver enzyme panel measurement or an age-derived variable) | Domain review of the 25 features and any added feature | Correlation screen against each component, with a documented threshold and manual review of flagged features |
| Preprocessing leakage | Imputation, scaling, or selection fitted on the full dataset | Pipelines fitted on training folds only | Unit test that fitted statistics differ across folds and match training-only recomputation |
| Patient overlap | Same SEQN in training and held-out data | Fold assignment keyed on SEQN | Assertion of empty intersection per fold |
| Tuning leakage | Hyperparameters or early stopping chosen using the outer held-out fold | Nested or inner-fold tuning only | Code audit plus log check that outer-fold labels are never read during tuning |
| Target-derived leakage | Any feature computed from the target or its components | Provenance review | Manifest review sign-off |

### 13.2 Leakage Gate

No model may be trained until the leakage gate passes. The gate produces a signed report containing the manifest hash, exclusion assertion result, reconstruction test result, proxy screen result, and fold-overlap assertion result. Any change to the manifest changes its hash and requires a new gate report and a new experiment version.

### 13.3 Sensitivity Analysis

Experiment 8 includes a deliberately leaky run (components added) to confirm that the framework would detect near-perfect R2 and to demonstrate the size of the leakage effect. These results are labeled as leakage demonstrations and are excluded from all comparative tables.

## 14. Experimental Design

All experiments use the same cohort, target, locked 25-feature set (unless the experiment states otherwise), and identical patient-level fold assignment.

### Experiment 0: Reproduce the Existing Baseline

| Item | Specification |
| --- | --- |
| Objective | Verify that reported results can be reproduced from the preserved code and data |
| Hypothesis | Reproduced R2 values fall within seed-level variability of the reported values |
| Inputs | Preserved code, data, manifest, configs, original fold assignment if recoverable |
| Exclusions | No retuning, no architectural change |
| Methodology | Run original entry points unmodified. Record seeds, library versions, hardware. Repeat with several seeds |
| Metrics | R2, MAE, RMSE per fold, mean and SD, compared with reported values |
| Outputs | Reproduction report, reproduced OOF predictions saved under a new results path |
| Acceptance | Each reproduced mean R2 within a pre-declared tolerance of the reported value, or discrepancies documented and explained |
| Failure conditions | Original folds not recoverable, missing seeds, version drift. Outcome in that case: document and treat reproduced numbers as the new baseline with the original numbers retained as reported only |

### Experiment 1: Linear and Conventional ML

| Item | Specification |
| --- | --- |
| Objective | Establish strong low-complexity baselines |
| Hypothesis | ElasticNet is comparable to Ridge. Extra Trees is comparable to Random Forest |
| Inputs | Locked 25 features |
| Exclusions | Four formula components, engineered features |
| Methodology | Ridge, ElasticNet, Random Forest, Extra Trees with inner-fold tuning |
| Metrics | R2, MAE, RMSE, fold-wise, mean and SD |
| Outputs | OOF predictions, tuned configs, metric tables |
| Acceptance | All models complete all folds with logged configs and seeds |
| Failure conditions | Non-convergence, unstable fold results, tuning budget unequal across models |

### Experiment 2: Advanced Boosting

| Item | Specification |
| --- | --- |
| Objective | Determine the ceiling of gradient boosting on the locked features |
| Hypothesis | CatBoost, LightGBM, and HistGradientBoosting are within noise of XGBoost |
| Inputs | Locked 25 features |
| Methodology | Equal tuning budget, inner-fold early stopping |
| Metrics | As Experiment 1 |
| Outputs | OOF predictions, tuned configs, learning curves |
| Acceptance | Equal budgets documented, no outer-fold use in tuning |
| Failure conditions | Early stopping on held-out fold, budget imbalance favoring one library |

### Experiment 3: Deep Learning

| Item | Specification |
| --- | --- |
| Objective | Determine whether the weak original MLP reflects tuning or an inherent limit, and evaluate FT-Transformer and optional TabNet |
| Hypothesis | A properly regularized MLP substantially exceeds 0.1320 R2 but remains below boosting |
| Methodology | Re-tuned MLP as a new version, FT-Transformer, TabNet if feasible. Multiple seeds. Fixed epoch and early-stopping rules |
| Metrics | As Experiment 1, plus seed variance |
| Outputs | OOF predictions, training curves, seed variance table |
| Acceptance | Training stability documented, seed variance reported |
| Failure conditions | Divergence, severe seed sensitivity, TabNet infeasible (reported as such) |

### Experiment 4: Graph Neural Networks

| Item | Specification |
| --- | --- |
| Objective | Compare classical heterogeneous GNN and HSGIN against the best tabular models |
| Hypothesis | HSGIN is at or modestly above the best tabular model |
| Methodology | Original configurations frozen. Multiple seeds |
| Metrics | As Experiment 1, plus seed variance |
| Outputs | OOF predictions, attention exports, seed variance table |
| Acceptance | Same folds and preprocessing as other models |
| Failure conditions | Different folds, different preprocessing, undocumented tuning difference |

### Experiment 5: Ensemble Learning

| Item | Specification |
| --- | --- |
| Objective | Test whether combining diverse families improves accuracy |
| Hypothesis | Stacking yields a small but consistent gain over the best single model |
| Methodology | Nested stacking with out-of-fold base predictions inside the training fold. Weighted ensemble with weights from inner folds |
| Metrics | As Experiment 1, plus diversity measure (correlation of OOF residuals between base models) |
| Outputs | Ensemble OOF predictions, meta-learner coefficients |
| Acceptance | No outer-fold information used in meta-learner training |
| Failure conditions | Meta-learner fitted on predictions that saw held-out labels |

### Experiment 6: Feature-Domain Ablation

| Item | Specification |
| --- | --- |
| Objective | Quantify the contribution of each organ-specific feature domain |
| Hypothesis | Domains defined from the verified manifest differ in contribution. The domain with the largest drop is identified by the ablation, not pre-specified |
| Methodology | Leave-one-domain-out and single-domain-only runs using the best tabular model and HSGIN. Same folds |
| Metrics | Change in R2 with paired uncertainty |
| Outputs | Domain contribution table and plot |
| Acceptance | Domain definitions come from the manifest, fixed before running |
| Failure conditions | Domain assignment changed after seeing results |

### Experiment 7: Graph Architecture Ablation

| Item | Specification |
| --- | --- |
| Objective | Identify which graph components matter |
| Hypothesis | Organ-aware readout and the relation families each contribute measurable changes. Effect sizes and their ordering are not pre-specified and depend on the verified 14 directed edge types |
| Methodology | Ablate node types, relation families, residual connections, readout, and attention heads as separately versioned variants. Include a graph with randomized edges as a control |
| Metrics | Change in R2 with paired uncertainty |
| Outputs | Ablation table |
| Acceptance | Original HSGIN untouched, each variant versioned |
| Failure conditions | Variants tuned more heavily than the original |

### Experiment 8: Y-Randomization and Leakage Controls

| Item | Specification |
| --- | --- |
| Objective | Confirm that performance is not an artifact of leakage or pipeline error |
| Hypothesis | Shuffled-target R2 is near or below zero for every model |
| Methodology | Repeated target permutation (many permutations, not one) for every top model. Leaky sensitivity run with components included, for demonstration only. Feature shuffling control |
| Metrics | Permutation R2 distribution per model, empirical p-value |
| Outputs | Null distributions, leakage demonstration report |
| Acceptance | Null R2 centered near zero. Leaky run clearly separable |
| Failure conditions | Positive R2 under shuffled targets, which indicates a pipeline defect and halts all reporting |

### Experiment 9: Robustness and Subgroup Analysis

| Item | Specification |
| --- | --- |
| Objective | Assess stability across seeds, folds, and subgroups |
| Hypothesis | Performance varies across subgroups and is lowest at the extremes of FIB-4 |
| Methodology | Repeated cross-validation with new seeds. Performance across FIB-4 ranges (for example below 1.3, 1.3 to 2.67, above 2.67 as commonly used clinical bands) and across subgroups defined from variables available in the cohort (for example sex or age bands, used only to define subgroups and never as predictors) where group size permits. Minimum group size declared in advance |
| Metrics | Metrics with confidence intervals per subgroup |
| Outputs | Subgroup tables, calibration-style residual plots |
| Acceptance | Groups below the minimum size are reported as not evaluable, not pooled silently |
| Failure conditions | Subgroups defined after seeing results |

### Experiment 10: External Validation (Conditional)

| Item | Specification |
| --- | --- |
| Objective | Test generalization on an independent dataset |
| Hypothesis | Performance declines relative to internal cross-validation |
| Methodology | Apply frozen trained pipelines to an external cohort with the same feature definitions. Candidate datasets are UNKNOWN and must be identified and checked for feature comparability |
| Metrics | As Experiment 1 |
| Acceptance | Run only if a dataset with all 25 features or documented equivalents exists |
| Failure conditions | Feature mismatch, different assay methods. If not met, state that no external validation was performed |

## 15. Training and Evaluation Methodology

### 15.1 Cross-Validation

- Primary: five-fold patient-level CV, fold assignment generated once, stored, hashed, and reused by every model.
- Recommended addition: repeated five-fold CV (for example several repeats with different seeds) to estimate variability beyond a single partition.
- Hyperparameter tuning: inner cross-validation within each outer training set (nested CV) for all models, with a bounded and equal budget.
- Stratification: consider stratifying folds on target quantile bins to balance the right-skewed target. Whether the existing folds were stratified is UNKNOWN. Any change in splitting is recorded as a new fold version and never replaces the original.

### 15.2 Preprocessing

Median imputation and standardization are fitted on training data of each fold and applied to its held-out data. Tree-based models may skip standardization but must use the same imputation for comparability, unless a documented native-missing-value variant is run separately.

### 15.3 Reproducibility

| Element | Requirement |
| --- | --- |
| Seeds | Fixed and logged for NumPy, Python, PyTorch, and library-specific RNGs |
| Determinism | Deterministic algorithms enabled where possible. Non-deterministic GPU operations documented |
| Configs | One versioned file per experiment and model, stored in the experiment record |
| Checkpoints | Saved per model, fold, and seed with config hash |
| Logs | Training logs, library versions, hardware, run time |
| Environment | Pinned dependency file and recorded environment hash |

### 15.4 Metrics

R2, MAE, and RMSE are computed on the held-out fold for each model, then summarized as mean and standard deviation across folds. Pooled out-of-fold metrics are also reported, clearly labeled as pooled.

```latex
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}, \quad \text{MAE} = \frac{1}{n}\sum_i |y_i - \hat{y}_i|, \quad \text{RMSE} = \sqrt{\frac{1}{n}\sum_i (y_i - \hat{y}_i)^2}
```

Note: R2 computed per fold uses the fold's own mean. Averaging fold R2 and computing pooled R2 give different numbers, so the report must state which is used in each table. The reproduction in Experiment 0 must match whichever convention the original results used (UNKNOWN, to be confirmed).

### 15.5 Required Outputs per Model

- Fold-wise metrics table, mean and SD.
- Predicted-versus-actual plot.
- Residual plot against predicted values, and residual distribution.
- Performance across FIB-4 score ranges.
- Saved out-of-fold predictions keyed by SEQN.

### 15.6 Statistical Validation

| Topic | Requirement |
| --- | --- |
| Paired comparison | Compare models on identical out-of-fold predictions. Use per-patient squared error differences and bootstrap resampling over patients for confidence intervals on R2 or RMSE differences |
| Limits of fold-level tests | With only five folds, a paired t-test on fold scores has very low power, and fold scores are not independent because training sets overlap. Fold-level p-values must not be presented as strong evidence |
| Corrected tests | Consider the corrected resampled t-test (Nadeau and Bengio) on repeated CV, and report it as approximate |
| Repeated CV | Use repeated or nested CV to stabilize estimates |
| Multiple comparisons | Many models are compared. Control the false discovery rate or state comparisons as exploratory |
| Effect size | Report differences in R2 with intervals, not only significance |
| Superiority claims | A model is called superior only if the paired interval for the difference excludes zero and the effect exceeds a pre-declared minimal meaningful difference |
| External validation | Reported separately, only if data exist |

### 15.7 Performance Target Policy

The exploratory R2 range of 0.60 to 0.70 is aspirational only. The following are prohibited:

- Reintroducing the four direct FIB-4 components to raise R2.
- Selecting results through repeated uncontrolled tuning.
- Reporting only the best fold or only the best seed.
- Changing the cohort or target selectively to inflate performance.
- Claiming success merely because R2 enters the desired range.

If the best valid model does not reach 0.60, the actual result is reported and the information limits of the 25 features are investigated (feature-domain ablation, residual analysis, noise-ceiling reasoning). A valid R2 well below 0.60 is a legitimate finding.

## 16. Explainability and Ablation Requirements

| Method | Applies to | Requirement | Caveat |
| --- | --- | --- | --- |
| Built-in feature importance | Random Forest, Extra Trees, boosting | Report gain and permutation importance, preferring permutation importance on held-out data | Impurity-based importance is biased toward high-cardinality or continuous features |
| SHAP | Tree models and, where methodologically appropriate, neural models | TreeSHAP for trees. Kernel or deep explainers for neural models only with a documented background set and stability check | Correlated features split attribution. SHAP is not causal |
| Attention analysis | HSGIN, classical HGNN | Export attention per relation and organ, aggregated across patients and folds | Attention is not a faithful explanation of model behavior and must not be read as biological mechanism |
| Node-type ablation | Graph models | Remove each organ node type in turn as a versioned variant | Compare with feature-domain ablation on tabular models |
| Relation-family ablation | Graph models | Remove or randomize each relation family, include random-edge control | Distinguishes structure from extra capacity |
| Importance stability | All | Compute importance per fold and per seed, report rank stability | Unstable importance should not be interpreted |

All explanation outputs carry the statement: these are predictive attributions, not evidence of biological causality.

## 17. Software Architecture

### 17.1 Repository Structure (Non-Destructive)

This is a proposed structure. It must be adapted to the actual repository without unnecessarily relocating existing files. Paths marked PRESERVE are never modified. Paths marked NEW are added alongside.

```
project/
  data/
    raw/                  PRESERVE
    processed/            PRESERVE (new processed variants go in processed/comparative_v1/)
    manifests/            PRESERVE original 25-feature manifest; NEW versions added beside it
  configs/
    comparative/          NEW per-model, per-experiment configs
  src/
    ingestion/            PRESERVE existing, NEW modules added only if needed
    preprocessing/
    cohort/
    target/
    features/
    graph/
    models/
      hsgin.py            PRESERVE
      baselines.py        PRESERVE
    comparative/          NEW comparative modules
    training/
    evaluation/
    explainability/
    validation/
  experiments/
    original_hsgin/       original experiment records (PRESERVE)
    comparative/          NEW
  results/
    original_baseline/    PRESERVE
    comparative/          NEW
  checkpoints/
  logs/
  reports/
  backups/                protected baseline snapshots
  tests/
```

### 17.2 Module Responsibilities

| Module | Responsibility |
| --- | --- |
| ingestion | Read XPT files, validate schemas, join on SEQN |
| cohort | Apply inclusion and exclusion rules, emit exclusion flow table |
| target | Compute FIB-4, unit checks, validity rules |
| features | Build locked 25-feature matrix, optional engineered variants with provenance |
| preprocessing | Fold-safe imputation and scaling pipelines |
| graph | Build patient-level heterogeneous graphs |
| models | Original models (preserved) and wrappers |
| comparative | New model definitions, unified fit and predict interface |
| training | Fold runner, tuning, seeding, checkpointing |
| evaluation | Metrics, plots, subgroup analysis |
| explainability | Importance, SHAP, attention export |
| validation | Leakage gate, Y-randomization, statistical comparison |

### 17.3 Interface Contract

Every model, original or new, is exposed through one adapter with the same contract: fit on training indices, predict on held-out indices, return predictions keyed by SEQN. Original HSGIN is wrapped, not edited.

### 17.4 Libraries

Python, pandas, NumPy, scikit-learn, XGBoost, CatBoost, LightGBM, PyTorch, PyTorch Geometric, SHAP, Matplotlib. No deployment infrastructure is introduced. Experiment tracking uses plain versioned config and result files unless a lightweight tracker is later justified.

### 17.5 Mandatory Pre-Modification Audit and Transition Deliverables

Before any comparative implementation begins, the developer completes the audit below. Work does not start until the deliverables are reviewed.

| Step | Requirement |
| --- | --- |
| 1 | Inspect the complete existing project directory |
| 2 | Generate a recursive file and directory inventory |
| 3 | Identify source code, datasets, configurations, and outputs |
| 4 | Identify current HSGIN training and evaluation entry points |
| 5 | Record Git status and commit history if available |
| 6 | Identify uncommitted modifications |
| 7 | Create a complete backup or immutable baseline snapshot |
| 8 | Verify that the backup is accessible and complete (checksum comparison), and never claim a backup exists without verification |
| 9 | If the project is not under Git, initialize version control only after the original state is preserved |

Required deliverables before comparative work: existing project inventory; baseline architecture documentation; existing experiment and results inventory; backup verification report; transition impact assessment; proposed directory and module structure; list of files to create; list of existing files that must remain untouched.

**Audit status in version 1.1.** This revision changed the PRD only. No project code, dataset, configuration, or result was modified, renamed, moved, or deleted. Repository access was not available during revision, so every item below is NOT STARTED, and no backup or checksum is claimed to exist. Comparative implementation must not begin until all rows are complete and reviewed.

| Deliverable | Status | Evidence required to mark complete |
| --- | --- | --- |
| Existing project inventory | NOT STARTED | Recursive file and directory listing with sizes and modification times |
| Baseline architecture documentation | NOT STARTED | HSGIN and baseline description derived from source code, with Tables 12.3a, 12.5a, 12.5b completed |
| Existing experiment and results inventory | NOT STARTED | List of every results file, with the metrics it contains (including MAE and RMSE) |
| Checkpoint inspection | NOT STARTED | Result of Section 9.5 inspection, including "none found" if applicable |
| Backup | NOT STARTED | Immutable snapshot at a recorded location |
| Backup verification and checksum report | NOT STARTED | SHA-256 for every file in original and backup, with zero mismatches and zero missing files |
| Git status and history | NOT STARTED | Output of status and log, including uncommitted modifications |
| Transition impact assessment | NOT STARTED | Completed table below, reviewed by the technical guide |
| Proposed structure, files to create, files to leave untouched | NOT STARTED | Lists reviewed and approved |

Suggested read-only audit commands (run from the project root; keep the inventory file outside the project tree and never claim a backup exists until the check passes):

```bash
INV=/path/outside/project/baseline_inventory.sha256
find . -path ./backups -prune -o -type f -print0 | sort -z | xargs -0 sha256sum > "$INV"
git status --porcelain=v1 > /path/outside/project/git_status.txt 2>&1
git log --oneline > /path/outside/project/git_log.txt 2>&1
# after copying the snapshot into backups/baseline_v1/ :
(cd backups/baseline_v1 && sha256sum -c "$INV")
```

Checksum report format: relative path | size | SHA-256 original | SHA-256 backup | match (yes or no). The report is accepted only if every row matches and the file counts are equal.

Transition impact assessment (template, to be completed after the inventory):

| Area | Existing asset | Planned interaction | Risk | Mitigation | Approval |
| --- | --- | --- | --- | --- | --- |
| HSGIN code | UNKNOWN | Wrapped by adapter, not edited | Silent modification | Checksum check after every run | Pending |
| Feature manifest | UNKNOWN | Read only, hash enforced | Silent change | Hash gate | Pending |
| Processed data | UNKNOWN | Read only, new variants in new path | Overwrite | Separate output directory | Pending |
| Serialized graphs | UNKNOWN | Read only | Overwrite | Separate output directory | Pending |
| Original results | UNKNOWN | Read only, new results in new path | Overwrite | Separate results directory | Pending |
| Fold assignment | UNKNOWN | Reused if recoverable, otherwise new version recorded | Different splits | Versioned fold file | Pending |
| Checkpoints | UNKNOWN | See Section 9.5 | Overwrite or misuse | Provenance check | Pending |

### 17.6 Developer Safety Rules

The coding agent must not: delete files to simplify the project; replace existing implementations with regenerated versions; rewrite the original pipeline without approval; change the locked feature manifest silently; recalculate or replace historical results without preserving the originals; remove existing leakage controls; change patient splits without recording a new experiment version; assume an undocumented file is unnecessary; or claim a backup exists without verifying it. If a conflict occurs, stop and request approval.

## 18. Functional Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-01 | Ingest all 27 XPT files and join on SEQN with a row-count audit at every join | Must |
| FR-02 | Produce a cohort flow table with counts at each inclusion and exclusion step | Must |
| FR-03 | Compute FIB-4 and validate against an independent recomputation on a sample | Must |
| FR-04 | Enforce the locked 25-feature manifest by hash | Must |
| FR-05 | Run the leakage gate and block training on failure | Must |
| FR-06 | Generate, store, and reuse one patient-level fold assignment | Must |
| FR-07 | Fit all preprocessing on training folds only | Must |
| FR-08 | Load and run the original HSGIN and baselines without modification | Must |
| FR-09 | Train all proposed models through a unified interface | Must |
| FR-10 | Save out-of-fold predictions keyed by SEQN for every model | Must |
| FR-11 | Compute R2, MAE, RMSE per fold, mean, SD, and pooled | Must |
| FR-12 | Produce predicted-versus-actual and residual plots | Must |
| FR-13 | Produce performance by FIB-4 range | Must |
| FR-14 | Perform paired bootstrap comparisons on OOF predictions | Must |
| FR-15 | Run repeated Y-randomization for top models | Must |
| FR-16 | Run feature-domain and graph ablations as versioned variants | Should |
| FR-17 | Produce SHAP and attention outputs with the causality disclaimer | Should |
| FR-18 | Support nested CV and repeated CV | Should |
| FR-19 | Support stacking and weighted ensembles with nested OOF construction | Should |
| FR-20 | Run external validation when a dataset is identified | Could |
| FR-21 | Write every run's config, seed, library versions, and hashes to the experiment record | Must |

## 19. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Reproducibility | Any reported number can be regenerated from config, code version, and data hash |
| Integrity | Original assets are immutable. Writes to PRESERVE paths are blocked or detected by checksum |
| Traceability | Every table and figure in a report links to the run that produced it |
| Performance | Full benchmark completes on a single workstation or modest GPU. Tuning budgets are capped and equal |
| Maintainability | Modular code, type hints, docstrings, linting |
| Portability | Pinned environment, no cloud dependency required |
| Auditability | Leakage gate reports and fold assignments are versioned |
| Honesty | Reporting templates require existing, proposed, and unknown labels and always show all folds |

## 20. Quality Assurance and Testing

| Test | Purpose |
| --- | --- |
| Manifest exclusion test | No excluded variable or alias in any feature matrix |
| Reconstruction test | Excluded components cannot be near-perfectly regressed from any single feature |
| Fold integrity test | No SEQN appears in both train and held-out sets, and all SEQNs appear exactly once as held-out |
| Preprocessing test | Fitted statistics come only from training data |
| Target test | FIB-4 matches an independent recomputation, and unit conversions are verified |
| Determinism test | Same seed and config produce identical predictions for deterministic models |
| Adapter test | Original HSGIN wrapped output equals output from original entry point |
| Backup test | Checksums of backup and original match |
| Preservation test | Checksums of PRESERVE paths unchanged after comparative runs |
| Metric test | Metrics match scikit-learn reference on synthetic data |
| Y-randomization test | Shuffled-target R2 near zero for all models |
| Regression test | Experiment 0 outputs unchanged between code revisions |

## 21. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Validation test |
| --- | --- | --- | --- | --- | --- |
| R1 | Direct target leakage | Low with gate | Critical | Locked manifest, exclusion assertion | Manifest exclusion test |
| R2 | Indirect or proxy leakage | Medium | High | Provenance review, reconstruction and correlation screens | Reconstruction test |
| R3 | Preprocessing leakage | Medium | High | Fold-safe pipelines | Preprocessing test |
| R4 | Patient overlap across folds | Low | Critical | SEQN-keyed folds | Fold integrity test |
| R5 | Hyperparameter selection bias | High | High | Nested CV, equal budgets, pre-registered search spaces | Tuning log audit |
| R6 | Missing-data bias | Medium | Medium | Report missingness, sensitivity variants | Missingness report |
| R7 | Overfitting of deep and graph models | High | Medium | Early stopping on inner split, regularization, multi-seed | Train versus held-out gap report |
| R8 | Feature importance instability | Medium | Medium | Per-fold and per-seed importance, rank stability | Stability metric |
| R9 | Small subgroup sample sizes | High | Medium | Pre-declared minimum group size, report not evaluable | Subgroup size table |
| R10 | Reproducibility failure | Medium | High | Pinned environment, seeds, hashes | Experiment 0 and determinism test |
| R11 | Inappropriate clinical interpretation | Medium | High | Limitations section, labeling as score estimation | Report review checklist |
| R12 | Overwriting original assets | Medium | Critical | Backups, checksums, PRESERVE paths | Preservation test |
| R13 | Chasing the 0.60 target | Medium | Critical | Explicit prohibition, full reporting | Reviewer checklist |
| R14 | Unequal tuning effort across models | High | High | Equal documented budgets | Budget audit |
| R15 | Reported baseline not reproducible | Medium | High | Experiment 0, retain reported-only status | Reproduction report |
| R16 | Right-skewed target distorts R2 | Medium | Medium | Report target distribution, residuals, robust metrics alongside R2 | Residual analysis |

## 22. Expected Deliverables

| Deliverable | Description |
| --- | --- |
| Transition package | Inventory, baseline documentation, backup verification report, impact assessment (Section 17.5) |
| Codebase | Modular, tested, non-destructive extension of the existing repository |
| Versioned configs | One per model per experiment |
| Leakage gate reports | Signed, hash-linked |
| Results | OOF predictions, metrics, fold tables, plots per experiment |
| Statistical report | Paired comparisons, intervals, multiple comparison handling |
| Explainability report | Importance, SHAP, attention, ablations with caveats |
| Final research report | Methods, results, limitations, honest positioning |
| Reproducibility package | Environment file, run instructions, checksums |

## 23. Success Metrics and Acceptance Criteria

| Criterion | Acceptance |
| --- | --- |
| Preservation | All PRESERVE path checksums unchanged |
| Leakage controls | Gate passes. Y-randomization R2 near zero for every reported model |
| Fair comparison | Identical folds, preprocessing, and equal documented tuning budgets |
| Completeness | Every planned model either completed or documented as infeasible |
| Transparency | All folds, all seeds, and all models reported, including poor ones |
| Reproduction | Experiment 0 reproduces reported results within declared tolerance, or discrepancies are explained |
| Statistics | Superiority claims supported by paired intervals and a minimal meaningful difference |
| Exploratory target | R2 between 0.60 and 0.70 is not required. Reaching it is not by itself success. Not reaching it is not failure |

## 24. Implementation Roadmap

| Phase | Content | Exit criterion |
| --- | --- | --- |
| 0. Audit and backup | Inventory, backup, verification, transition deliverables | Deliverables reviewed and approved |
| 1. Foundations | Fold assignment, leakage gate, unified model interface, test suite | Gate and tests pass |
| 2. Reproduction | Experiment 0 | Reproduction report accepted |
| 3. Tabular benchmarks | Experiments 1 and 2 | Results and configs archived |
| 4. Neural and graph | Experiments 3 and 4 | Multi-seed results archived |
| 5. Ensembles | Experiment 5 | Nested protocol verified |
| 6. Ablations | Experiments 6 and 7 | Ablation tables complete |
| 7. Controls and robustness | Experiments 8 and 9 | Controls pass |
| 8. External validation | Experiment 10 if data exist | Run or documented as not performed |
| 9. Reporting | Statistics, explainability, final report | Review by guide, ML engineer, bioinformatics researcher |

Timeline estimates are intentionally not given because team size and compute availability are UNKNOWN.

## 25. Resource and Dependency Requirements

| Resource | Requirement |
| --- | --- |
| Compute | CPU workstation sufficient for tabular models. GPU helpful for FT-Transformer, TabNet, and GNN multi-seed runs. Exact hardware UNKNOWN |
| Storage | Raw data, processed data, backups, OOF predictions, checkpoints |
| Software | Libraries in Section 17.4 with pinned versions |
| Data | NHANES XPT files (existing). External dataset UNKNOWN |
| People | Technical research guide, ML engineer, bioinformatics reviewer. Availability UNKNOWN |
| Version control | Git, initialized only after original state is preserved |

## 26. Limitations

- The target is a calculated score, not a diagnosis. No independent clinical reference standard (biopsy or elastography) is used.
- NHANES is cross-sectional and US-based, so generalization to other populations is unestablished.
- Single dataset and cycle unless external validation is performed.
- About 6,277 participants limits power for subgroup analysis and for deep models.
- Five-fold CV yields noisy comparisons. Repeated CV mitigates but does not remove this.
- Existing results are reported, not independently reproduced, until Experiment 0 completes.
- Zero leakage across every conceivable pathway cannot be guaranteed. Controls reduce, but do not eliminate, this risk.
- Attention and SHAP are predictive attributions, not causal or mechanistic evidence.
- NHANES laboratory and examination variables may carry measurement noise and missingness that cap achievable R2.
- Several technical facts are UNKNOWN (feature list, graph schema, original fold construction, target transformation, R2 convention) and must be resolved from the existing project.

## 27. Future Work

- Additional feature engineering experiments with strict provenance, versioned separately.
- Other NHANES cycles for temporal validation.
- External cohorts with liver stiffness or histology as an independent reference standard.
- Uncertainty-aware prediction (conformal or quantile approaches).
- Calibration analysis against clinical FIB-4 bands.
- Improved graph designs as separately versioned HSGIN variants.
- Multi-task prediction of related indices (for example APRI), with the same leakage discipline.

## 28. Final Research Positioning

This study is a leakage-controlled comparative benchmark. It estimates how much of a computed liver fibrosis index can be recovered from non-direct, multi-organ clinical features, and whether graph-based modeling offers a measurable advantage over strong tabular baselines. It does not diagnose liver fibrosis, does not establish biological causality, and does not claim external generalizability or statistical superiority without the corresponding validation. HSGIN is evaluated as one candidate among many, and its original implementation and results remain preserved and independently reproducible. Every outcome, including a valid R2 below the exploratory 0.60 to 0.70 range, is a reportable and scientifically meaningful result.

## Appendix A. Change Log (version 1.0 to 1.1)

| # | Section | Change |
| --- | --- | --- |
| 1 | 12.3 | Added the 25-feature manifest as supplied by the project owner (Demographic 1, Liver 6, Kidney 6, Heart/Cardio 8, Biomarker 4), labeled USER-PROVIDED (UNVERIFIED), with the three-source verification procedure. Added a leakage note on the six liver features |
| 2 | 12.5 | Added the owner-provided schema: 5 node types (Patient, Liver, Kidney, Heart, Biomarker) and 14 directed edge types (8 Patient-organ, 6 organ-organ). Relation names UNKNOWN. Labeled UNVERIFIED until checked against code and a serialized graph |
| 3 | 9.5 (new) | Added existing checkpoint status: none reported, models evaluated in memory, repository search pending |
| 4 | 3.2, 7 (RQ4), 14 (Experiments 6, 7, 9) | Removed the unsupported domain names and pre-specified domain ranking. Hypotheses depend on the verified manifest. Subgroup variables are used only for stratification, never as predictors |
| 5 | 9.2 | Added MAE, RMSE, and fold SD columns with owner-provided fold means for all six models. Fold SD UNKNOWN. Added an implied-target-variance consistency check |
| 6 | 3.1, 12.2 | FIB-4 unit handling and any target transformation must be verified from the original pipeline, never assumed |
| 7 | 17.5 | Audit status (all NOT STARTED), checksum report format, read-only audit commands, and transition impact assessment template |
| 8 | 1.2 | Added the USER-PROVIDED (UNVERIFIED) evidence label |
| 9 | Appendix B | Added a verification register |

No existing project file was touched. This document is the only artifact changed.

## Appendix B. Verification Register

| Item | Current status | Source of current claim | Needed to close |
| --- | --- | --- | --- |
| 25-feature manifest | USER-PROVIDED (UNVERIFIED) | Project owner | Three-source check passed and SHA-256 recorded; NHANES codes for 24 features filled |
| 5 node types | USER-PROVIDED (UNVERIFIED) | Project owner | Table 12.5a verified against code and serialized graph |
| 14 directed edge types | USER-PROVIDED (UNVERIFIED) | Project owner | Table 12.5b verified, relation names filled |
| Existing checkpoints | None reported, repository not inspected | Project handover | Section 9.5 inspection |
| MAE and RMSE of existing models | USER-PROVIDED (UNVERIFIED), fold means | Project owner | Match against original results files |
| Fold SD of existing results | UNKNOWN | None | Extract from original results files |
| R2 convention (fold mean or pooled) | UNKNOWN | None | Confirm from original evaluation code |
| FIB-4 input units and rescaling | UNKNOWN (standard units only) | None | Verify from original pipeline code |
| Target transformation | UNKNOWN | None | Verify from original pipeline code |
| Original fold construction and stratification | UNKNOWN | None | Verify from original code and fold files |
| Tuning effort of baselines versus HSGIN | UNKNOWN | None | Verify from original configs and logs |
| Proxy-leakage screen of liver features | NOT STARTED | None | Section 13.1 tests and Experiment 6 with and without the liver group |
| Backup, checksums, impact assessment | NOT STARTED | None | Section 17.5 deliverables |
