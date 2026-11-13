"""
ORGANIX Data Loading and Cohort Integrity Tests.
"""

import unittest
from organix.data.cohort import load_final_cohort
from organix.data.manifest import verify_and_load_manifest, get_feature_names
from organix.core.constants import EXPECTED_COHORT_SIZE, EXPECTED_FEATURE_COUNT, EXCLUDED_FEATURES


class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.df = load_final_cohort()
        self.manifest = verify_and_load_manifest()

    def test_cohort_dimensions(self):
        self.assertEqual(len(self.df), EXPECTED_COHORT_SIZE)
        self.assertIn("SEQN", self.df.columns)
        self.assertIn("patient_uid", self.df.columns)
        self.assertIn("fib4_target", self.df.columns)

    def test_locked_features_present(self):
        feature_names = get_feature_names()
        self.assertEqual(len(feature_names), EXPECTED_FEATURE_COUNT)
        for feat in feature_names:
            self.assertIn(feat, self.df.columns, f"Feature {feat} missing from cohort!")

    def test_target_moments(self):
        y = self.df["fib4_target"]
        self.assertFalse(y.isna().any(), "Target has NaN values!")
        self.assertTrue((y > 0).all(), "Target contains non-positive values!")
        self.assertAlmostEqual(float(y.mean()), 1.15, delta=0.2)
        self.assertAlmostEqual(float(y.median()), 0.98, delta=0.2)


if __name__ == "__main__":
    unittest.main()
