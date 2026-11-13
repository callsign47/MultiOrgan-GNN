"""
ORGANIX Experiment Registry Resolution Tests.
"""

import unittest
from organix.experiments.registry import (
    EXPERIMENT_REGISTRY,
    list_registered_experiments,
    get_experiment_info,
)
from organix.utils.paths import get_paths


class TestExperimentRegistry(unittest.TestCase):
    def setUp(self):
        self.paths = get_paths()

    def test_registry_count(self):
        exp_list = list_registered_experiments()
        self.assertEqual(len(exp_list), 10)
        expected = [
            "exp0_reproduction",
            "exp1_linear_trees",
            "exp2_boosting",
            "exp3_deep_tabular",
            "exp4_gnn",
            "exp5_ensemble",
            "exp6_domain_ablations",
            "exp7_graph_ablations",
            "exp8_controls",
            "exp9_subgroups",
        ]
        for e in expected:
            self.assertIn(e, exp_list)

    def test_configs_and_artifacts_resolve(self):
        for exp_id in list_registered_experiments():
            info = get_experiment_info(exp_id)
            cfg_file = self.paths.root / info["config_file"]
            self.assertTrue(cfg_file.exists(), f"Config file missing for {exp_id}: {cfg_file}")
            for in_art in info["input_artifacts"]:
                in_path = self.paths.root / in_art
                self.assertTrue(in_path.exists(), f"Input artifact missing for {exp_id}: {in_path}")


if __name__ == "__main__":
    unittest.main()
