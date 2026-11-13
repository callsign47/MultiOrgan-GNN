"""
ORGANIX Cross-Validation Fold Management and Integrity Verification.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import pandas as pd
from sklearn.model_selection import KFold
from organix.core.constants import EXPECTED_COHORT_SIZE, EXPECTED_FOLDS_COUNT, RANDOM_SEED
from organix.core.exceptions import CohortValidationError
from organix.utils.paths import get_paths


def load_or_generate_splits(
    cohort_path: Optional[Path] = None,
    folds_path: Optional[Path] = None,
    n_splits: int = EXPECTED_FOLDS_COUNT,
    seed: int = RANDOM_SEED,
    force_regenerate: bool = False,
) -> Dict[str, Any]:
    """
    Loads pre-computed 5-fold cross-validation assignments or generates them deterministically.
    Verifies 100% mutual exclusivity (zero patient overlap) between train and val folds.
    """
    paths = get_paths()
    c_path = cohort_path or paths.final_cohort_path
    f_path = folds_path or paths.folds_path

    if f_path.is_file() and not force_regenerate:
        with open(f_path, "r", encoding="utf-8") as f:
            folds_data = json.load(f)
        validate_splits_integrity(folds_data, expected_total=EXPECTED_COHORT_SIZE)
        return folds_data

    # Generate deterministically
    df = pd.read_csv(c_path)
    if "SEQN" not in df.columns or "patient_uid" not in df.columns:
        raise CohortValidationError("Cohort dataframe must contain 'SEQN' and 'patient_uid' columns.")

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    seqns = df["SEQN"].values
    patient_uids = df["patient_uid"].values

    folds = []
    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(seqns), start=1):
        fold_obj = {
            "fold": fold_idx,
            "train_seqn": [int(x) for x in seqns[train_idx]],
            "val_seqn": [int(x) for x in seqns[val_idx]],
            "train_uid": [str(x) for x in patient_uids[train_idx]],
            "val_uid": [str(x) for x in patient_uids[val_idx]],
        }
        folds.append(fold_obj)

    folds_data = {
        "description": "Deterministic 5-fold cross validation split on patient level (SEQN / patient_uid)",
        "seed": seed,
        "n_splits": n_splits,
        "total_patients": len(df),
        "folds": folds,
    }

    validate_splits_integrity(folds_data, expected_total=len(df))
    f_path.parent.mkdir(parents=True, exist_ok=True)
    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(folds_data, f, indent=2)

    return folds_data


def validate_splits_integrity(folds_data: Dict[str, Any], expected_total: int = EXPECTED_COHORT_SIZE) -> None:
    """Verifies that folds are mutually disjoint and cover the complete cohort."""
    all_val_seqns = set()
    for fold in folds_data.get("folds", []):
        tr = set(fold["train_seqn"])
        va = set(fold["val_seqn"])
        overlap = tr.intersection(va)
        if overlap:
            raise CohortValidationError(
                f"Data leakage detected! Fold {fold['fold']} has {len(overlap)} overlapping patients."
            )
        if len(tr) + len(va) != expected_total:
            raise CohortValidationError(
                f"Fold {fold['fold']} patient sum ({len(tr)} + {len(va)}) != {expected_total}"
            )
        all_val_seqns.update(va)

    if len(all_val_seqns) != expected_total:
        raise CohortValidationError(
            f"Validation set union ({len(all_val_seqns)}) != cohort total ({expected_total})"
        )
