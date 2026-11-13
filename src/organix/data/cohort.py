"""
ORGANIX Cohort Management and Validation.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
from organix.core.constants import (
    EXPECTED_COHORT_SIZE,
    get_locked_feature_list,
    EXCLUDED_FEATURES,
)
from organix.core.exceptions import CohortValidationError
from organix.utils.paths import get_paths


def load_final_cohort(cohort_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads and validates the canonical patient cohort (N=6,277).
    Ensures correct patient identifiers, target column, and manifest features.
    """
    path = cohort_path or get_paths().final_cohort_path
    if not path.is_file():
        raise FileNotFoundError(f"Final cohort CSV not found at: {path}")

    df = pd.read_csv(path)

    # 1. Size check
    if len(df) != EXPECTED_COHORT_SIZE:
        raise CohortValidationError(
            f"Expected cohort size {EXPECTED_COHORT_SIZE}, found {len(df)}"
        )

    # 2. Key identifier check
    required_id_cols = ["SEQN", "patient_uid", "fib4_target"]
    missing_ids = [c for c in required_id_cols if c not in df.columns]
    if missing_ids:
        raise CohortValidationError(f"Missing required identifier columns: {missing_ids}")

    # 3. Features check
    manifest_features = get_locked_feature_list()
    missing_features = [f for f in manifest_features if f not in df.columns]
    if missing_features:
        raise CohortValidationError(f"Missing manifest features in cohort: {missing_features}")

    # 4. Target validity check
    if df["fib4_target"].isna().any():
        raise CohortValidationError("NaN values detected in fib4_target!")

    return df
