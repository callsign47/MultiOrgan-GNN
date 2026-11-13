# Experiment 8: Y-Randomization & Leakage Controls Summary

## 1. Deliberately Leaky Sensitivity Demonstration Controls
> [!CAUTION]
> The models below intentionally include the 4 excluded formula components (`RIDAGEYR`, `LBXSASSI`, `LBXSATSI`, `LBXPLTSI`) solely to confirm that the evaluation framework would detect near-perfect $R^2$ if leakage were present. These models are labeled as leakage demonstrations and are strictly excluded from all comparative benchmarking tables.

| Model Name | Features Tested | Feature Count | Pooled $R^2$ | RMSE | MAE | Leakage Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Ridge_Leaky_Raw4** | Raw 4 components with linear Ridge regression... | 4 | **0.7297** | 0.4028 | 0.2083 | **100% Detected Leakage** |
| **Ridge_Leaky_Full29** | 25 manifest features + 4 components with linear Ri... | 29 | **0.7521** | 0.3858 | 0.2105 | **100% Detected Leakage** |
| **XGBoost_Leaky_Raw4** | Raw 4 components with tuned XGBoost non-linear tre... | 4 | **0.9494** | 0.1743 | 0.0637 | **100% Detected Leakage** |
| **XGBoost_Leaky_Full29** | 25 manifest features + 4 components with tuned XGB... | 29 | **0.9406** | 0.1888 | 0.0739 | **100% Detected Leakage** |
| **MLP_Leaky_Raw4** | Raw 4 components with deep MLP regressor... | 4 | **0.9649** | 0.1451 | 0.0458 | **100% Detected Leakage** |
| **MLP_Leaky_Full29** | 25 manifest features + 4 components with deep MLP... | 29 | **0.9110** | 0.2311 | 0.1178 | **100% Detected Leakage** |
| **Exact_LogFormula_Ridge** | Exact log-linear formula decomposition: ln(Age) + ... | 4 | **1.0000** | 0.0000 | 0.0000 | **100% Detected Leakage** |

---

## 2. Y-Randomization Empirical Null Distributions
Target vector $y$ permuted repeatedly across patients while feature matrices remain locked.

| Model Architecture | Permutations ($M$) | True Locked $R^2$ | Mean Null $R^2 \pm \text{SD}$ | 95% Empirical Null Range | Max Null $R^2$ | Empirical $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ridge** | 100 | **0.3871** | **-0.0059 \pm 0.0019** | [-0.0099, -0.0017] | -0.0012 | **0.0099** |
| **XGBoost** | 100 | **0.4723** | **-0.0227 \pm 0.0095** | [-0.0470, -0.0072] | -0.0065 | **0.0099** |
| **MLP** | 100 | **0.4492** | **-0.0699 \pm 0.0078** | [-0.0842, -0.0562] | -0.0536 | **0.0099** |
| **HSGIN** | 10 | **0.4988** | **-0.0019 \pm 0.0014** | [-0.0039, +0.0005] | +0.0006 | **0.0909** |
