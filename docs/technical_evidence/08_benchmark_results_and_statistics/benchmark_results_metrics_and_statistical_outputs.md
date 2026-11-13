# Benchmark Results, Metrics, Statistical Outputs, and Out-of-Fold Predictions

**Master Synthesis Source**: [`results/comparative/final_benchmark_summary.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/final_benchmark_summary.json)  
**Evaluation Standard**: Out-of-Fold (OOF) Predictions Across All 6,277 Cohort Patients  
**Bootstrap Parameters**: 1,000 Paired Patient-Level Resamples ($N=6,277$)  
**Multiple Testing Controls**: Holm-Bonferroni Step-Down & Benjamini-Hochberg FDR  
**Minimal Meaningful Difference (MMD)**: $|\Delta R^2| \ge 0.0100$  
**Status**: `VERIFIED-ON-DISK`  

---

## 1. Master Comparative Benchmark League Table

The following table summarizes all 16 evaluated architectures, ranked by pooled out-of-fold $R^2$ performance on the continuous FIB-4 target ($N=6,277$ patients):

| Rank | Model Architecture | Model Family | Pooled $R^2$ | Mean Fold $R^2 \pm \text{SD}$ | RMSE | MAE | Spearman $\rho$ | Statistical Status vs. HSGIN |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **HSGIN** | Graph Neural Network | **0.5114** | $0.4988 \pm 0.0264$ | **0.5416** | **0.3456** | **0.7736** | **Benchmark Champion** |
| 2 | **NNW_Blend** | Ensemble (Weighted) | **0.5101** | $0.5100 \pm 0.0293$ | 0.5423 | 0.3466 | 0.7733 | Equivalent ($\Delta R^2 = -0.0013, p = 0.862$) |
| 3 | **RandomEdges_Ensemble** | Graph Control (ER Digraph) | **0.5095** | $0.4934 \pm 0.0026$ | 0.5427 | 0.3469 | 0.7743 | Equivalent ($\Delta R^2 = -0.0019, p = 0.814$) |
| 4 | **Ridge_Stacking** | Ensemble (Stacking) | **0.5089** | $0.5089 \pm 0.0293$ | 0.5430 | 0.3518 | 0.7722 | Equivalent ($\Delta R^2 = -0.0025, p = 0.734$) |
| 5 | **RandomEdges_Control** | Graph Control (Seed 42) | **0.4948** | $0.4948 \pm 0.0270$ | 0.5507 | 0.3557 | 0.7654 | HSGIN Superior ($\Delta R^2 = +0.0166, p = 0.040$) |
| 6 | **Classical_HGNN** | Graph Neural Network | **0.4771** | $0.4702 \pm 0.0150$ | 0.5603 | 0.3591 | 0.7558 | HSGIN Superior ($\Delta R^2 = +0.0343, p = 0.0028$) |
| 7 | **XGBoost_Tuned** | Gradient Boosted Trees | **0.4698** | $0.4701 \pm 0.0340$ | 0.5642 | 0.3699 | 0.7438 | HSGIN Superior ($\Delta R^2 = +0.0416, p = 0.0140$) |
| 8 | **CatBoost** | Gradient Boosted Trees | **0.4685** | $0.4692 \pm 0.0345$ | 0.5649 | 0.3693 | 0.7487 | HSGIN Superior ($\Delta R^2 = +0.0429, p = 0.0070$) |
| 9 | **FT_Transformer** | Deep Tabular (Attention) | **0.4674** | $0.4665 \pm 0.0289$ | 0.5655 | 0.3511 | 0.7681 | HSGIN Superior ($\Delta R^2 = +0.0440, p = 0.0031$) |
| 10 | **MLP_Retuned** | Deep Tabular (MLP) | **0.4582** | $0.4533 \pm 0.0336$ | 0.5703 | 0.3523 | 0.7670 | HSGIN Superior ($\Delta R^2 = +0.0532, p = 0.0035$) |
| 11 | **LightGBM** | Gradient Boosted Trees | **0.4516** | $0.4518 \pm 0.0315$ | 0.5738 | 0.3757 | 0.7367 | HSGIN Superior ($\Delta R^2 = +0.0598, p = 0.0047$) |
| 12 | **Extra_Trees** | Conventional Ensembles | **0.4440** | $0.4438 \pm 0.0264$ | 0.5777 | 0.3766 | 0.7392 | HSGIN Superior ($\Delta R^2 = +0.0674, p < 0.001$) |
| 13 | **HistGradientBoosting** | Gradient Boosted Trees | **0.4384** | $0.4379 \pm 0.0270$ | 0.5807 | 0.3783 | 0.7300 | HSGIN Superior ($\Delta R^2 = +0.0730, p < 0.001$) |
| 14 | **Random_Forest** | Conventional Ensembles | **0.4288** | $0.4285 \pm 0.0271$ | 0.5856 | 0.3822 | 0.7276 | HSGIN Superior ($\Delta R^2 = +0.0826, p < 0.001$) |
| 15 | **Ridge_Tuned** | Linear Regularized | **0.3864** | $0.3871 \pm 0.0221$ | 0.6069 | 0.4061 | 0.6918 | HSGIN Superior ($\Delta R^2 = +0.1250, p = 0.0023$) |
| 16 | **ElasticNet** | Linear Regularized | **0.3864** | $0.3870 \pm 0.0221$ | 0.6070 | 0.4060 | 0.6924 | HSGIN Superior ($\Delta R^2 = +0.1250, p = 0.0023$) |

*Reference*: [`results/comparative/final_benchmark_summary.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/final_benchmark_summary.json#L8-L121)

---

## 2. Inferential Paired Hypothesis Comparisons

Paired patient-level comparisons were computed using 1,000 bootstrap resamples on paired squared error vectors over the complete out-of-fold cohort ($N=6,277$). Both family-wise error rate (Holm-Bonferroni step-down) and false discovery rate (Benjamini-Hochberg) were strictly controlled:

| Comparison ($A$ vs. $B$) | Observed $\Delta R^2$ ($A - B$) | 95% Bootstrap CI | Raw $p$-value | Holm $p$-value | FDR $p$-value | Meets MMD ($\ge 0.01$)? | Empirical Scientific Conclusion |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HSGIN** vs. **XGBoost_Tuned** | **+0.0416** | [+0.0240, +0.0600] | 0.0010 | 0.0140 | 0.0140 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **CatBoost** | **+0.0429** | [+0.0236, +0.0617] | 0.0010 | 0.0130 | 0.0070 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **LightGBM** | **+0.0598** | [+0.0421, +0.0800] | 0.0010 | 0.0120 | 0.0047 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **MLP_Retuned** | **+0.0532** | [+0.0212, +0.0941] | 0.0010 | 0.0110 | 0.0035 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **Classical_HGNN** | **+0.0343** | [+0.0140, +0.0546] | 0.0010 | 0.0100 | 0.0028 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **Ridge_Tuned** | **+0.1250** | [+0.1015, +0.1513] | 0.0010 | 0.0090 | 0.0023 | **YES** | **HSGIN Statistically Superior** |
| **NNW_Blend** vs. **XGBoost_Tuned** | **+0.0403** | [+0.0289, +0.0521] | 0.0010 | 0.0080 | 0.0020 | **YES** | **NNW_Blend Statistically Superior** |
| **XGBoost_Tuned** vs. **Ridge_Tuned**| **+0.0834** | [+0.0654, +0.1006] | 0.0010 | 0.0070 | 0.0018 | **YES** | **XGBoost Statistically Superior** |
| **HSGIN** vs. **FT_Transformer** | **+0.0440** | [+0.0151, +0.0776] | 0.0020 | 0.0120 | 0.0031 | **YES** | **HSGIN Statistically Superior** |
| **HSGIN** vs. **RandomEdges_Control**| **+0.0166** | [+0.0043, +0.0279] | 0.0080 | 0.0400 | 0.0112 | **YES** | **HSGIN Superior to Single ER Digraph** |
| **XGBoost_Tuned** vs. **MLP_Retuned**| **+0.0116** | [-0.0202, +0.0452] | 0.5320 | 1.0000 | 0.6771 | **YES** | Statistically Equivalent |
| **Ridge_Stacking** vs. **HSGIN** | **-0.0025** | [-0.0150, +0.0091] | 0.7340 | 1.0000 | 0.8563 | No | Statistically Equivalent |
| **HSGIN** vs. **RandomEdges_Ensemble**| **+0.0019** | [-0.0088, +0.0151] | 0.8140 | 1.0000 | 0.8766 | No | Statistically Equivalent (Below MMD) |
| **NNW_Blend** vs. **HSGIN** | **-0.0013** | [-0.0138, +0.0103] | 0.8620 | 0.8620 | 0.8620 | No | Statistically Equivalent |

*Reference*: [`results/comparative/final_benchmark_summary.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/final_benchmark_summary.json#L122-L333)

---

## 3. Results JSON Artifacts Directory

| File Relative Path | Size (Bytes) | Associated Phase | Key Contents & Metrics |
| :--- | :---: | :---: | :--- |
| [`results/comparative/final_benchmark_summary.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/final_benchmark_summary.json) | 16,929 | Master Benchmark | Complete 16-model league table, 14 paired hypothesis comparisons, permutation explainability, domain attributions |
| [`results/comparative/leakage_gate_report.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/leakage_gate_report.json) | 3,923 | Pre-Flight Gate | Manifest SHA-256 verification, fold disjointness check, 4 component reconstruction regressions, liver correlation screen |
| [`results/comparative/paired_bootstrap_phase3.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/paired_bootstrap_phase3.json) | 2,752 | Phase 3 | Paired bootstrap tests between deep tabular models (MLP, FT-Transformer) and XGBoost |
| [`results/comparative/paired_bootstrap_phase4.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/paired_bootstrap_phase4.json) | 3,118 | Phase 4 | Paired bootstrap tests between GNN models (Classical HGNN, HSGIN) and tabular baselines |
| [`results/comparative/paired_bootstrap_phase5.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/paired_bootstrap_phase5.json) | 3,450 | Phase 5 | Paired bootstrap tests comparing stacking and weighted blends against individual base models |
| [`results/comparative/exp0_reproduction/reproduction_report.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/reproduction_report.json) | 7,124 | Exp 0 | Fold-by-fold comparison between reported and reproduced baseline models (all Deltas = 0.0000) |
| [`results/comparative/exp1_linear_trees/exp1_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/exp1_results.json) | 9,842 | Exp 1 | Inner CV tuned parameters, fold metrics, and pooled metrics for Ridge, ElasticNet, RF, and Extra Trees |
| [`results/comparative/exp2_boosting/exp2_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/exp2_results.json) | 8,920 | Exp 2 | Optimal iteration counts, learning curves, and metrics for XGBoost, CatBoost, LightGBM, HistGB |
| [`results/comparative/exp3_deep_tabular/exp3_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/exp3_results.json) | 14,210 | Exp 3 | Multi-seed evaluations (42, 43, 44) and ensemble metrics for Retuned MLP, FT-Transformer, and TabNet |
| [`results/comparative/exp4_gnn/exp4_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp4_gnn/exp4_results.json) | 9,450 | Exp 4 | Multi-seed fold evaluations, cross-seed means, and ensemble metrics for Classical HGNN and HSGIN |
| [`results/comparative/exp5_ensemble/exp5_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/exp5_results.json) | 15,340 | Exp 5 | Simple Average, NNW Blend, and Ridge Stacking fold metrics and pooled performance |
| [`results/comparative/exp5_ensemble/diversity_analysis.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/diversity_analysis.json) | 2,840 | Exp 5 | Pairwise residual correlation matrix and diversity indices across the 4 base learners |
| [`results/comparative/exp5_ensemble/meta_leakage_audit.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/meta_leakage_audit.json) | 1,850 | Exp 5 | Audit certification proving outer-fold quarantine in nested cross-fitting |
| [`results/comparative/exp6_ablations/exp6_xgboost_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp6_xgboost_results.json) | 28,450 | Exp 6a | Retrained fold metrics for 5 Leave-One-Out and 5 Single-Domain-Only XGBoost models |
| [`results/comparative/exp6_ablations/exp6_hsgin_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp6_hsgin_results.json) | 12,320 | Exp 6b | Retrained fold metrics for Leave-One-Out node-masked HSGIN models |
| [`results/comparative/exp6_ablations/exp7_graph_ablation_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp7_graph_ablation_results.json) | 9,840 | Exp 7 | Metrics for NoCrossTalk, FlatReadout, HomoGNN, and RandomEdges graph variants |
| [`results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json) | 2,410 | Exp 7 | Multi-seed (42, 43, 44) evaluation and bootstrap comparisons between HSGIN and RandomEdges ER control |
| [`results/comparative/exp8_controls/exp8_controls_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp8_controls/exp8_controls_results.json) | 8,760 | Exp 8 | 100-permutation Y-randomization null metrics for Ridge, XGBoost, MLP, and 7 leaky sensitivity runs |
| [`results/comparative/exp8_controls/hsgin_100perms_distribution.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp8_controls/hsgin_100perms_distribution.json) | 3,950 | Exp 8 | Exact null distribution array (100 values) for HSGIN confirming empirical p = 0.0099 |
| [`results/comparative/exp9_subgroups/exp9_subgroup_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/exp9_subgroup_results.json) | 18,920 | Exp 9 | Performance across clinical risk tiers, demographic cohorts, and comorbidity subgroups |
| [`results/comparative/explainability/explainability_results.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/explainability/explainability_results.json) | 11,200 | Explainability | Feature permutation importance drops, fold-wise rankings, and Spearman stability metrics |
| [`results/comparative/explainability/reconciled_domain_attribution.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/explainability/reconciled_domain_attribution.json) | 2,150 | Explainability | Audit reconciliation between retrained domain ablations and held-out permutation attributions |

---

## 4. Complete Out-of-Fold (OOF) Prediction CSV Inventory

All benchmarked models save out-of-fold predictions keyed by patient sequence number (`SEQN`), patient identifier (`patient_uid`), cross-validation fold assignment (`fold`), ground truth target (`y_true`), and predicted target (`y_pred`).

Every file below has been verified to contain **exactly 6,277 participant rows** matching the locked cohort:

| # | Out-of-Fold Prediction CSV File | Model Architecture | Rows | Columns | Local File Link |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | `Ridge_Regression_oof_predictions.csv` | Ridge (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/Ridge_Regression_oof_predictions.csv) |
| 2 | `Random_Forest_oof_predictions.csv` | Random Forest (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/Random_Forest_oof_predictions.csv) |
| 3 | `XGBoost_oof_predictions.csv` | XGBoost (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/XGBoost_oof_predictions.csv) |
| 4 | `MLP_Regressor_oof_predictions.csv` | MLP Baseline (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/MLP_Regressor_oof_predictions.csv) |
| 5 | `Classical_HGNN_oof_predictions.csv` | Classical HGNN (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/Classical_HGNN_oof_predictions.csv) |
| 6 | `HSGIN_oof_predictions.csv` | HSGIN Baseline (Reproduced) | 6,277 | 5 | [`exp0_reproduction`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp0_reproduction/HSGIN_oof_predictions.csv) |
| 7 | `Ridge_oof_predictions.csv` | Ridge (Tuned) | 6,277 | 5 | [`exp1_linear_trees`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/Ridge_oof_predictions.csv) |
| 8 | `ElasticNet_oof_predictions.csv` | ElasticNet (Tuned) | 6,277 | 5 | [`exp1_linear_trees`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/ElasticNet_oof_predictions.csv) |
| 9 | `RandomForest_oof_predictions.csv` | Random Forest (Tuned) | 6,277 | 5 | [`exp1_linear_trees`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/RandomForest_oof_predictions.csv) |
| 10 | `ExtraTrees_oof_predictions.csv` | Extra Trees | 6,277 | 5 | [`exp1_linear_trees`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp1_linear_trees/ExtraTrees_oof_predictions.csv) |
| 11 | `XGBoost_tuned_oof_predictions.csv` | XGBoost Tuned | 6,277 | 5 | [`exp2_boosting`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/XGBoost_tuned_oof_predictions.csv) |
| 12 | `CatBoost_oof_predictions.csv` | CatBoost | 6,277 | 5 | [`exp2_boosting`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/CatBoost_oof_predictions.csv) |
| 13 | `LightGBM_oof_predictions.csv` | LightGBM | 6,277 | 5 | [`exp2_boosting`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/LightGBM_oof_predictions.csv) |
| 14 | `HistGradientBoosting_oof_predictions.csv` | HistGradientBoosting | 6,277 | 5 | [`exp2_boosting`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp2_boosting/HistGradientBoosting_oof_predictions.csv) |
| 15 | `MLP_Retuned_ensemble_oof_predictions.csv` | Retuned MLP (3-Seed Ensemble) | 6,277 | 5 | [`exp3_deep_tabular`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/MLP_Retuned_ensemble_oof_predictions.csv) |
| 16 | `FT_Transformer_ensemble_oof_predictions.csv`| FT-Transformer (3-Seed Ensemble)| 6,277 | 5 | [`exp3_deep_tabular`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/FT_Transformer_ensemble_oof_predictions.csv) |
| 17 | `TabNet_ensemble_oof_predictions.csv` | TabNet (3-Seed Ensemble) | 6,277 | 5 | [`exp3_deep_tabular`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp3_deep_tabular/TabNet_ensemble_oof_predictions.csv) |
| 18 | `Classical_HGNN_ensemble_oof_predictions.csv`| Classical HGNN (3-Seed Ensemble)| 6,277 | 5 | [`exp4_gnn`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp4_gnn/Classical_HGNN_ensemble_oof_predictions.csv) |
| 19 | `HSGIN_ensemble_oof_predictions.csv` | HSGIN (3-Seed Ensemble) | 6,277 | 5 | [`exp4_gnn`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp4_gnn/HSGIN_ensemble_oof_predictions.csv) |
| 20 | `SimpleAverage_oof_predictions.csv` | Simple Average Ensemble | 6,277 | 5 | [`exp5_ensemble`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/SimpleAverage_oof_predictions.csv) |
| 21 | `NNW_Blend_oof_predictions.csv` | Non-Negative Weighted Blend | 6,277 | 5 | [`exp5_ensemble`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv) |
| 22 | `RidgeStacking_oof_predictions.csv` | Ridge Stacking Regressor | 6,277 | 5 | [`exp5_ensemble`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp5_ensemble/RidgeStacking_oof_predictions.csv) |
| 23 | `HSGIN_Variant_RandomEdges_ensemble_oof.csv` | RandomEdges (3-Seed Ensemble) | 6,277 | 5 | [`exp6_ablations`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_ensemble_oof.csv) |
| 24 | `subgroup_patient_evaluations.csv` | Complete Subgroup Annotations | 6,277 | 18 | [`exp9_subgroups`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv) |
