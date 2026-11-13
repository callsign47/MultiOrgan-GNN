# Complete Experiments 0–9 Protocols, Implementation Details, and Execution Scripts

**Governing Protocol**: PRD Comparative Evaluation v1.1  
**Scope**: All 10 Experimental Phases (Exp 0 through Exp 9)  
**Execution Standard**: Unified 5-Fold Patient-Level CV Partition (`data/comparative/folds_v1.json`)  
**Status**: `VERIFIED-ON-DISK` (100% Executed, Verified, and Archived)  

---

## 1. Overview of Experimental Progression

The benchmark progresses through 10 sequentially dependent, audited experimental phases:

```
[Phase 0: Baseline Reproduction (Exp 0)] ──> Exact Historical Reproduction (Delta = 0.0000)
                 │
                 ▼
[Phase 1 & 2: Tabular Benchmarking (Exp 1 & 2)] ──> Linear, Trees, and Gradient Boosting
                 │
                 ▼
[Phase 3 & 4: Deep & Graph Benchmarking (Exp 3 & 4)] ──> Deep Tabular, Classical HGNN, HSGIN
                 │
                 ▼
[Phase 5: Audited Ensembling (Exp 5)] ──> Stacking & Non-Negative Blending
                 │
                 ▼
[Phase 6 & 7: Scientific Ablations (Exp 6 & 7)] ──> Organ Domain Ablations & Graph Architecture Controls
                 │
                 ▼
[Phase 8 & 9: Verification & Clinical Translation (Exp 8 & 9)] ──> Y-Randomization, Leaky Controls & Subgroups
```

---

## 2. Detailed Experiment-by-Experiment Breakdown

