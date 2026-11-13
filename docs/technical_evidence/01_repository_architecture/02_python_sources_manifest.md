# Complete Python Source Files Manifest and Purpose Inventory

**Evaluation Scope**: All Python Scripts Across the Repository | **Standard**: Comprehensive Codebase Audit  
**Total Python Source Files**: 75 | **Status**: `VERIFIED-ON-DISK`  

---

## 1. High-Level Architectural Module Taxonomy

| Module Layer | Subdirectory / Scope | File Count | Core Architectural Responsibility |
| :--- | :--- | :---: | :--- |
| **Comparative Experiments (Phase 0–9)** | `src/comparative/` | 29 | Benchmark execution scripts, unified model adapters, bootstrap testing, and statistical corrections |
| **Core Data & Graph Pipeline** | `src/` | 14 | Ingestion of 27 XPT files, SEQN linkage, cohort filtering, FIB-4 calculation, graph construction |
| **Model Architectures** | `src/models/` | 2 | Deep PyTorch Geometric HSGIN, Classical HGNN, and scikit-learn/XGBoost baselines |
| **Automated Verification Suite** | `tests/` | 3 | Regression gates, patient fold disjointness assertions, and cryptographic baseline preservation |
| **Audits & Isolation Scripts** | `backups/` | 9 | Pre-execution audits, stacking leakage verification, and outer-fold quarantine assertions |
| **Baseline v1 Snapshot** | `backups/baseline_v1/` | 16 | Immutable preservation snapshot of historical Phase 1/Phase 2 source code |
| **Root Utilities** | Root | 1 | Standalone NHANES dataset inspection and summary report generator |

---

## 2. Detailed Python Source Inventory

### Isolation Audits & Verification (backups/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/audit_outer_fold_isolation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/audit_outer_fold_isolation.py)
- **Lines of Code**: 67 | **Size**: 2,913 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

### Preserved Baseline v1 Snapshot (backups/baseline_v1/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/generate_dataset_report.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/generate_dataset_report.py)
- **Lines of Code**: 95 | **Size**: 5,823 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_report()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: generate_dataset_report.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/ablation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/ablation.py)
- **Lines of Code**: 81 | **Size**: 3,182 bytes
- **Classes Defined**: None
- **Key Functions**: `run_organ_ablation_study()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: ablation.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/audit.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/audit.py)
- **Lines of Code**: 121 | **Size**: 5,124 bytes
- **Classes Defined**: None
- **Key Functions**: `audit_features()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: audit.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/cohort.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/cohort.py)
- **Lines of Code**: 78 | **Size**: 3,417 bytes
- **Classes Defined**: None
- **Key Functions**: `build_cohort_flow()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: cohort.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/dataset.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/dataset.py)
- **Lines of Code**: 122 | **Size**: 5,121 bytes
- **Classes Defined**: None
- **Key Functions**: `get_data_dir()`, `load_all_datasets()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: dataset.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/draw_schema_diagram.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/draw_schema_diagram.py)
- **Lines of Code**: 88 | **Size**: 3,468 bytes
- **Classes Defined**: None
- **Key Functions**: `draw_schema()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: draw_schema_diagram.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/graph_builder.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/graph_builder.py)
- **Lines of Code**: 116 | **Size**: 4,692 bytes
- **Classes Defined**: None
- **Key Functions**: `get_leak_free_organ_taxonomy()`, `build_patient_hetero_graph()`, `build_all_graphs()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: graph_builder.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/hsgin_ablation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/hsgin_ablation.py)
- **Lines of Code**: 187 | **Size**: 7,308 bytes
- **Classes Defined**: None
- **Key Functions**: `create_subgraph_for_config()`, `run_hsgin_ablation()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: hsgin_ablation.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/leakage_audit.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/leakage_audit.py)
- **Lines of Code**: 210 | **Size**: 11,338 bytes
- **Classes Defined**: None
- **Key Functions**: `run_leakage_audit()`, `generate_leakage_report()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: leakage_audit.py.

