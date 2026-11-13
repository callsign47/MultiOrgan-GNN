# ORGANIX: Architecture Overview

## 1. System Mission & Physiological Rationale

**ORGANIX** is an open-source, reproducible computational medicine framework implementing the **Heterogeneous Systemic Graph Interaction Network (HSGIN)** for patient-level multi-organ risk stratification.

### The Scientific Challenge
The standard **Fibrosis-4 (FIB-4)** index is an established clinical surrogate for non-alcoholic fatty liver disease (NAFLD) and metabolic dysfunction-associated steatotic liver disease (MASLD) fibrosis progression. The mathematical formula is:

$$\text{FIB-4} = \frac{\text{Age} \times \text{AST}}{\text{Platelet Count} \times \sqrt{\text{ALT}}}$$

Because FIB-4 is an explicit deterministic function of these four clinical inputs, including any of them directly in a predictive model introduces algebraic target leakage ($R^2 \approx 1.00$). 

**ORGANIX enforces strict algebraic leakage control**:
By strictly excluding $\text{Age}, \text{AST}, \text{ALT},$ and $\text{Platelet Count}$ from the feature matrix, ORGANIX investigates the physiological inter-organ cross-talk between **Liver, Kidney, and Heart/Cardiovascular** domains, answering:
> *How much variance in liver fibrosis risk can be captured solely through systemic, multi-organ clinical biomarkers when direct formula components are strictly omitted?*

---

## 2. Package Architecture

The code is organized into a modular Python package located at `src/organix/`:

```
src/organix/
├── __init__.py           # Package root, versioning, top-level exports
├── core/
│   ├── config.py         # PathConfig and OrganixConfig using pathlib.Path
│   ├── constants.py      # Locked 25 features, domains, node & edge definitions
│   ├── exceptions.py     # Domain-specific exceptions (LeakageGateError, etc.)
│   └── logging.py        # Structured logging configuration
├── data/
│   ├── cohort.py         # Cohort validation, N=6,277 integrity verification
│   ├── manifest.py       # Cryptographic feature manifest loading and verification
│   ├── target.py         # FIB-4 formula computation and moment statistics
│   ├── splits.py         # 5-fold cross-validation generation & disjointness audit
│   ├── preprocessing.py  # Fold-safe median imputation & standardization
│   └── ingestion.py      # CDC NHANES SAS transport (XPT) ingestion
├── graphs/
│   ├── schema.py         # 5 node types, 14 directed relations specification
│   ├── builder.py        # HeteroData patient graph builder
│   └── dataset.py        # PyG dataset loader & fold-safe graph preprocessor
├── models/
│   ├── hsgin.py          # HSGIN architecture (HeteroOrganConvBlock, Organ Readout)
│   ├── baselines.py      # ClassicalHGNN, StandardGNNBaseline, Scikit-Learn adapters
│   ├── deep_tabular.py   # FT-Transformer, Deep Tabular MLP
│   └── layers.py         # Residual linear blocks and shared layers
├── training/
│   ├── trainer.py        # Deterministic PyG graph & tabular training loops
│   └── loss.py           # MSE, MAE, and Huber loss implementations
├── evaluation/
│   ├── metrics.py        # R^2, RMSE, MAE, Spearman rho, Pearson r, fold aggregation
│   ├── leakage_gate.py   # 4-tier automated leakage verification gate
│   ├── statistical_tests.py # Paired bootstrap test, Holm-Bonferroni, Benjamini-Hochberg FDR
│   └── subgroups.py      # Demographic & clinical subgroup stratification
├── explainability/
│   ├── attribution.py    # Held-out feature permutation importance & domain share
│   └── ablations.py      # Leave-One-Domain-Out and Single-Domain feature sets
├── experiments/
│   ├── base.py           # Abstract Base Experiment interface
│   └── registry.py       # Central registry for Exp0 through Exp9
├── utils/
│   ├── paths.py          # PathManager resolving paths dynamically from repo root
│   ├── seeding.py        # Deterministic seed_everything (Python, NumPy, PyTorch, CUDA)
│   └── io.py             # SHA-256 computation, atomic JSON/CSV I/O
└── cli.py                # Command-Line Interface (organix gate, verify, experiments)
```

---

## 3. Heterogeneous Graph Schema

Each patient is formulated as an isolated `HeteroData` graph:
- **5 Node Types**:
  1. `patient`: [1, 1] — Demographics (`RIAGENDR`)
  2. `liver`: [1, 6] — `LBXSGTSI`, `LBXSAL`, `LBXSTB`, `LBXSAPSI`, `LUXSMED`, `LUXCAPM`
  3. `kidney`: [1, 6] — `LBXSCR`, `LBXSBU`, `LBXSUA`, `URXUMA`, `URXUCR`, `KIQ022`
  4. `heart`: [1, 8] — `BPXOSY1`, `BPXODI1`, `BPXOPLS1`, `LBDHDD`, `LBXTC`, `BPQ020`, `MCQ160C`, `MCQ160E`
  5. `biomarker`: [1, 4] — `LBXWBCSI`, `LBXRBCSI`, `LBXHGB`, `LBXHSCRP`
- **14 Directed Edge Types**:
  - Patient-to-Organ & Organ-to-Patient affinity edges (8 directed edges).
  - Inter-Organ physiological cross-talk edges between Liver, Kidney, and Heart (6 directed edges).
