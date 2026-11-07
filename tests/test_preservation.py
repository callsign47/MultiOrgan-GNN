import unittest
import os
import hashlib

class TestPreservation(unittest.TestCase):
    def test_all_preserved_files_match_snapshot(self):
        """
        Verify that all files in the baseline snapshot are unchanged in the project root.
        """
        report_path = r"c:\Users\admin_fix\Downloads\3 ORGAN\backups\baseline_v1\checksum_report.md"
        self.assertTrue(os.path.exists(report_path), "Checksum report not found!")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        checked_files = 0
        mismatches = []
        missing = []
        
        for line in lines:
            if line.startswith('| `') and 'YES' in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                rel_path = parts[0].strip('`')
                if rel_path == '.gitignore':
                    continue
                orig_hash = parts[2].strip('`')
                
                project_file = os.path.join(r"c:\Users\admin_fix\Downloads\3 ORGAN", rel_path)
                if not os.path.exists(project_file):
                    missing.append(rel_path)
                    continue
                    
                h = hashlib.sha256()
                with open(project_file, 'rb') as pf:
                    while chunk := pf.read(65536):
                        h.update(chunk)
                current_hash = h.hexdigest()
                
                if current_hash != orig_hash:
                    mismatches.append((rel_path, orig_hash, current_hash))
                checked_files += 1
                
        self.assertGreater(checked_files, 60, f"Expected >60 files checked, found {checked_files}")
        self.assertEqual(len(missing), 0, f"Missing preserved files: {missing}")
        self.assertEqual(len(mismatches), 0, f"Preservation check failed! Hash mismatches: {mismatches}")

if __name__ == '__main__':
    unittest.main()
