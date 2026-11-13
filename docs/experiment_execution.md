# ORGANIX: Experiment Execution Guide

## 1. Registered Experiments Index

| Experiment ID | Title | Objective | Primary Artifact |
| :--- | :--- | :--- | :--- |
| **`exp0_reproduction`** | Phase 0 Reproduction | Verifies historical baseline metrics under audited protocol | `reproduction_report.json` |
| **`exp1_linear_trees`** | Linear & Tree Baselines | Benchmarks Ridge, ElasticNet, RandomForest, ExtraTrees | `exp1_results.json` |
| **`exp2_boosting`** | Gradient Boosted Trees | Benchmarks XGBoost, LightGBM, CatBoost, HistGradientBoosting | `exp2_results.json` |
| **`exp3_deep_tabular`** | Deep Tabular Networks | Benchmarks FT-Transformer, MLP, TabNet (multi-seed 42, 43, 44) | `exp3_results.json` |
| **`exp4_gnn`** | Multi-Organ GNNs | Benchmarks Classical HGNN vs. HSGIN (multi-seed 42, 43, 44) | `exp4_results.json` |
| **`exp5_ensemble`** | Multi-Architecture Stacking | Evaluates Simple Average, NNW Blend, Ridge Stacking | `exp5_results.json` |
| **`exp6_domain_ablations`** | Physiological Domain Ablations | Leave-One-Domain-Out retraining & single-domain models | `exp6_xgboost_results.json` |
| **`exp7_graph_ablations`** | Graph Architecture Ablations | Tests Flat Readout, Homogeneous GNN, No Cross-talk, Random Digraphs | `exp7_graph_ablation_results.json` |
| **`exp8_controls`** | 100-Perm Y-Randomization | Establishes true empirical null distribution ($R^2 \approx 0.00$) | `hsgin_100perms_distribution.json` |
| **`exp9_subgroups`** | Patient Subgroup Analysis | Evaluates performance across Age, Sex, BMI, Glycemic status | `exp9_subgroup_results.json` |

---

## 2. Inspecting Experiments via CLI

```bash
# List all registered experiments
organix experiments

# Inspect detailed metadata and artifact specs for a specific experiment
organix experiments --id exp4_gnn
```

---

## 3. Programmatic Experiment Access

```python
from organix.experiments.registry import get_experiment_info, list_registered_experiments

# Print registry overview
for exp_id in list_registered_experiments():
    info = get_experiment_info(exp_id)
    print(f"[{exp_id}] {info['name']}")
    print(f"  Inputs:  {info['input_artifacts']}")
    print(f"  Outputs: {info['output_artifacts']}")
```
