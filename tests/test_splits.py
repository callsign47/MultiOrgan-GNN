import unittest
import os
import json

class TestSplits(unittest.TestCase):
    def test_fold_integrity(self):
        folds_path = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\comparative\folds_v1.json"
        self.assertTrue(os.path.exists(folds_path), "Folds JSON file not found!")
        
        with open(folds_path, 'r') as f:
            data = json.load(f)
            
        self.assertEqual(data['n_splits'], 5)
        self.assertEqual(data['total_patients'], 6277)
        self.assertEqual(len(data['folds']), 5)
        
        all_val_seqns = set()
        for fold in data['folds']:
            train_seqns = set(fold['train_seqn'])
            val_seqns = set(fold['val_seqn'])
            
            # 1. Zero overlap
            overlap = train_seqns & val_seqns
            self.assertEqual(len(overlap), 0, f"Fold {fold['fold']} has {len(overlap)} overlapping SEQNs!")
            
            # 2. Counts sum to 6277
            self.assertEqual(len(train_seqns) + len(val_seqns), 6277)
            
            all_val_seqns.update(val_seqns)
            
        # 3. Exhaustive coverage: every patient in exactly one val fold
        self.assertEqual(len(all_val_seqns), 6277)

if __name__ == '__main__':
    unittest.main()
