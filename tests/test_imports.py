"""
ORGANIX Package Import Validation Tests.
"""

import unittest


class TestOrganixImports(unittest.TestCase):
    def test_import_core(self):
        import organix.core
        from organix.core.constants import FEATURE_DOMAINS, EXCLUDED_FEATURES, NODE_TYPES, EDGE_TYPES
        from organix.core.config import get_config, PathConfig
        self.assertEqual(len(FEATURE_DOMAINS), 5)
        self.assertEqual(len(EXCLUDED_FEATURES), 4)
        self.assertEqual(len(NODE_TYPES), 5)
        self.assertEqual(len(EDGE_TYPES), 14)

    def test_import_data(self):
        import organix.data
        from organix.data.cohort import load_final_cohort
        from organix.data.manifest import verify_and_load_manifest
        from organix.data.splits import load_or_generate_splits
        from organix.data.preprocessing import preprocess_fold_tabular
        from organix.data.target import compute_fib4_score

    def test_import_graphs(self):
        import organix.graphs
        from organix.graphs.schema import get_hetero_schema
        from organix.graphs.builder import build_patient_hetero_graph
        from organix.graphs.dataset import load_patient_graphs, preprocess_fold_graphs

    def test_import_models(self):
        import organix.models
        from organix.models.hsgin import HSGIN, HeteroOrganConvBlock
        from organix.models.baselines import ClassicalHGNN, StandardGNNBaseline
        from organix.models.deep_tabular import FTTransformer, MLPRegressorPyTorch

    def test_import_training(self):
        import organix.training
        from organix.training.loss import get_loss_function
        from organix.training.trainer import train_gnn_model_fold

    def test_import_evaluation(self):
        import organix.evaluation
        from organix.evaluation.metrics import compute_regression_metrics, aggregate_fold_metrics
        from organix.evaluation.leakage_gate import run_leakage_gate
        from organix.evaluation.statistical_tests import paired_bootstrap_comparison

    def test_import_experiments(self):
        import organix.experiments
        from organix.experiments.registry import list_registered_experiments, get_experiment_info
        self.assertEqual(len(list_registered_experiments()), 10)


if __name__ == "__main__":
    unittest.main()
