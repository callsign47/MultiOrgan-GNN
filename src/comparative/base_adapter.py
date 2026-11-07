import os
import json
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class BaseComparativeModel(ABC):
    """
    Standard interface contract for all benchmarked models.
    """
    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.config = config or {}
        self.imputer = None
        self.scaler = None

    def fit_preprocessing(self, X_train: np.ndarray, standardize: bool = True):
        """
        Fit median imputation and optional standardization strictly on training folds.
        """
        self.imputer = SimpleImputer(strategy='median')
        X_imp = self.imputer.fit_transform(X_train)
        if standardize:
            self.scaler = StandardScaler()
            return self.scaler.fit_transform(X_imp)
        return X_imp

    def transform_preprocessing(self, X: np.ndarray, standardize: bool = True):
        """
        Apply fitted imputation and standardization to validation or test data.
        """
        X_imp = self.imputer.transform(X)
        if standardize and self.scaler is not None:
            return self.scaler.transform(X_imp)
        return X_imp

    @abstractmethod
    def fit(self, X_train: np.ndarray, y_train: np.ndarray, X_inner_val: np.ndarray = None, y_inner_val: np.ndarray = None):
        """
        Fit the model on training data. Inner validation split is optional for early stopping/tuning.
        """
        pass

    @abstractmethod
    def predict(self, X_val: np.ndarray) -> np.ndarray:
        """
        Predict continuous target values.
        """
        pass

def save_model_oof_predictions(model_name: str, oof_records: list, output_dir: str):
    """
    Save out-of-fold predictions keyed by SEQN to CSV and JSON.
    oof_records: list of dicts with keys: SEQN, patient_uid, fold, y_true, y_pred
    """
    os.makedirs(output_dir, exist_ok=True)
    df_oof = pd.DataFrame(oof_records)
    csv_path = os.path.join(output_dir, f"{model_name}_oof_predictions.csv")
    df_oof.to_csv(csv_path, index=False)
    return csv_path
