"""
ORGANIX Leakage-Safe Data Preprocessing.
"""

from typing import List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def preprocess_fold_tabular(
    df: pd.DataFrame,
    train_uids: List[str],
    val_uids: List[str],
    feature_cols: List[str],
    target_col: str = "fib4_target",
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, SimpleImputer, StandardScaler]:
    """
    Fold-safe tabular preprocessing:
    Median imputation and StandardScaler are fit SOLELY on the training partition
    and evaluated out-of-fold to strictly prevent test-fold information leakage.
    """
    train_df = df[df["patient_uid"].isin(train_uids)].copy()
    val_df = df[df["patient_uid"].isin(val_uids)].copy()

    X_train_raw = train_df[feature_cols].values
    y_train = train_df[target_col].values

    X_val_raw = val_df[feature_cols].values
    y_val = val_df[target_col].values

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_train = scaler.fit_transform(imputer.fit_transform(X_train_raw))
    X_val = scaler.transform(imputer.transform(X_val_raw))

    return X_train, y_train, X_val, y_val, imputer, scaler
