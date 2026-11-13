# ORGANIX: Benchmark Results and Artifact Inventory

## 1. Master League Table (5-Fold Cross-Validation, N=6,277)

All performance numbers are pooled out-of-fold (OOF) metrics verified on disk in [`artifacts/results/benchmarks/final_benchmark_summary.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/artifacts/results/benchmarks/final_benchmark_summary.json):

| Rank | Model Architecture | Family | Pooled $R^2$ | Fold Mean $R^2 \pm \text{SD}$ | RMSE | MAE | Spearman $\rho$ | Stat Difference vs HSGIN |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **HSGIN** | Graph Neural Network | **0.5114** | $0.4988 \pm 0.0264$ | **0.5416** | **0.3456** | **0.7736** | **Benchmark Champion** |
| 2 | **NNW Blend** | Ensemble (Weighted) | 0.5101 | $0.5100 \pm 0.0293$ | 0.5423 | 0.3466 | 0.7733 | Equivalent ($\Delta R^2 = -0.0013, p = 0.862$) |
| 3 | **RandomEdges Control** | Graph Null Control | 0.5095 | $0.4934 \pm 0.0026$ | 0.5427 | 0.3469 | 0.7743 | Equivalent ($\Delta R^2 = -0.0019, p = 0.814$) |
| 4 | **Ridge Stacking** | Ensemble (Stacking) | 0.5089 | $0.5089 \pm 0.0293$ | 0.5430 | 0.3518 | 0.7722 | Equivalent ($\Delta R^2 = -0.0025, p = 0.734$) |
| 5 | **Classical HGNN** | Graph Neural Network | 0.4771 | $0.4702 \pm 0.0150$ | 0.5603 | 0.3591 | 0.7558 | HSGIN Superior ($\Delta R^2 = +0.0343, p = 0.0028$) |
| 6 | **XGBoost (Tuned)** | Boosted Trees | 0.4698 | $0.4701 \pm 0.0340$ | 0.5642 | 0.3699 | 0.7438 | HSGIN Superior ($\Delta R^2 = +0.0416, p = 0.0140$) |
| 7 | **CatBoost** | Boosted Trees | 0.4685 | $0.4692 \pm 0.0345$ | 0.5649 | 0.3693 | 0.7487 | HSGIN Superior ($\Delta R^2 = +0.0429, p = 0.0070$) |
| 8 | **FT-Transformer** | Deep Tabular | 0.4674 | $0.4665 \pm 0.0289$ | 0.5655 | 0.3511 | 0.7681 | HSGIN Superior ($\Delta R^2 = +0.0440, p = 0.0031$) |
| 9 | **Deep MLP** | Deep Tabular | 0.4582 | $0.4533 \pm 0.0336$ | 0.5703 | 0.3523 | 0.7670 | HSGIN Superior ($\Delta R^2 = +0.0532, p = 0.0035$) |
| 10 | **LightGBM** | Boosted Trees | 0.4516 | $0.4518 \pm 0.0315$ | 0.5738 | 0.3757 | 0.7367 | HSGIN Superior ($\Delta R^2 = +0.0598, p = 0.0047$) |
| 11 | **Extra Trees** | Tree Ensemble | 0.4440 | $0.4438 \pm 0.0264$ | 0.5777 | 0.3766 | 0.7392 | HSGIN Superior ($\Delta R^2 = +0.0674, p < 0.001$) |
| 12 | **HistGradientBoosting** | Boosted Trees | 0.4384 | $0.4379 \pm 0.0270$ | 0.5807 | 0.3783 | 0.7300 | HSGIN Superior ($\Delta R^2 = +0.0730, p < 0.001$) |
| 13 | **Random Forest** | Tree Ensemble | 0.4288 | $0.4285 \pm 0.0271$ | 0.5856 | 0.3822 | 0.7276 | HSGIN Superior ($\Delta R^2 = +0.0826, p < 0.001$) |
| 14 | **Ridge (Tuned)** | Regularized Linear | 0.3864 | $0.3871 \pm 0.0221$ | 0.6069 | 0.4061 | 0.6918 | HSGIN Superior ($\Delta R^2 = +0.1250, p = 0.0023$) |
| 15 | **ElasticNet** | Regularized Linear | 0.3864 | $0.3870 \pm 0.0221$ | 0.6070 | 0.4060 | 0.6924 | HSGIN Superior ($\Delta R^2 = +0.1250, p = 0.0023$) |

---

## 2. Artifact Directory Organization

All artifacts are housed under `artifacts/`:
- `artifacts/graphs/patient_graphs.pt`: Pre-built PyG heterogeneous graphs for all 6,277 patients.
- `artifacts/results/benchmarks/`: Master league table JSON.
- `artifacts/results/leakage_gate/`: Automated 4-tier audit report.
- `artifacts/results/statistical_tests/`: Paired bootstrap test results.
- `artifacts/results/explainability/`: Feature permutation importance and domain attribution CSVs.
- `artifacts/results/experiments/`: Full per-experiment records, OOF predictions CSVs, and markdown summaries.
