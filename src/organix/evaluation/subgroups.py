"""
ORGANIX Clinical and Demographic Subgroup Evaluation.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from organix.evaluation.metrics import compute_regression_metrics


def evaluate_patient_subgroups(
    df: pd.DataFrame,
    y_true_col: str,
    y_pred_col: str,
    subgroup_definitions: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Evaluates model performance across demographic (Age, Sex, Race/Ethnicity)
    and clinical (BMI, Glycemic, Hypertension) patient subgroups.
    """
    results = {}
    for group_name, query_str in subgroup_definitions.items():
        sub_df = df.query(query_str) if isinstance(query_str, str) else df[query_str(df)]
        if len(sub_df) < 10:
            continue
        metrics = compute_regression_metrics(
            sub_df[y_true_col].values,
            sub_df[y_pred_col].values,
        )
        results[group_name] = {
            "sample_size": len(sub_df),
            "percentage_of_cohort": float(len(sub_df) / len(df) * 100.0),
            "metrics": metrics,
        }
    return results
