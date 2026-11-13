# Experiment 4 Summary: Graph Neural Networks Multi-Seed Evaluation

- **Seeds Evaluated**: [42, 43, 44]
- **Folds**: 5-fold patient-level (folds_v1.json, N=6277)
- **Preprocessing**: Fold-safe node-level imputation + standardization strictly on train graphs

| Model | Cross-Seed R² Mean ± SD | Seed Ensemble Pooled R² | Cross-Seed MAE | Cross-Seed RMSE | Delta R² vs Seed 42 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Classical_HGNN** | 0.4696 ± 0.0011 | 0.4771 | 0.3628 | 0.5633 | +0.0015 |
| **HSGIN** | 0.4944 ± 0.0024 | 0.5114 | 0.3525 | 0.5497 | -0.0032 |