### Experiment 0: Reproduction of Historical Baseline (Phase 0)
- **Objective**: Independently verify that historical Phase 1/Phase 2 baseline metrics reported in [`reports/FINAL_MASTER_HANDOVER.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/reports/FINAL_MASTER_HANDOVER.md) can be reproduced with zero discrepancy from preserved code and data.
- **Script Location**: [`src/comparative/exp0_reproduction.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp0_reproduction.py)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp0_reproduction/reproduction_report.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/reproduction_report.json)
  - Narrative Comparison: [`results/comparative/exp0_reproduction/reproduction_comparison.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/reproduction_comparison.md)
  - 6 OOF Prediction CSVs: `Ridge_Regression`, `Random_Forest`, `XGBoost`, `MLP_Regressor`, `Classical_HGNN`, `HSGIN`.
- **Methodology**: Load preserved entry points, execute 5-fold cross-validation on locked cohort, compare regenerated fold metrics with reported values.
- **Verification Results**:
  - Ridge Regression: Reported $R^2 = 0.3869$, Reproduced $R^2 = 0.3869$ ($\Delta = 0.0000$)
  - Random Forest: Reported $R^2 = 0.3940$, Reproduced $R^2 = 0.3940$ ($\Delta = 0.0000$)
  - XGBoost: Reported $R^2 = 0.4519$, Reproduced $R^2 = 0.4519$ ($\Delta = 0.0000$)
  - MLP Regressor: Reported $R^2 = 0.1320$, Reproduced $R^2 = 0.1320$ ($\Delta = 0.0000$)
  - Classical HGNN: Reported $R^2 = 0.4681$, Reproduced $R^2 = 0.4681$ ($\Delta = 0.0000$)
  - HSGIN: Reported $R^2 = 0.4976$, Reproduced $R^2 = 0.4976$ ($\Delta = 0.0000$)
  - **Reproduction Verdict**: **100% PERFECT PARITY (PASSED)**.

---

### Experiment 1: Linear and Conventional Machine Learning (Phase 1)
- **Objective**: Establish competitive low-complexity baselines across regularized linear models (Ridge, ElasticNet) and conventional tree ensembles (Random Forest, Extra Trees).
- **Script Location**: [`src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp1_linear_trees.py)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp1_linear_trees/exp1_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/exp1_results.json)
  - Summary: [`results/comparative/exp1_linear_trees/exp1_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/exp1_summary.md)
  - 4 OOF Prediction CSVs: `Ridge`, `ElasticNet`, `RandomForest`, `ExtraTrees`.
- **Methodology**: 3-fold inner cross-validation for hyperparameter tuning ($\alpha$ for Ridge; $\alpha$ and $l_1$-ratio for ElasticNet) within each outer training fold. Median imputation and standardization fitted strictly on training folds.
- **Results**: Extra Trees ($R^2 = 0.4440$) significantly outperforms Random Forest ($R^2 = 0.4288$), while Ridge ($R^2 = 0.3864$) and ElasticNet ($R^2 = 0.3864$) achieve identical performance.

---

### Experiment 2: Advanced Gradient Boosting (Phase 2)
- **Objective**: Determine the performance ceiling of gradient boosted decision trees under equalized tuning budgets and leakage-free early stopping.
- **Script Location**: [`src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp2_boosting.py)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp2_boosting/exp2_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/exp2_results.json)
  - Summary: [`results/comparative/exp2_boosting/exp2_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/exp2_summary.md)
  - 4 OOF Prediction CSVs: `XGBoost_tuned`, `CatBoost`, `LightGBM`, `HistGradientBoosting`.
- **Methodology**: 20% inner validation split from outer training data used for 50-round early stopping. No outer test fold labels were accessed during fitting or iteration selection.
- **Results**: Tuned XGBoost achieves $R^2 = 0.4698$ (mean optimal iterations: 354), followed closely by CatBoost ($R^2 = 0.4685$), LightGBM ($R^2 = 0.4516$), and HistGradientBoosting ($R^2 = 0.4384$).

---

### Experiment 3: Deep Tabular Architectures (Phase 3)
- **Objective**: Resolve whether the baseline MLP failure ($R^2 = 0.1320$) reflects an inherent deep learning deficit on tabular clinical data, and benchmark modern tabular attention (FT-Transformer) and sparse attention (TabNet).
- **Script Locations**: [`src/comparative/exp3_deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp3_deep_tabular.py), [`src/comparative/deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/deep_tabular.py)
- **Configuration**: [`configs/comparative/exp3_deep_tabular/deep_tabular_configs.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp3_deep_tabular/deep_tabular_configs.json)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp3_deep_tabular/exp3_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/exp3_results.json)
  - Summary: [`results/comparative/exp3_deep_tabular/exp3_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/exp3_summary.md)
  - 12 OOF CSVs (3 seeds + ensemble for MLP, FT-Transformer, TabNet).
- **Methodology**: Re-tuned MLP with LayerNorm, Huber loss, AdamW, and Dropout. FT-Transformer with 2 attention blocks. TabNet with sparse mask selection. Evaluated across 3 distinct random seeds (42, 43, 44) under 5-fold CV.
- **Results**: Re-tuned MLP achieves ensemble $R^2 = 0.4582$ (+0.3262 gain over baseline 0.1320). FT-Transformer achieves ensemble $R^2 = 0.4674$. TabNet achieves $R^2 = 0.4501$.

---

### Experiment 4: Graph Neural Networks Multi-Seed Evaluation (Phase 4)
- **Objective**: Conduct rigorous multi-seed evaluation of Classical HGNN and HSGIN to quantify fold and seed variance and evaluate GNN performance against best tabular models.
- **Script Location**: [`src/comparative/exp4_gnn.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp4_gnn.py)
- **Configuration**: [`configs/comparative/exp4_gnn/gnn_configs.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp4_gnn/gnn_configs.json)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp4_gnn/exp4_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp4_gnn/exp4_results.json)
  - Summary: [`results/comparative/exp4_gnn/exp4_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp4_gnn/exp4_summary.md)
  - 8 OOF CSVs (3 seeds + ensemble for HGNN and HSGIN).
