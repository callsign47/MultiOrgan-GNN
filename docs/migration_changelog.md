# ORGANIX: Repository Migration Changelog

## Migration Summary
- **Source**: `3 ORGAN` (heterogeneous, monolithic research repository)
- **Target**: `ORGANIX` (modular, professionally packaged computational medicine framework)
- **Date**: November 2026
- **Status**: **100% COMPLETE & VERIFIED**

---

## Key Structural Transformations

1. **Package Creation**:
   - Built the modular `organix` package (`src/organix/`) with subpackages for `core`, `data`, `graphs`, `models`, `training`, `evaluation`, `explainability`, `experiments`, and `utils`.
2. **Data Re-Organization**:
   - `NHANES AUG'21 - AUG'23/` $\to$ `data/raw/nhanes_2021_2023/` (all 27 raw XPTs preserved).
   - Canonical datasets moved to `data/processed/` (`final_cohort.csv`, `master_patient.csv`).
   - Cross-validation splits moved to `data/splits/` (`folds_v1.json`).
   - Feature manifests & audits moved to `data/metadata/` (`feature_manifest.json`, etc.).
3. **Artifact Restructuring**:
   - Graph tensors moved to `artifacts/graphs/patient_graphs.pt`.
   - All 112 experimental results, OOF CSVs, and metrics reorganized into `artifacts/results/` under `benchmarks/`, `leakage_gate/`, `statistical_tests/`, `explainability/`, and `experiments/`.
4. **Documentation Reconciliation**:
   - Reconciled all 12 sections of the technical evidence package into `docs/technical_evidence/`.
   - Created comprehensive technical guides across architecture, installation, dataset, graphs, models, training, experiments, results, and reproducibility.
5. **Testing Suite Modernization**:
   - Developed 8 dedicated test modules under `tests/` covering imports, data integrity, manifest hash, graph schema, model forward passes, leakage gate, experiment registry, and end-to-end pipeline smoke test.
   - 100% pass rate achieved across all 22 automated test cases.
