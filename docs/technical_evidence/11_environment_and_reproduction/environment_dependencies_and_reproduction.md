# Computational Environment, Dependency Versions, and Reproduction Protocol

**Operating System**: Windows 10 / Windows 11 Enterprise (`Windows-10-10.0.26200-SP0`)  
**Python Runtime**: Python 3.10.0 (64-bit AMD64)  
**Acceleration Hardware**: NVIDIA CUDA GPU Acceleration Enabled (`torch.cuda.is_available() == True`)  
**Status**: `VERIFIED-ON-DISK` (Direct System & Package Inspection)  

---

## 1. Environment Details & Installed Package Versions

The following table provides the exact pinned library versions utilized across all comparative experiments:

| Software Component / Library | Pinned Version in Environment | Minimum Spec (`requirements.txt`) | Primary Architectural Role |
| :--- | :--- | :--- | :--- |
| **Python** | **3.10.0** (`tags/v3.10.0:b494f59`) | $\ge 3.9$ | Core runtime |
| **PyTorch (`torch`)** | **2.5.1+cu121** | $\ge 2.0.0$ | Deep neural networks, tensor ops, GPU autograd |
| **PyTorch Geometric (`torch_geometric`)** | **2.8.0.post1** | $\ge 2.3.0$ | HeteroData graphs, GATConv, HeteroConv |
| **NumPy (`numpy`)** | **1.23.5** | $\ge 1.23.0$ | Numerical arrays, matrix operations, seeds |
| **Pandas (`pandas`)** | **2.3.3** | $\ge 1.5.0$ | Dataframe manipulation, outer joins, CSV I/O |
| **Scikit-Learn (`scikit-learn`)** | **1.7.2** | $\ge 1.2.0$ | Preprocessing (imputer/scaler), linear models, trees |
| **SciPy (`scipy`)** | **1.15.3** | $\ge 1.10.0$ | Statistical tests, skewness, Spearman $\rho$, SLSQP |
| **XGBoost (`xgboost`)** | **3.2.0** | $\ge 1.7.0$ | Hist-gradient boosting trees |
| **CatBoost (`catboost`)** | **1.2.10** | Unspecified | Symmetric oblivious decision trees |
| **LightGBM (`lightgbm`)** | **4.7.0** | Unspecified | Leaf-wise gradient boosting trees |
| **PyTorch-TabNet (`pytorch-tabnet`)** | **4.1.0** | Unspecified | Sparse sequential attention for tabular data |
| **tqdm (`tqdm`)** | **4.70.0** | $\ge 4.65.0$ | Progress meters across cross-validation folds |

---

## 2. Requirements File (`requirements.txt`)

Located at [`requirements.txt`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/requirements.txt):
```text
torch>=2.0.0
torch-geometric>=2.3.0
numpy>=1.23.0
pandas>=1.5.0
scikit-learn>=1.2.0
scipy>=1.10.0
xgboost>=1.7.0
pyreadstat>=1.2.0
tqdm>=4.65.0
```

---

## 3. Authoritative Reproduction Commands

To replicate any phase of the study, execute the corresponding command from the project root directory (`c:\Users\admin_fix\Downloads\3 ORGAN`):

### 3.1 Automated Verification & Integrity Gates (Read-Only)
```powershell
# 1. Run full unit test suite (preservation, splits, leakage gate)
python -m unittest discover tests

# 2. Execute stand-alone leakage gate audit
python -c "from src.comparative.leakage_gate import run_leakage_gate; run_leakage_gate()"

# 3. Verify baseline v1 snapshot checksum parity
python tests/test_preservation.py
```

### 3.2 Experiment Reproduction Sequence (Exp 0 – Exp 9)

```powershell
# Experiment 0: Baseline Reproduction (reproduces reported Phase 1/2 baselines)
python src/comparative/exp0_reproduction.py

# Experiment 1: Linear & Conventional Trees (Ridge, ElasticNet, RF, Extra Trees)
python src/comparative/exp1_linear_trees.py

# Experiment 2: Advanced Gradient Boosting (XGBoost, CatBoost, LightGBM, HistGB)
python src/comparative/exp2_boosting.py

# Experiment 3: Deep Tabular Architectures (MLP Retuned, FT-Transformer, TabNet)
python src/comparative/exp3_deep_tabular.py

# Experiment 4: Graph Neural Networks Multi-Seed (Classical HGNN, HSGIN)
python src/comparative/exp4_gnn.py

# Experiment 5: Audited Leakage-Free Ensembling (NNW Blend, Ridge Stacking)
python src/comparative/exp5_ensemble.py

# Experiment 6: Feature-Domain Ablations (XGBoost & HSGIN Leave-One-Out)
python src/comparative/run_exp6_xgboost.py
python src/comparative/run_exp6b_hsgin.py

# Experiment 7: Graph Architecture Ablations & RandomEdges Null Control
python src/comparative/run_exp7_graph_ablations.py
python src/comparative/run_exp7_random_edges_multiseed.py

# Experiment 8: Y-Randomization (100 perms) & Deliberate Leaky Controls
python src/comparative/run_exp8_controls.py
python src/comparative/run_exp8_hsgin_100perms.py

# Experiment 9: Clinical Subgroup & Robustness Analysis
python src/comparative/run_exp9_subgroups.py

# Phase 8 Master Benchmark Synthesis & Feature Permutation Explainability
python src/comparative/run_phase8_synthesis.py
```

---

## 4. Hardware Environment & Runtime Profiling

| Experimental Component | Hardware Device | Approximate Wall-Clock Execution Time |
| :--- | :--- | :--- |
| **Data Ingestion & Cohort Filter** | AMD64 CPU | $\approx 25$ seconds |
| **PyG Graph Construction (6,277 graphs)** | AMD64 CPU | $\approx 45$ seconds |
| **Experiment 0 (Reproduction)** | NVIDIA CUDA GPU | $\approx 2.5$ minutes |
| **Experiment 1 (Linear & Trees)** | AMD64 CPU (Multiprocess) | $\approx 40$ seconds |
| **Experiment 2 (Gradient Boosting)** | AMD64 CPU / GPU | $\approx 1.2$ minutes |
| **Experiment 3 (Deep Tabular, 3 Seeds)** | NVIDIA CUDA GPU | $\approx 35$ minutes |
| **Experiment 4 (GNNs, 3 Seeds)** | NVIDIA CUDA GPU | $\approx 160$ minutes ($\approx 2.7$ hours) |
| **Experiment 5 (Nested Stacking)** | NVIDIA CUDA GPU / CPU | $\approx 12$ minutes |
| **Experiment 6 (Domain Ablations)** | NVIDIA CUDA GPU / CPU | $\approx 45$ minutes |
| **Experiment 7 (Graph Variants & ER Null)**| NVIDIA CUDA GPU | $\approx 55$ minutes |
| **Experiment 8 (HSGIN 100 Permutations)** | NVIDIA CUDA GPU (Multiprocess)| $\approx 16$ minutes |
| **Experiment 9 (Subgroups & Classification)**| AMD64 CPU | $\approx 15$ seconds |
