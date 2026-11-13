# Experiment 2 Summary: Advanced Gradient Boosting Models

- **Early stopping holdout**: 20% inner split (never the outer val fold)
- **Early stopping rounds**: 50
- **Preprocessing**: Median imputation + StandardScaler fit on outer train fold only
- **Folds**: 5-fold patient-level (folds_v1.json, seed=42, N=6277)

| Model | R2 Mean | R2 Std | MAE Mean | RMSE Mean | Avg Best Iter | Delta R2 vs Exp0 XGB |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost_tuned** | 0.4701 | 0.0340 | 0.3699 | 0.5629 | 354 | +0.0182 |
| **LightGBM** | 0.4519 | 0.0229 | 0.3757 | 0.5727 | 281 | -0.0000 |
| **CatBoost** | 0.4686 | 0.0352 | 0.3693 | 0.5637 | 755 | +0.0166 |
| **HistGradientBoosting** | 0.4376 | 0.0223 | 0.3783 | 0.5799 | 386 | -0.0144 |

> Exp0 reference (untuned XGBoost): R2=0.4519
