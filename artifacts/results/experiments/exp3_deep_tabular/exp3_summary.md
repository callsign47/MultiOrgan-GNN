# Experiment 3 Summary: Deep Tabular Models (Multi-Seed)

- **Seeds Evaluated**: [42, 43, 44]
- **Early Stopping**: 20% inner holdout of outer train fold (patience=15)
- **Preprocessing**: Fold-safe SimpleImputer + StandardScaler on train fold only

| Model | Cross-Seed R² Mean ± SD | Seed Ensemble Pooled R² | Cross-Seed MAE | Cross-Seed RMSE | Delta R² vs Exp0 MLP (0.1320) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **MLP_Retuned** | 0.4492 ± 0.0033 | 0.4582 | 0.3569 | 0.5745 | +0.3172 |
| **FT_Transformer** | 0.4537 ± 0.0118 | 0.4674 | 0.3575 | 0.5721 | +0.3217 |
| **TabNet** | 0.4099 ± 0.0129 | 0.4501 | 0.3856 | 0.5933 | +0.2779 |