### Model Architectures (src/models/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/models/baselines.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/models/baselines.py)
- **Lines of Code**: 92 | **Size**: 3,903 bytes
- **Classes Defined**: `StandardGNNBaseline`, `ClassicalHGNN`
- **Key Functions**: `get_tabular_baselines()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: baselines.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/models/hsgin.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/models/hsgin.py)
- **Lines of Code**: 120 | **Size**: 4,720 bytes
- **Classes Defined**: `HeteroOrganConvBlock`, `HSGIN`
- **Key Functions**: None
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: hsgin.py.

### Preserved Baseline v1 Snapshot (backups/baseline_v1/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/pipeline.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/pipeline.py)
- **Lines of Code**: 95 | **Size**: 3,660 bytes
- **Classes Defined**: None
- **Key Functions**: `get_leak_free_feature_list()`, `get_5fold_splits()`, `preprocess_fold_tabular()`, `preprocess_fold_graphs()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: pipeline.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/target.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/target.py)
- **Lines of Code**: 87 | **Size**: 3,714 bytes
- **Classes Defined**: None
- **Key Functions**: `compute_and_verify_fib4()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: target.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/train.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/train.py)
- **Lines of Code**: 238 | **Size**: 10,711 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `evaluate_predictions()`, `train_hsgin_fold()`, `train_classical_hgnn_fold()`, `run_phase_2_pipeline()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: train.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/visualize_graph.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/visualize_graph.py)
- **Lines of Code**: 98 | **Size**: 3,649 bytes
- **Classes Defined**: None
- **Key Functions**: `visualize_patient_graph()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: visualize_graph.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/visualize_interactive.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/visualize_interactive.py)
- **Lines of Code**: 158 | **Size**: 6,267 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_interactive_html()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: visualize_interactive.py.

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/y_randomization.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/baseline_v1/src/y_randomization.py)
- **Lines of Code**: 65 | **Size**: 2,607 bytes
- **Classes Defined**: None
- **Key Functions**: `run_in_fold_y_randomization()`
- **Architectural Purpose**: Immutable baseline snapshot of original Phase 1/Phase 2 file: y_randomization.py.

### Isolation Audits & Verification (backups/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/check_exp5_json.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/check_exp5_json.py)
- **Lines of Code**: 8 | **Size**: 395 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/check_metrics.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/check_metrics.py)
- **Lines of Code**: 35 | **Size**: 1,606 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/test_inner_fitting.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/test_inner_fitting.py)
- **Lines of Code**: 81 | **Size**: 3,057 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/test_stacking_leakage.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/test_stacking_leakage.py)
- **Lines of Code**: 143 | **Size**: 6,092 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/update_ft_inner_predictions.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/update_ft_inner_predictions.py)
- **Lines of Code**: 90 | **Size**: 3,742 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_exp1.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_exp1.py)
- **Lines of Code**: 44 | **Size**: 1,795 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_exp2.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_exp2.py)
- **Lines of Code**: 37 | **Size**: 1,597 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_phase3_pre.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/backups/verify_phase3_pre.py)
- **Lines of Code**: 21 | **Size**: 970 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

### Root Utilities

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/generate_dataset_report.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/generate_dataset_report.py)
- **Lines of Code**: 95 | **Size**: 5,823 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_report()`
- **Architectural Purpose**: UNKNOWN

### Core Data & Graph Pipeline (src/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/ablation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/ablation.py)
- **Lines of Code**: 81 | **Size**: 3,182 bytes
- **Classes Defined**: None
- **Key Functions**: `run_organ_ablation_study()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/audit.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/audit.py)
- **Lines of Code**: 121 | **Size**: 5,124 bytes
- **Classes Defined**: None
- **Key Functions**: `audit_features()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/cohort.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/cohort.py)
- **Lines of Code**: 78 | **Size**: 3,417 bytes
- **Classes Defined**: None
- **Key Functions**: `build_cohort_flow()`
- **Architectural Purpose**: UNKNOWN

