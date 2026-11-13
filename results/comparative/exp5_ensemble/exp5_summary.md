# Phase 5 Ensemble Learning — Audited & Corrected Summary

**Cohorts**: N=6,277 patients | **Splits**: 5-fold patient-level partitions | **Inner Cross-Fitting**: 10 pair-excluded subsets

## 1. Reconciled Ground-Truth Prior Pooled R²
- **HSGIN (3-seed ensemble)**: 0.5114
- **HSGIN (Seed 42)**: 0.4988
- **HSGIN (Seed 44)**: 0.4943
- **HSGIN (Seed 43)**: 0.4927
- **Classical HGNN (3-seed ensemble)**: 0.4771
- **XGBoost (tuned)**: 0.4698
- **CatBoost**: 0.4685
- **FT-Transformer (3-seed ensemble)**: 0.4674
- **FT-Transformer (Seed 42)**: 0.4660

## 2. Audited Ensemble Performance (Strict Leakage-Free)

| Ensemble | Pooled R² | Mean-Fold R² | MAE | RMSE |
| :--- | :---: | :---: | :---: | :---: |
| **Simple Average** | 0.5004 | 0.5009 | 0.3505 | 0.5477 |
| **NNW Blend (Strict)** | 0.5101 | 0.5100 | 0.3466 | 0.5423 |
| **Ridge Stacking (Strict)** | 0.5089 | 0.5086 | 0.3518 | 0.5430 |

## 3. Average Non-Negative Weights
- **HSGIN_seed42**: 0.4894
- **XGBoost_tuned**: 0.3411
- **CatBoost**: 0.0000
- **FT_Transformer_seed42**: 0.1695

## 4. Current Best Observed Performance Plateau

> **Empirical Observation**: Performance across all tabular learners, transformers, graph networks,
> and ensemble combinations plateaus at R² ≈ 0.47–0.51 under the locked 25-feature set.
> This is characterized strictly as the **current best observed performance** of the tested models
> and does not constitute an asserted biological ceiling.

## 5. Paired Bootstrap Tests (Holm-Bonferroni Corrected)

| Ensemble | Competitor | Delta R² | 95% CI | Holm p | Significant? |
| :--- | :--- | :---: | :---: | :---: | :---: |
| SimpleAverage | XGBoost_tuned | +0.0306 | [+0.0173, +0.0435] | 0.0000 | **YES** |
| SimpleAverage | CatBoost | +0.0319 | [+0.0241, +0.0401] | 0.0000 | **YES** |
| SimpleAverage | FT_Transformer_seed42 | +0.0483 | [+0.0301, +0.0687] | 0.0000 | **YES** |
| NNW_Blend | XGBoost_tuned | +0.0403 | [+0.0287, +0.0526] | 0.0000 | **YES** |
| NNW_Blend | CatBoost | +0.0416 | [+0.0318, +0.0519] | 0.0000 | **YES** |
| NNW_Blend | FT_Transformer_seed42 | +0.0581 | [+0.0343, +0.0834] | 0.0000 | **YES** |
| RidgeStacking | XGBoost_tuned | +0.0391 | [+0.0281, +0.0504] | 0.0000 | **YES** |
| RidgeStacking | CatBoost | +0.0404 | [+0.0302, +0.0506] | 0.0000 | **YES** |
| RidgeStacking | FT_Transformer_seed42 | +0.0569 | [+0.0322, +0.0835] | 0.0000 | **YES** |
| NNW_Blend | HSGIN_seed42 | +0.0113 | [+0.0012, +0.0218] | 0.1110 | NO |
| RidgeStacking | HSGIN_seed42 | +0.0101 | [+0.0001, +0.0205] | 0.1000 | NO |
| SimpleAverage | HSGIN_seed42 | +0.0016 | [-0.0145, +0.0179] | 0.8150 | NO |