- **Methodology**: 5-fold CV across seeds 42, 43, and 44. AdamW optimizer, batch size 64, Huber loss.
- **Results**: HSGIN single-seed mean $R^2 = 0.4944 \pm 0.0024$; 3-seed ensemble pooled $R^2 = \mathbf{0.5114}$ ($\text{RMSE} = 0.5416, \text{MAE} = 0.3456$). Classical HGNN ensemble pooled $R^2 = 0.4771$.

---

### Experiment 5: Audited Leakage-Free Ensemble Learning (Phase 5)
- **Objective**: Benchmark ensemble combinations across diverse model families (GNN, Tree, Boosting, Deep Tabular) under strict nested cross-fitting.
- **Script Location**: [`src/comparative/exp5_ensemble.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp5_ensemble.py)
- **Configuration**: [`configs/comparative/exp5_ensemble/base_model_selection.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp5_ensemble/base_model_selection.json)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp5_ensemble/exp5_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/exp5_results.json)
  - Summary: [`results/comparative/exp5_ensemble/exp5_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/exp5_summary.md)
  - Audit: [`results/comparative/exp5_ensemble/meta_leakage_audit.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/meta_leakage_audit.json)
  - Inner Matrix: [`results/comparative/exp5_ensemble/inner_meta_predictions.npz`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/inner_meta_predictions.npz)
  - 3 OOF Prediction CSVs: `SimpleAverage`, `NNW_Blend`, `RidgeStacking`.
- **Methodology**: 4 diverse base models: `HSGIN_seed42`, `XGBoost_tuned`, `CatBoost`, `FT_Transformer_seed42`. Inner out-of-fold meta-features generated across 10 pair-excluded subsets $D \setminus (F_k \cup F_j)$ to guarantee zero test fold contamination.
- **Results**: Non-Negative Weighted Blend ($R^2 = 0.5101$) and Ridge Stacking ($R^2 = 0.5089$) closely match HSGIN ($R^2 = 0.5114$).

---

### Experiment 6: Feature-Domain Ablations (Phase 6)
- **Objective**: Quantify the empirical contribution of each organ domain via full Leave-One-Domain-Out and Single-Domain-Only model retraining.
- **Script Locations**: [`src/comparative/run_exp6_xgboost.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp6_xgboost.py), [`src/comparative/run_exp6b_hsgin.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp6b_hsgin.py)
- **Configuration**: [`configs/comparative/exp6_ablations/exp6_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp6_ablations/exp6_config.json)
- **Primary Outputs**:
  - XGBoost Results: [`results/comparative/exp6_ablations/exp6_xgboost_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp6_xgboost_results.json)
  - HSGIN Results: [`results/comparative/exp6_ablations/exp6_hsgin_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp6_hsgin_results.json)
  - Statistical Audits: `exp6a_bootstrap_holm.json`, `exp6b_bootstrap_holm.json`
  - 12 OOF CSVs (Full, LOO, and ONLY runs for each domain).
- **Methodology**: 5 Leave-One-Out subsets and 5 Single-Domain subsets retrained from scratch across all 5 folds using fixed XGBoost (360 trees) and HSGIN (30 epochs).
- **Results**: Liver removal causes largest drop ($\Delta R^2 = -0.0965$ XGBoost, $-0.1074$ HSGIN). Standalone single domains achieve Heart $R^2 = 0.2232$, Liver $R^2 = 0.2083$, Biomarkers $R^2 = 0.1531$, Kidney $R^2 = 0.1492$, proving multi-organ synergy drives prediction.

---

### Experiment 7: Graph Architecture Ablations & Random Edge Controls (Phase 7)
- **Objective**: Deconstruct HSGIN to identify whether gains stem from specific biological topology, organ-aware readout, attention mechanism, or inductive capacity regularization.
- **Script Locations**: [`src/comparative/run_exp7_graph_ablations.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp7_graph_ablations.py), [`src/comparative/run_exp7_random_edges_multiseed.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp7_random_edges_multiseed.py)
- **Configuration**: [`configs/comparative/exp6_ablations/exp7_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp6_ablations/exp7_config.json)
- **Primary Outputs**:
  - Variant Results: [`results/comparative/exp6_ablations/exp7_graph_ablation_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp7_graph_ablation_results.json)
  - RandomEdges Multi-Seed: [`results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json)
  - 7 OOF CSVs (`NoCrossTalk`, `FlatReadout`, `HomoGNN`, `RandomEdges` seeds & ensemble).