### Comparative Evaluation Suite (src/comparative/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/__init__.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/__init__.py)
- **Lines of Code**: 3 | **Size**: 88 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN
- **Module Docstring**: *"Comparative Evaluation Framework for Leakage-Controlled FIB-4 Score Prediction."*

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/base_adapter.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/base_adapter.py)
- **Lines of Code**: 62 | **Size**: 2,165 bytes
- **Classes Defined**: `BaseComparativeModel`
- **Key Functions**: `save_model_oof_predictions()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/compute_multiple_corrections.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/compute_multiple_corrections.py)
- **Lines of Code**: 169 | **Size**: 6,716 bytes
- **Classes Defined**: None
- **Key Functions**: `compute_paired_bootstrap_pvalue()`, `holm_bonferroni_correction()`, `run_exp6a_corrections()`, `run_exp6b_corrections()`, `run_exp7_corrections()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/deep_tabular.py)
- **Lines of Code**: 74 | **Size**: 2,683 bytes
- **Classes Defined**: `MLPRegressorPyTorch`, `FeatureTokenizer`, `FTTransformer`
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp0_reproduction.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp0_reproduction.py)
- **Lines of Code**: 306 | **Size**: 13,338 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `evaluate_preds()`, `train_hsgin_reproduction()`, `train_classical_hgnn_reproduction()`, `run_experiment_0()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp1_linear_trees.py)
- **Lines of Code**: 201 | **Size**: 8,339 bytes
- **Classes Defined**: None
- **Key Functions**: `run_experiment_1()`
- **Architectural Purpose**: UNKNOWN
- **Module Docstring**: *"Experiment 1: Linear & Tree-Ensemble Models with Inner-CV Hyperparameter Tuning
Models: Ridge, ElasticNet, RandomForest, ExtraTrees
- Fold-safe preprocessing: imputer + scaler fit strictly on train portion of each outer fold
- Inner CV (3-fold) for hyperparameter selection on training data only
- OOF predictions saved keyed by SEQN"*

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp2_boosting.py)
- **Lines of Code**: 267 | **Size**: 10,559 bytes
- **Classes Defined**: None
- **Key Functions**: `run_experiment_2()`
- **Architectural Purpose**: UNKNOWN
- **Module Docstring**: *"Experiment 2: Advanced Gradient Boosting Models with Inner-Validation Early Stopping
Models: XGBoost (re-tuned), LightGBM, CatBoost, HistGradientBoosting
- Fold-safe preprocessing: imputer + scaler fit strictly on train portion of each outer fold
- Inner 20% holdout split for early stopping (never touches outer val)
- XGBoost, LightGBM, CatBoost: native early stopping on inner holdout
- HistGradientBoosting: sklearn validation_fraction early stopping
- OOF predictions saved keyed by SEQN"*

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp3_deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp3_deep_tabular.py)
- **Lines of Code**: 324 | **Size**: 13,436 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `train_pytorch_model()`, `run_experiment_3()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp4_gnn.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp4_gnn.py)
- **Lines of Code**: 250 | **Size**: 9,968 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `train_gnn_model_fold()`, `run_experiment_4()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp5_ensemble.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp5_ensemble.py)
- **Lines of Code**: 635 | **Size**: 29,747 bytes
- **Classes Defined**: None
- **Key Functions**: `fold_metrics_from_df()`, `bootstrap_r2_diff()`
- **Architectural Purpose**: UNKNOWN
- **Module Docstring**: *"Phase 5: Ensemble Learning (Audited & Leakage-Free)
--------------------------------------------------
Implements:
  1. Systematic audit and quantitative investigation of meta-level leakage
     in standard OOF stacking vs. strict outer-fold isolation with inner cross-fitting.
  2. Strict outer-fold isolation and inner cross-fitting across 10 pair-excluded subsets
     for base models: HSGIN (seed 42), XGBoost_tuned, CatBoost, FT-Transformer (seed 42).
  3. Non-Negative Constrained Weighted Blending (NNW) fitted on inner meta-predictions.
  4. Ridge Stacking Meta-Learner fitted on inner meta-predictions.
  5. Simple Average Ensemble (zero parameter fitting; provably leakage-free benchmark).
  6. Residual correlation & diversity analysis.
  7. Paired bootstrap significance testing (B=2,000 resamples, Holm-Bonferroni corrected).
  8. Master ranking reconciliation against original JSON metrics.

Outputs:
  results/comparative/exp5_ensemble/SimpleAverage_oof_predictions.csv
  results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv
  results/comparative/exp5_ensemble/RidgeStacking_oof_predictions.csv
  results/comparative/exp5_ensemble/exp5_results.json
  results/comparative/exp5_ensemble/exp5_summary.md
  results/comparative/exp5_ensemble/diversity_analysis.json
  results/comparative/exp5_ensemble/meta_leakage_audit.json
  results/comparative/paired_bootstrap_phase5.json
  configs/comparative/exp5_ensemble/base_model_selection.json

Constraints:
  - Strict outer-fold isolation: outer test fold F_k is never seen by inner base models nor meta-learner
  - Extend, Never Replace: no modification to any prior output file
  - ASCII characters only for Windows cp1252 console safety"*

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp6_ablations.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/exp6_ablations.py)
- **Lines of Code**: 924 | **Size**: 43,048 bytes
- **Classes Defined**: `HSGIN_NoCrossTalk`, `HSGIN_FlatReadout`, `HomogeneousGNN`
- **Key Functions**: `set_seed()`, `run_xgb_fold()`, `preprocess_tabular_fold()`, `run_xgb_full_cv()`, `train_hsgin_fold()`, `run_hsgin_full_cv()` *(+5 more)*
- **Architectural Purpose**: UNKNOWN
- **Module Docstring**: *"Experiment 6: Feature-Domain Ablation
Experiment 7: Graph Architecture Ablation

PRD v1.1 - Phase 6
--------------------
Exp 6: Leave-one-domain-out and single-domain-only runs using:
  - Best tabular learner: XGBoost (tuned, same config as Exp2)
  - Graph model: HSGIN (seed 42, same config as Exp4)

Exp 7: Graph architecture ablations of HSGIN:
  - No cross-talk edges (patient-organ star only)
  - Random edge topology control
  - Flat mean-pool readout (vs organ-aware hierarchical)
  - Homogeneous GNN baseline

Domain assignments (from locked manifest):
  Demographics : RIAGENDR                                     [1 feature]
  Liver        : LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI,
                 LUXSMED, LUXCAPM                             [6 features]
  Kidney       : LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR,
                 KIQ022                                       [6 features]
  Heart        : BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD,
                 LBXTC, BPQ020, MCQ160C, MCQ160E             [8 features]
  Biomarker    : LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP      [4 features]

Constraints:
  - NEVER modify original baseline files (src/, data/, graphs/, reports/).
  - All new files in src/comparative/, results/comparative/exp6_ablations/,
    configs/comparative/exp6_ablations/.
  - Reuse IDENTICAL locked folds_v1.json.
  - XGBoost config identical to Exp2 (except n_estimators fixed to best_iter avg).
  - HSGIN config identical to Exp4 seed 42."*

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/finalize_phase6_audit.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/finalize_phase6_audit.py)
- **Lines of Code**: 329 | **Size**: 30,943 bytes
- **Classes Defined**: None
- **Key Functions**: `update_exp7_holm()`, `generate_audited_report()`, `update_walkthrough()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/finalize_phase7_report.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/finalize_phase7_report.py)
- **Lines of Code**: 293 | **Size**: 21,144 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_report()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/leakage_gate.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/leakage_gate.py)
- **Lines of Code**: 172 | **Size**: 7,090 bytes
- **Classes Defined**: None
- **Key Functions**: `compute_sha256()`, `run_leakage_gate()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/metrics.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/metrics.py)
- **Lines of Code**: 77 | **Size**: 3,004 bytes
- **Classes Defined**: None
- **Key Functions**: `compute_regression_metrics()`, `aggregate_fold_metrics()`, `paired_bootstrap_comparison()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/paired_tests.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/paired_tests.py)
- **Lines of Code**: 76 | **Size**: 3,235 bytes
- **Classes Defined**: None
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/reconcile_liver_contribution.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/reconcile_liver_contribution.py)
- **Lines of Code**: 96 | **Size**: 4,296 bytes
- **Classes Defined**: None
- **Key Functions**: `reconcile_audit()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/rerun_exp7_random_edges.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/rerun_exp7_random_edges.py)
- **Lines of Code**: 233 | **Size**: 9,923 bytes
- **Classes Defined**: `HSGIN_RandomTopology`
- **Key Functions**: `set_seed()`, `train_model_fold()`, `build_random_graphs()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp6_xgboost.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp6_xgboost.py)
- **Lines of Code**: 146 | **Size**: 5,926 bytes
- **Classes Defined**: None
- **Key Functions**: `preprocess_tabular_fold()`, `run_xgb_full_cv()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp6b_hsgin.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp6b_hsgin.py)
- **Lines of Code**: 217 | **Size**: 8,231 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `train_hsgin_fold()`, `apply_node_mask()`, `run_ablation_cv()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp7_graph_ablations.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp7_graph_ablations.py)
- **Lines of Code**: 366 | **Size**: 15,252 bytes
- **Classes Defined**: `HSGIN_NoCrossTalk`, `HSGIN_FlatReadout`, `HomogeneousGNN`
- **Key Functions**: `set_seed()`, `randomize_graph_edges()`, `train_model_fold()`, `run_variant_cv()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp7_random_edges_multiseed.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp7_random_edges_multiseed.py)
- **Lines of Code**: 302 | **Size**: 13,250 bytes
- **Classes Defined**: `HSGIN_RandomTopology`
- **Key Functions**: `set_seed()`, `train_model_fold()`, `build_random_graphs()`, `run_multiseed()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_controls.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_controls.py)
- **Lines of Code**: 443 | **Size**: 20,568 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `run_leaky_controls()`, `run_y_randomization()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_hsgin_100perms.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_hsgin_100perms.py)
- **Lines of Code**: 186 | **Size**: 7,798 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `run_hsgin_100perms()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_multiprocess.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_multiprocess.py)
- **Lines of Code**: 124 | **Size**: 4,637 bytes
- **Classes Defined**: None
- **Key Functions**: `run_multiprocess_y_randomization()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_worker.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp8_worker.py)
- **Lines of Code**: 126 | **Size**: 4,677 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp9_subgroups.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_exp9_subgroups.py)
- **Lines of Code**: 310 | **Size**: 13,224 bytes
- **Classes Defined**: None
- **Key Functions**: `bootstrap_subgroup_ci()`, `compute_extended_metrics()`, `compute_clinical_classification_metrics()`, `main()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_phase8_synthesis.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/run_phase8_synthesis.py)
- **Lines of Code**: 605 | **Size**: 40,142 bytes
- **Classes Defined**: None
- **Key Functions**: `run_explainability()`, `run_statistical_inference()`, `generate_master_report()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/split.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/comparative/split.py)
- **Lines of Code**: 71 | **Size**: 2,538 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_or_load_folds()`
- **Architectural Purpose**: UNKNOWN

