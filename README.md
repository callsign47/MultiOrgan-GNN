# HSGIN: Heterogeneous Systemic Graph Interaction Network for Multi-Organ Disease Modeling

[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch)](https://pytorch.org/)
[![PyTorch Geometric](https://img.shields.io/badge/PyG-2.3+-3C2179.svg)](https://pyg.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official repository for **HSGIN (Heterogeneous Systemic Graph Interaction Network)**, a multi-organ graph neural network architecture designed to model inter-organ interactions across **Liver, Kidney, and Heart/Cardiovascular** physiological domains for liver fibrosis risk assessment (continuous FIB-4 index) on the **NHANES August 2021–August 2023** cohort ($N = 6,277$).

---

## 🔬 Core Scientific Contributions

1. **Leakage-Free Multi-Organ Modeling**: Strictly excludes direct algebraic components of FIB-4 ($\text{Age}$, $\text{AST}$, $\text{ALT}$, $\text{Platelets}$) from model feature inputs, preventing mathematical identity leakage and enforcing genuine multi-organ relational learning.
2. **Heterogeneous Organ Graph Formulation**: Each patient is modeled as an isolated `HeteroData` graph featuring **5 node types** (`patient`, `liver`, `kidney`, `heart`, `biomarker`) and **14 directed edge types** encoding patient-affinity and physiological organ cross-talk.
3. **Multi-Organ Readout Architecture**: Outperforms strong tabular baselines (XGBoost $R^2 = 0.4519$, Classical HGNN $R^2 = 0.4681$) by achieving **$R^2 = 0.4976 \pm 0.0285$** under rigorous 5-fold cross-validation.
4. **Architectural Organ Ablation**: Demonstrates empirical gains across organ subgraphs: Liver-only ($R^2 = 0.3540$) $\to$ Liver+Kidney ($R^2 = 0.4394$) $\to$ Liver+Heart ($R^2 = 0.4592$) $\to$ Full 3-Organ ($R^2 = 0.4976$).

---

## 📊 Performance Benchmark Summary (5-Fold CV)

| Model Class | Architecture | Mean MAE ($\pm$ SD) | Mean RMSE ($\pm$ SD) | Mean $R^2$ ($\pm$ SD) | $\Delta R^2$ vs XGBoost |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Tabular Baseline** | Ridge Regression | $0.4065 \pm 0.0094$ | $0.6058 \pm 0.0386$ | $0.3869 \pm 0.0222$ | $-0.0650$ |
| **Tabular Baseline** | Random Forest | $0.3927 \pm 0.0093$ | $0.6019 \pm 0.0391$ | $0.3940 \pm 0.0409$ | $-0.0579$ |
| **Tabular Baseline** | XGBoost Regressor | $0.3740 \pm 0.0102$ | $0.5728 \pm 0.0417$ | $0.4519 \pm 0.0324$ | Baseline ($0.0000$) |
| **Tabular Baseline** | MLP Regressor | $0.4679 \pm 0.0280$ | $0.7204 \pm 0.0760$ | $0.1320 \pm 0.1152$ | $-0.3199$ |
| **Classical GNN** | Heterogeneous SAGE (HGNN) | $0.3648 \pm 0.0070$ | $0.5641 \pm 0.0337$ | $0.4681 \pm 0.0195$ | $+0.0162$ |
| **Proposed Model** | **HSGIN (Hetero GAT + Organ Readout)** | $\mathbf{0.3509 \pm 0.0091}$ | $\mathbf{0.5478 \pm 0.0287}$ | $\mathbf{0.4976 \pm 0.0285}$ | $\mathbf{+0.0457}$ |
| **Validation Control** | Y-Randomization Control | $0.5569 \pm 0.0070$ | $0.7838 \pm 0.0351$ | $-0.0280 \pm 0.0291$ | *No target leakage* |

---

## 📁 Repository Structure

```
├── .gitignore                          # Standard git ignore definitions
├── README.md                           # Project documentation and reproduction guide
├── requirements.txt                    # Core Python dependencies
├── generate_dataset_report.py          # Report generation script
├── HSGIN_3_Organ_Training_Pipeline_PRD.md # Project Requirements Document
├── data/
│   ├── cohort_flow.csv                 # 6-step cohort attrition counts (11,933 -> 6,277)
│   ├── experiment_results.json         # Master results record (Baselines, HSGIN, Ablations)
│   ├── feature_manifest.json           # Locked 25-feature manifest specification
│   ├── fib4_target_validation.json     # FIB-4 moments and validation metrics
│   ├── ingestion_summary.csv           # 27-file metadata audit verifying unique SEQN
│   ├── leakage_audit_results.json      # 3-experiment target leakage benchmark results
│   └── missingness_report.csv          # Per-feature missingness analysis (raw vs. cohort)
├── graphs/
│   └── .gitkeep                        # Output directory for patient_graphs.pt
├── reports/
│   ├── dataset_report.md               # Phase 1 dataset & missingness audit
│   ├── experiment_report.md            # Final experiment results & organ ablation report
│   ├── FINAL_MASTER_HANDOVER.md        # Master technical handover document
│   ├── leakage_audit_report.md         # Pre-training target-leakage audit
│   └── NHANES_Dataset_Report.md        # Complete dataset provenance & acquisition tutorial
└── src/
    ├── __init__.py
    ├── pipeline.py                     # Data ingestion, SEQN merging & cohort filtering
    ├── graph_builder.py                # PyG HeteroData graph construction
    ├── train.py                        # 5-fold CV training pipeline (Baselines + HSGIN)
    ├── hsgin_ablation.py               # HSGIN organ subgraph ablation suite (A-D)
    └── models/
        ├── __init__.py
        ├── baselines.py                # Classical HGNN and baseline model definitions
        └── hsgin.py                    # HSGIN architecture implementation
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/HSGIN.git
cd HSGIN
```

### 2. Set Up Environment
```bash
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📥 Data Acquisition: NHANES August 2021–August 2023

Download the official SAS Transport (`.XPT`) files from the **CDC/NCHS NHANES** repository:
**Official Portal**: `https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023`

Place the downloaded `.XPT` files in the following directory layout:
```
NHANES AUG'21 - AUG'23/
├── DEMO G/
│   └── DEMO_L.xpt
├── LABORATORY/
│   ├── ALB_CR_L.xpt
│   ├── BIOPRO_L.xpt
│   ├── CBC_L.xpt
│   ├── HDL_L.xpt
│   ├── HSCRP_L.xpt
│   └── TCHOL_L.xpt
├── EXAMINATION/
│   ├── BPXO_L.xpt
│   └── LUX_L.xpt
└── QUESTIONNAIRE/
    ├── BPQ_L.xpt
    ├── KIQ_U_L.xpt
    └── MCQ_L.xpt
```

*(Refer to [`reports/NHANES_Dataset_Report.md`](reports/NHANES_Dataset_Report.md) for a beginner-friendly tutorial on navigating and downloading these files).*

---

## 🚀 End-to-End Execution Pipeline

### Step 1: Ingest & Build the Final Cohort
Runs the multi-table `SEQN` left-join, applies the sequential inclusion filters, computes the continuous FIB-4 score, and saves `data/final_cohort.csv` ($N = 6,277$):
```bash
python src/pipeline.py
```

### Step 2: Build PyG Heterogeneous Patient Graphs
Converts `final_cohort.csv` into 6,277 PyTorch Geometric `HeteroData` graphs stored in `graphs/patient_graphs.pt`:
```bash
python src/graph_builder.py
```

### Step 3: Run Baseline & HSGIN 5-Fold Cross-Validation
Executes fold-isolated preprocessing, trains tabular baselines (Ridge, Random Forest, XGBoost, MLP), Classical HGNN, and the proposed HSGIN architecture:
```bash
python src/train.py
```

### Step 4: Run HSGIN Organ Ablation Study
Performs subgraph masking and trains 5-fold CV models across 4 organ configurations (**A**: Liver Only, **B**: Liver+Kidney, **C**: Liver+Heart, **D**: Full 3-Organ):
```bash
python src/hsgin_ablation.py
```

---

## 🧬 Graph Topology Specification

Each patient graph consists of **5 node types** and **14 directed edge types**:

```
                    [Patient (dim=1)]
                   /  |         |    \
                  /   |         |     \
          [Liver(6)] [Kidney(6)] [Heart(8)] [Biomarker(4)]
                 \     |      /
                  \    |     /
             (inter-organ crosstalk)
```

- **Node Features (25 Total)**:
  - `patient` (1): Gender (`RIAGENDR`)
  - `liver` (6): `LBXSGTSI`, `LBXSAL`, `LBXSTB`, `LBXSAPSI`, `LUXSMED`, `LUXCAPM`
  - `kidney` (6): `LBXSCR`, `LBXSBU`, `LBXSUA`, `URXUMA`, `URXUCR`, `KIQ022`
  - `heart` (8): `BPXOSY1`, `BPXODI1`, `BPXOPLS1`, `LBDHDD`, `LBXTC`, `BPQ020`, `MCQ160C`, `MCQ160E`
  - `biomarker` (4): `LBXWBCSI`, `LBXRBCSI`, `LBXHGB`, `LBXHSCRP`
- **Edges (14 Total)**:
  - 8 Patient-Organ edges (bidirectional `pertains_to` / `rev_pertains_to`)
  - 6 Inter-Organ edges (bidirectional `interacts_with` between `liver <-> kidney`, `liver <-> heart`, `kidney <-> heart`)

---

## 📄 Documentation & Reports

- [`reports/NHANES_Dataset_Report.md`](reports/NHANES_Dataset_Report.md): Complete data provenance, acquisition guide, and validation checklist.
- [`reports/experiment_report.md`](reports/experiment_report.md): Full empirical benchmarks, tabular ablation, and HSGIN organ ablation results.
- [`reports/leakage_audit_report.md`](reports/leakage_audit_report.md): Controlled target leakage audit report.
- [`reports/FINAL_MASTER_HANDOVER.md`](reports/FINAL_MASTER_HANDOVER.md): Full technical handover report.

---

## 📜 Citation & License

This project is licensed under the MIT License. Data from NHANES is in the public domain and provided by the CDC/NCHS.
