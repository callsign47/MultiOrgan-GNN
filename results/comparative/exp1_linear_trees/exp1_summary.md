# Experiment 1 Summary: Linear & Tree Models

- **Inner CV**: 3-fold GridSearchCV on training data only
- **Preprocessing**: Median imputation + StandardScaler fit on train fold only
- **Folds**: 5-fold patient-level (folds_v1.json, seed=42, N=6277)

| Model | R2 Mean | R2 Std | MAE Mean | MAE Std | RMSE Mean | RMSE Std | Delta R2 vs Exp0 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ridge** | 0.3871 | 0.0221 | 0.4061 | 0.0094 | 0.6057 | 0.0386 | +0.0002 |
| **ElasticNet** | 0.3870 | 0.0215 | 0.4060 | 0.0091 | 0.6057 | 0.0385 | N/A (new) |
| **RandomForest** | 0.4295 | 0.0205 | 0.3822 | 0.0080 | 0.5844 | 0.0376 | +0.0355 |
| **ExtraTrees** | 0.4446 | 0.0220 | 0.3766 | 0.0074 | 0.5766 | 0.0371 | N/A (new) |

> Exp0 reference baselines (untuned): Ridge R2=0.3869, RF R2=0.3940
