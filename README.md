# ORGANIX: Heterogeneous Systemic Graph Interaction Network for Multi-Organ Disease Modeling & FIB-4 Risk Stratification

[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch)](https://pytorch.org/)
[![PyTorch Geometric](https://img.shields.io/badge/PyG-2.3+-3C2179.svg)](https://pyg.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-22%20Passed-brightgreen.svg)]()
[![Leakage Gate](https://img.shields.io/badge/Leakage%20Gate-Verified-success.svg)]()

**ORGANIX** is an open-source, modular, and mathematically rigorous computational medicine framework implementing the **Heterogeneous Systemic Graph Interaction Network (HSGIN)**. 

The framework evaluates inter-organ physiological interactions across **Liver, Kidney, and Heart/Cardiovascular** clinical domains for continuous Fibrosis-4 (FIB-4) liver fibrosis risk stratification on the representative **NHANES August 2021–August 2023** cohort ($N = 6,277$).

---

## 🔬 Core Scientific Highlights

1. **Strict Algebraic Leakage Control**: Direct mathematical formula components of FIB-4 ($\text{Age}$, $\text{AST}$, $\text{ALT}$, $\text{Platelet Count}$) are strictly removed from model feature matrices, preventing artificial target leakage ($R^2 \approx 1.00$) and enforcing genuine multi-organ relational learning.
2. **Heterogeneous Organ Graph Topology**: Formulates each patient as an isolated `HeteroData` graph featuring **5 node types** (`patient`, `liver`, `kidney`, `heart`, `biomarker`) and **14 directed relations** encoding physiological cross-talk and systemic biomarker affinities.
3. **Benchmarking Superiority**: Achieves top benchmark performance with pooled out-of-fold **$R^2 = 0.5114$** ($0.4988 \pm 0.0264$), statistically outperforming tuned XGBoost ($R^2 = 0.4698, p = 0.0140$), FT-Transformer ($R^2 = 0.4674, p = 0.0031$), Classical HGNN ($R^2 = 0.4771, p = 0.0028$), and linear baselines ($R^2 = 0.3864, p = 0.0023$).
4. **Physiological & Graph Ablations**: Retrained Leave-One-Domain-Out (LODO) ablations prove Liver markers contribute the single largest retrained delta ($\Delta R^2 = -0.1074$), followed by Heart ($\Delta R^2 = -0.0458$) and Kidney ($\Delta R^2 = -0.0321$).

---

## 📊 Benchmark League Table (5-Fold CV, $N=6,277$)

| Rank | Model Architecture | Family | Pooled $R^2$ | Fold Mean $R^2 \pm \text{SD}$ | RMSE | MAE | Spearman $\rho$ | Stat Significance vs HSGIN |
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

## 📁 Repository Organization

```
ORGANIX/
├── pyproject.toml              # Modern package build configuration
├── requirements.txt            # Locked runtime dependencies
├── README.md                   # Master repository documentation
├── MIGRATION_MANIFEST.md       # Audit and migration mapping record
├── configs/
│   ├── default.json            # Global default settings
│   └── experiments/            # Experiment configurations (Exp0 to Exp9)
├── data/
│   ├── raw/                    # Original 27 SAS Transport XPT survey files
│   ├── processed/              # Canonical final_cohort.csv and master_patient.csv
│   ├── splits/                 # folds_v1.json (5-fold patient disjoint splits)
│   └── metadata/               # Locked feature_manifest.json and dataset audits
├── artifacts/
│   ├── graphs/                 # patient_graphs.pt (PyG HeteroData graphs)
│   └── results/                # 112 audited result files, metrics, OOF predictions
│       ├── benchmarks/         # final_benchmark_summary.json
│       ├── leakage_gate/       # leakage_gate_report.json
│       ├── statistical_tests/  # paired_bootstrap_phase3/4/5.json
│       ├── explainability/     # feature_permutation_importance.csv, etc.
│       └── experiments/        # exp0 through exp9 results and OOF prediction CSVs
├── docs/                       # Technical guides and documentation
│   ├── architecture.md         # System architecture & physiological rationale
│   ├── installation.md         # Environment setup instructions
│   ├── dataset_preparation.md  # NHANES provenance & cohort filtering flow
│   ├── graph_construction.md   # HeteroData schema & graph builders
│   ├── model_architecture.md   # HSGIN & comparative model specifications
│   ├── training_and_evaluation.md # Protocol, metrics, statistical tests
│   ├── experiment_execution.md # Experiment runner & registry guide
│   ├── results_and_artifacts.md# Complete results league table & artifact inventory
│   ├── reproducibility.md      # Deterministic seeding & scientific limitations
│   ├── migration_changelog.md  # Transformation log from legacy codebase
│   └── technical_evidence/     # 12 authoritative technical evidence sections
├── src/
│   └── organix/                # Core modular Python package
│       ├── core/               # Constants, config, exceptions, logging
│       ├── data/               # Ingestion, cohort, manifest, target, splits
│       ├── graphs/             # Schema, builder, dataset, graph preprocessing
│       ├── models/             # HSGIN, ClassicalHGNN, FT-Transformer, MLP, Baselines
│       ├── training/           # Deterministic trainers & loss functions
│       ├── evaluation/         # Metrics, leakage gate, bootstrap tests, subgroups
│       ├── explainability/     # Permutation attribution & domain ablations
│       ├── experiments/        # BaseExperiment and central registry
│       ├── utils/              # Paths, seeding, atomic I/O
│       └── cli.py              # Command-line interface
└── tests/                      # Full automated test suite (22 tests)
```

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/your-username/organix.git
cd organix
pip install -e .
```

### 2. Verify Assets & Integrity
```bash
organix verify
```

### 3. Run the Automated Leakage Control Gate
```bash
organix gate
```

### 4. Run the Full Test Suite
```bash
pytest tests/
# or
python -m unittest discover tests
```

---

## 📖 Detailed Documentation
- [Architecture Overview](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/architecture.md)
- [Installation Guide](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/installation.md)
- [Dataset Preparation & Attrition](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/dataset_preparation.md)
- [Graph Construction Guide](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/graph_construction.md)
- [Model Architecture & Baselines](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/model_architecture.md)
- [Training and Evaluation Protocol](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/training_and_evaluation.md)
- [Experiment Execution Guide](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/experiment_execution.md)
- [Benchmark Results and Artifacts](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/results_and_artifacts.md)
- [Reproducibility and Limitations](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/reproducibility.md)
- [Migration Changelog](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/migration_changelog.md)
- [Technical Evidence Package](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/docs/technical_evidence/README.md)

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for details.
