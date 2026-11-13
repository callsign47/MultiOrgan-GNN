"""
ORGANIX Central Experiment Registry (Exp0 to Exp9).
"""

from typing import Dict, Any, List, Optional
from organix.utils.paths import get_paths


EXPERIMENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "exp0_reproduction": {
        "id": "exp0_reproduction",
        "name": "Phase 0 Baseline Reproduction",
        "description": "Exact 5-fold cross-validation reproduction of historical reported baselines and HSGIN.",
        "config_file": "configs/experiments/exp0_reproduction.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "artifacts/graphs/patient_graphs.pt"],
        "output_artifacts": ["artifacts/results/experiments/exp0_reproduction/reproduction_report.json"],
        "models": ["Ridge_Regression", "Random_Forest", "XGBoost", "MLP_Regressor", "Classical_HGNN", "HSGIN"],
    },
    "exp1_linear_trees": {
        "id": "exp1_linear_trees",
        "name": "Linear Models & Conventional Tree Ensembles",
        "description": "5-fold CV evaluation of Ridge, ElasticNet, RandomForest, and ExtraTrees.",
        "config_file": "configs/experiments/exp1_linear_trees.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp1_linear_trees/exp1_results.json"],
        "models": ["Ridge", "ElasticNet", "RandomForest", "ExtraTrees"],
    },
    "exp2_boosting": {
        "id": "exp2_boosting",
        "name": "Modern Gradient Boosted Decision Trees",
        "description": "5-fold CV evaluation of CatBoost, LightGBM, HistGradientBoosting, and tuned XGBoost.",
        "config_file": "configs/experiments/exp2_boosting.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp2_boosting/exp2_results.json"],
        "models": ["XGBoost_tuned", "LightGBM", "CatBoost", "HistGradientBoosting"],
    },
    "exp3_deep_tabular": {
        "id": "exp3_deep_tabular",
        "name": "Deep Tabular Neural Networks",
        "description": "5-fold CV evaluation of PyTorch MLP, FT-Transformer, and TabNet across seeds (42, 43, 44).",
        "config_file": "configs/experiments/deep_tabular_configs.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp3_deep_tabular/exp3_results.json"],
        "models": ["MLP_Retuned", "FT_Transformer", "TabNet"],
    },
    "exp4_gnn": {
        "id": "exp4_gnn",
        "name": "Multi-Organ Graph Neural Networks",
        "description": "5-fold CV evaluation of Classical HGNN (HeteroSAGE) vs. HSGIN across seeds (42, 43, 44).",
        "config_file": "configs/experiments/gnn_configs.json",
        "input_artifacts": ["artifacts/graphs/patient_graphs.pt", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp4_gnn/exp4_results.json"],
        "models": ["Classical_HGNN", "HSGIN"],
    },
    "exp5_ensemble": {
        "id": "exp5_ensemble",
        "name": "Leakage-Audited Multi-Architecture Ensembling",
        "description": "Inner-fold meta-prediction generation and evaluation of Simple Average, NNW Blend, and Ridge Stacking.",
        "config_file": "configs/experiments/base_model_selection.json",
        "input_artifacts": ["artifacts/results/experiments/exp5_ensemble/inner_meta_predictions.npz"],
        "output_artifacts": ["artifacts/results/experiments/exp5_ensemble/exp5_results.json"],
        "models": ["SimpleAverage", "NNW_Blend", "RidgeStacking"],
    },
    "exp6_domain_ablations": {
        "id": "exp6_domain_ablations",
        "name": "Physiological Domain Ablations & Standalones",
        "description": "Leave-One-Domain-Out retraining and Single-Domain standalone models across XGBoost and HSGIN.",
        "config_file": "configs/experiments/exp6_config.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp6_ablations/exp6_xgboost_results.json"],
        "models": ["XGBoost_Ablations", "HSGIN_Ablations"],
    },
    "exp7_graph_ablations": {
        "id": "exp7_graph_ablations",
        "name": "Graph Architectural Component Ablations",
        "description": "Systematic ablation of Flat Readout, Homogeneous GNN, No Cross-Talk, and Multi-Seed Random Edge Control.",
        "config_file": "configs/experiments/exp7_config.json",
        "input_artifacts": ["artifacts/graphs/patient_graphs.pt", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp6_ablations/exp7_graph_ablation_results.json"],
        "models": ["FlatReadout", "HomoGNN", "NoCrossTalk", "RandomEdges_Ensemble"],
    },
    "exp8_controls": {
        "id": "exp8_controls",
        "name": "100-Permutation Y-Randomization Null & Positive Controls",
        "description": "100-permutation Y-randomization distribution establishing true empirical null and intentional leaky models.",
        "config_file": "configs/experiments/exp8_config.json",
        "input_artifacts": ["artifacts/graphs/patient_graphs.pt", "data/splits/folds_v1.json"],
        "output_artifacts": ["artifacts/results/experiments/exp8_controls/hsgin_100perms_distribution.json"],
        "models": ["HSGIN_YRandomization_100", "Leaky_Controls"],
    },
    "exp9_subgroups": {
        "id": "exp9_subgroups",
        "name": "Clinical & Demographic Subgroup Performance",
        "description": "Stratified evaluation across Age cohorts, Sex, Race/Ethnicity, BMI categories, and metabolic risk factors.",
        "config_file": "configs/experiments/exp9_subgroups.json",
        "input_artifacts": ["data/processed/final_cohort.csv", "artifacts/results/experiments/exp9_subgroups/subgroup_patient_evaluations.csv"],
        "output_artifacts": ["artifacts/results/experiments/exp9_subgroups/exp9_subgroup_results.json"],
        "models": ["HSGIN", "XGBoost", "NNW_Blend", "Ridge"],
    },
}


def list_registered_experiments() -> List[str]:
    """Returns list of registered experiment IDs."""
    return list(EXPERIMENT_REGISTRY.keys())


def get_experiment_info(experiment_id: str) -> Dict[str, Any]:
    """Retrieves metadata and configuration info for a registered experiment."""
    if experiment_id not in EXPERIMENT_REGISTRY:
        raise KeyError(f"Experiment '{experiment_id}' is not in the ORGANIX registry. Available: {list_registered_experiments()}")
    return EXPERIMENT_REGISTRY[experiment_id]
