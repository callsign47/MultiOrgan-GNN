"""
ORGANIX Heterogeneous Graph Schema & Batching Tests.
"""

import unittest
import torch
from organix.graphs.schema import get_hetero_schema
from organix.graphs.builder import build_patient_hetero_graph
from organix.data.cohort import load_final_cohort
from organix.core.constants import NODE_TYPES, EDGE_TYPES, NODE_FEATURE_DIMS


class TestGraphSchema(unittest.TestCase):
    def setUp(self):
        self.df = load_final_cohort()

    def test_schema_specification(self):
        schema = get_hetero_schema()
        self.assertEqual(len(schema["node_types"]), 5)
        self.assertEqual(len(schema["edge_types"]), 14)
        for nt in NODE_TYPES:
            self.assertIn(nt, schema["node_types"])

    def test_single_graph_construction(self):
        sample_row = self.df.iloc[0]
        g = build_patient_hetero_graph(sample_row)

        # Node check
        for nt in NODE_TYPES:
            self.assertIn(nt, g.node_types)
            expected_dim = NODE_FEATURE_DIMS[nt]
            self.assertEqual(g[nt].x.shape, (1, expected_dim))

        # Edge check
        for et in EDGE_TYPES:
            self.assertIn(et, g.edge_types)
            self.assertEqual(g[et].edge_index.shape, (2, 1))

        # Target check
        self.assertEqual(g["patient"].y.shape, (1,))
        self.assertAlmostEqual(g["patient"].y.item(), float(sample_row["fib4_target"]), places=4)


if __name__ == "__main__":
    unittest.main()
