"""
ORGANIX Evaluation Package.
"""

from organix.evaluation.metrics import compute_regression_metrics, aggregate_fold_metrics
from organix.evaluation.leakage_gate import run_leakage_gate
from organix.evaluation.statistical_tests import (
    paired_bootstrap_comparison,
    apply_holm_bonferroni,
    apply_benjamini_hochberg,
)
from organix.evaluation.subgroups import evaluate_patient_subgroups

__all__ = [
    "compute_regression_metrics",
    "aggregate_fold_metrics",
    "run_leakage_gate",
    "paired_bootstrap_comparison",
    "apply_holm_bonferroni",
    "apply_benjamini_hochberg",
    "evaluate_patient_subgroups",
]