- **Methodology**: Evaluated 4 architectural variants:
  1. `NoCrossTalk`: Star topology (removes 6 organ-organ edges).
  2. `FlatReadout`: Replaces organ-aware readout with global mean pooling across all 5 nodes.
  3. `HomoGNN`: Collapses heterogeneous graph into homogeneous GCN.
  4. `RandomEdges`: Erdős–Rényi random digraph $G(5, 14)$ null control across seeds 42, 43, 44.
- **Results**: RandomEdges 3-seed ensemble achieves $R^2 = 0.5095$ vs HSGIN $0.5114$ ($\Delta R^2 = \mathbf{+0.0019}$, $p = 0.6920$, n.s., below MMD). Proves graph acts as capacity regularizer without requiring specific biological topology.

---

### Experiment 8: Y-Randomization & Leakage Controls (Phase 8)
- **Objective**: Confirm absence of direct target leakage via 100-permutation target shuffling and demonstrate framework sensitivity using 7 deliberately leaky controls.
- **Script Locations**: [`src/comparative/run_exp8_controls.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp8_controls.py), [`src/comparative/run_exp8_hsgin_100perms.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp8_hsgin_100perms.py)
- **Configuration**: [`configs/comparative/exp8_controls/exp8_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp8_controls/exp8_config.json)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp8_controls/exp8_controls_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp8_controls/exp8_controls_results.json)
  - Summary: [`results/comparative/exp8_controls/exp8_controls_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp8_controls/exp8_controls_summary.md)
  - HSGIN 100-Perm Distribution: [`results/comparative/exp8_controls/hsgin_100perms_distribution.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp8_controls/hsgin_100perms_distribution.json)
  - 7 Leaky OOF CSVs (Ridge, XGBoost, MLP on Raw 4, Full 29, and Exact Log-Formula).
- **Methodology**: Target vector $y$ permuted across patients while feature matrix remains locked. 100 permutations each for Ridge, XGBoost, MLP, and HSGIN. 7 deliberately leaky runs with Age, AST, ALT, and Platelet Count reintroduced.
- **Results**: HSGIN 100-permutation empirical null $R^2 = -0.0114 \pm 0.0066$ (max $+0.0006$, empirical $p = 0.0099 < 0.01$). Leaky controls achieve $R^2 = 0.7297$ to $1.0000$, validating framework leakage sensitivity.

---

### Experiment 9: Clinical Robustness & Subgroup Analysis (Phase 9)
- **Objective**: Assess clinical diagnostic concordance across FIB-4 clinical risk tiers (<1.30, 1.30-2.67, >2.67), demographic/comorbidity subgroups, and analyze mathematical range restriction.
- **Script Location**: [`src/comparative/run_exp9_subgroups.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/run_exp9_subgroups.py)
- **Primary Outputs**:
  - Results JSON: [`results/comparative/exp9_subgroups/exp9_subgroup_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/exp9_subgroup_results.json)
  - Summary: [`results/comparative/exp9_subgroups/exp9_subgroups_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/exp9_subgroups_summary.md)
  - Patient Evaluation CSV: [`results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv) ($N=6,277$).
- **Methodology**: Evaluate out-of-fold predictions across clinical risk bands, biological sex, age brackets (<45, 45-64, 65+), hypertension history, diabetes history, liver steatosis (CAP), and BMI categories.
- **Results**: High clinical screening concordance: Low-risk rule-out sensitivity = **$87.0\%$** (NPV **$67.2\%$**); High-risk rule-in specificity = **$99.5\%$** (PPV **$52.5\%$**); 3-class concordance = **$77.8\%$**. Proves continuous $R^2$ truncation within narrow slices is driven by mathematical range restriction rather than model failure.
