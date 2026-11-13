"""
ORGANIX End-to-End Pipeline Smoke Test.
"""

import unittest
import numpy as np
from organix.data.cohort import load_final_cohort
from organix.data.splits import load_or_generate_splits
from organix.data.preprocessing import preprocess_fold_tabular
from organix.data.manifest import get_feature_names
from organix.models.baselines import get_tabular_baselines
from organix.evaluation.metrics import compute_regression_metrics


class TestSmokePipeline(unittest.TestCase):
    def test_end_to_end_tabular_smoke(self):
        df = load_final_cohort()
        folds_data = load_or_generate_splits()
        fold1 = folds_data["folds"][0]

        train_uids = fold1["train_patient_uids"]
        val_uids = fold1["val_patient_uids"]
        feature_cols = get_feature_names()

        X_train, y_train, X_val, y_val, imputer, scaler = preprocess_fold_tabular(
            df=df,
            train_uids=train_uids,
            val_uids=val_uids,
            feature_cols=feature_cols,
        )

        self.assertEqual(X_train.shape, (len(train_uids), 25))
        self.assertEqual(X_val.shape, (len(val_uids), 25))
        self.assertFalse(np.isnan(X_train).any())
        self.assertFalse(np.isnan(X_val).any())

        # Fit lightweight Ridge baseline
        models = get_tabular_baselines()
        ridge = models["Ridge_Regression"]
        ridge.fit(X_train, y_train)
        preds = ridge.predict(X_val)

        metrics = compute_regression_metrics(y_val, preds)
        self.assertGreater(metrics["r2"], 0.30, f"Smoke test R^2 too low: {metrics['r2']}")
        self.assertLess(metrics["mae"], 0.50, f"Smoke test MAE too high: {metrics['mae']}")


if __name__ == "__main__":
    unittest.main()
