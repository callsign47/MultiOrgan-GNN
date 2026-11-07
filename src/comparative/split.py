import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"
FOLDS_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\comparative\folds_v1.json"

def generate_or_load_folds(cohort_path=COHORT_PATH, folds_path=FOLDS_PATH, n_splits=5, seed=42, force_regenerate=False):
    """
    Generate or load deterministic 5-fold patient-level partitions keyed on SEQN and patient_uid.
    """
    if os.path.exists(folds_path) and not force_regenerate:
        with open(folds_path, 'r') as f:
            data = json.load(f)
        return data

    df = pd.read_csv(cohort_path)
    if 'SEQN' not in df.columns or 'patient_uid' not in df.columns:
        raise ValueError("Cohort dataframe must contain 'SEQN' and 'patient_uid' columns.")

    # Unique patients
    patient_ids = df['patient_uid'].values
    seqns = df['SEQN'].values

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    
    folds = []
    all_val_seqns = set()
    total_patients = len(df)

    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(patient_ids)):
        train_uids = patient_ids[train_idx].tolist()
        val_uids = patient_ids[val_idx].tolist()
        train_seqn = [int(s) for s in seqns[train_idx]]
        val_seqn = [int(s) for s in seqns[val_idx]]

        # Integrity checks
        intersection = set(train_seqn) & set(val_seqn)
        assert len(intersection) == 0, f"Fold {fold_idx}: Patient overlap detected across train and val!"
        all_val_seqns.update(val_seqn)

        folds.append({
            "fold": fold_idx + 1,
            "train_count": len(train_idx),
            "val_count": len(val_idx),
            "train_patient_uids": train_uids,
            "val_patient_uids": val_uids,
            "train_seqn": train_seqn,
            "val_seqn": val_seqn
        })

    assert len(all_val_seqns) == total_patients, f"Total validation SEQNs ({len(all_val_seqns)}) does not match cohort size ({total_patients})!"

    fold_data = {
        "n_splits": n_splits,
        "seed": seed,
        "total_patients": total_patients,
        "folds": folds
    }

    os.makedirs(os.path.dirname(folds_path), exist_ok=True)
    with open(folds_path, 'w') as f:
        json.dump(fold_data, f, indent=2)

    print(f"Generated and saved versioned fold partition with {n_splits} folds to: {folds_path}")
    return fold_data

if __name__ == "__main__":
    generate_or_load_folds(force_regenerate=True)
