"""
ORGANIX Canonical Dataset Checksum Verification Tests.
"""

import unittest
from organix.utils.io import compute_file_sha256
from organix.utils.paths import get_paths


class TestChecksumPreservation(unittest.TestCase):
    def setUp(self):
        self.paths = get_paths()

    def test_canonical_dataset_checksums(self):
        expected_checksums = {
            self.paths.final_cohort_path: "7d9f30deb21b4c49683b96a62d6866fedd8877f3c60b8c03d208f699c6c5ca1f",
            self.paths.master_patient_path: "b1682cb1d0ad083a2d8e7749f826a9c078169925a8f9914eae2460f12d1a111d",
            self.paths.folds_path: "226b731be71e246942c3378c02182b9de5a9a1a02cf2742418fa0d343152cfe8",
            self.paths.manifest_path: "6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22",
            self.paths.patient_graphs_path: "4bffe0406004b951b3db848c7d92bd4183d4b2530a523a38f885e6dc21324145",
        }

        for path, exp_hash in expected_checksums.items():
            self.assertTrue(path.exists(), f"Canonical asset not found: {path}")
            act_hash = compute_file_sha256(path)
            self.assertEqual(act_hash, exp_hash, f"Checksum mismatch for {path}!")


if __name__ == "__main__":
    unittest.main()