### Core Data & Graph Pipeline (src/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/dataset.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/dataset.py)
- **Lines of Code**: 122 | **Size**: 5,121 bytes
- **Classes Defined**: None
- **Key Functions**: `get_data_dir()`, `load_all_datasets()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/draw_schema_diagram.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/draw_schema_diagram.py)
- **Lines of Code**: 88 | **Size**: 3,468 bytes
- **Classes Defined**: None
- **Key Functions**: `draw_schema()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/graph_builder.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/graph_builder.py)
- **Lines of Code**: 116 | **Size**: 4,692 bytes
- **Classes Defined**: None
- **Key Functions**: `get_leak_free_organ_taxonomy()`, `build_patient_hetero_graph()`, `build_all_graphs()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/hsgin_ablation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/hsgin_ablation.py)
- **Lines of Code**: 187 | **Size**: 7,308 bytes
- **Classes Defined**: None
- **Key Functions**: `create_subgraph_for_config()`, `run_hsgin_ablation()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/leakage_audit.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/leakage_audit.py)
- **Lines of Code**: 210 | **Size**: 11,338 bytes
- **Classes Defined**: None
- **Key Functions**: `run_leakage_audit()`, `generate_leakage_report()`
- **Architectural Purpose**: UNKNOWN

### Model Architectures (src/models/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/models/baselines.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/models/baselines.py)
- **Lines of Code**: 92 | **Size**: 3,903 bytes
- **Classes Defined**: `StandardGNNBaseline`, `ClassicalHGNN`
- **Key Functions**: `get_tabular_baselines()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/models/hsgin.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/models/hsgin.py)
- **Lines of Code**: 120 | **Size**: 4,720 bytes
- **Classes Defined**: `HeteroOrganConvBlock`, `HSGIN`
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

### Core Data & Graph Pipeline (src/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/pipeline.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/pipeline.py)
- **Lines of Code**: 95 | **Size**: 3,660 bytes
- **Classes Defined**: None
- **Key Functions**: `get_leak_free_feature_list()`, `get_5fold_splits()`, `preprocess_fold_tabular()`, `preprocess_fold_graphs()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/target.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/target.py)
- **Lines of Code**: 87 | **Size**: 3,714 bytes
- **Classes Defined**: None
- **Key Functions**: `compute_and_verify_fib4()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/train.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/train.py)
- **Lines of Code**: 238 | **Size**: 10,711 bytes
- **Classes Defined**: None
- **Key Functions**: `set_seed()`, `evaluate_predictions()`, `train_hsgin_fold()`, `train_classical_hgnn_fold()`, `run_phase_2_pipeline()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/visualize_graph.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/visualize_graph.py)
- **Lines of Code**: 98 | **Size**: 3,649 bytes
- **Classes Defined**: None
- **Key Functions**: `visualize_patient_graph()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/visualize_interactive.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/visualize_interactive.py)
- **Lines of Code**: 158 | **Size**: 6,267 bytes
- **Classes Defined**: None
- **Key Functions**: `generate_interactive_html()`
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/src/y_randomization.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/src/y_randomization.py)
- **Lines of Code**: 65 | **Size**: 2,607 bytes
- **Classes Defined**: None
- **Key Functions**: `run_in_fold_y_randomization()`
- **Architectural Purpose**: UNKNOWN

### Automated Verification Tests (tests/)

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_leakage_gate.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_leakage_gate.py)
- **Lines of Code**: 16 | **Size**: 663 bytes
- **Classes Defined**: `TestLeakageGate`
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_preservation.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_preservation.py)
- **Lines of Code**: 48 | **Size**: 1,965 bytes
- **Classes Defined**: `TestPreservation`
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN

#### [`c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_splits.py`](file:///c:/Users/admin_fix/Downloads/3 ORGAN/tests/test_splits.py)
- **Lines of Code**: 35 | **Size**: 1,256 bytes
- **Classes Defined**: `TestSplits`
- **Key Functions**: None
- **Architectural Purpose**: UNKNOWN
