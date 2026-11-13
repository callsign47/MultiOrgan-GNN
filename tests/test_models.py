"""
ORGANIX Model Construction and Forward Pass Tests.
"""

import unittest
import torch
from torch_geometric.data import HeteroData, Batch
from organix.models.hsgin import HSGIN
from organix.models.baselines import ClassicalHGNN
from organix.models.deep_tabular import FTTransformer, MLPRegressorPyTorch
from organix.core.constants import NODE_FEATURE_DIMS, EDGE_TYPES


class TestModels(unittest.TestCase):
    def setUp(self):
        self.in_dim_dict = NODE_FEATURE_DIMS

    def create_dummy_batch(self, batch_size=2):
        graphs = []
        for i in range(batch_size):
            g = HeteroData()
            g.patient_uid = f"P_{i}"
            for nt, dim in self.in_dim_dict.items():
                g[nt].x = torch.randn(1, dim)
            g["patient"].y = torch.tensor([1.2])
            for src, rel, dst in EDGE_TYPES:
                g[src, rel, dst].edge_index = torch.tensor([[0], [0]], dtype=torch.long)
            graphs.append(g)
        return Batch.from_data_list(graphs)

    def test_hsgin_forward_pass(self):
        model = HSGIN(self.in_dim_dict, hidden_dim=64, num_layers=2)
        batch = self.create_dummy_batch(batch_size=3)
        out = model(batch)
        self.assertEqual(out.shape, (3,))
        self.assertFalse(torch.isnan(out).any())

    def test_classical_hgnn_forward_pass(self):
        model = ClassicalHGNN(self.in_dim_dict, hidden_dim=64)
        batch = self.create_dummy_batch(batch_size=3)
        out = model(batch)
        self.assertEqual(out.shape, (3,))
        self.assertFalse(torch.isnan(out).any())

    def test_ft_transformer_forward_pass(self):
        model = FTTransformer(num_features=25, embed_dim=32, num_heads=4, num_layers=2)
        x = torch.randn(4, 25)
        out = model(x)
        self.assertEqual(out.shape, (4,))
        self.assertFalse(torch.isnan(out).any())

    def test_mlp_forward_pass(self):
        model = MLPRegressorPyTorch(in_features=25, hidden_dims=[64, 32])
        x = torch.randn(4, 25)
        out = model(x)
        self.assertEqual(out.shape, (4,))
        self.assertFalse(torch.isnan(out).any())


if __name__ == "__main__":
    unittest.main()
