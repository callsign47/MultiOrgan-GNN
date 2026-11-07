import unittest
import os
import json
from src.comparative.leakage_gate import run_leakage_gate

class TestLeakageGate(unittest.TestCase):
    def test_gate_execution(self):
        report = run_leakage_gate()
        self.assertTrue(report['all_passed'], "Leakage gate failed validation!")
        self.assertTrue(report['tests']['gate_1_manifest_check']['passed'])
        self.assertTrue(report['tests']['gate_2_fold_disjointness']['passed'])
        self.assertTrue(report['tests']['gate_3_reconstruction_test']['passed'])
        self.assertEqual(report['tests']['gate_1_manifest_check']['feature_count'], 25)

if __name__ == '__main__':
    unittest.main()
