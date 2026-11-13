# ORGANIX: Heterogeneous Graph Construction Guide

## 1. Graph Formulation

In ORGANIX, each patient is represented as an independent heterogeneous graph $G = (V, E)$ using PyTorch Geometric (`torch_geometric.data.HeteroData`):
- **Nodes $V$**: 5 nodes corresponding to physiological biological compartments:
  - Patient Node ($v_{\text{patient}} \in \mathbb{R}^1$)
  - Liver Node ($v_{\text{liver}} \in \mathbb{R}^6$)
  - Kidney Node ($v_{\text{kidney}} \in \mathbb{R}^6$)
  - Heart Node ($v_{\text{heart}} \in \mathbb{R}^8$)
  - Biomarker Node ($v_{\text{biomarker}} \in \mathbb{R}^4$)
- **Edges $E$**: 14 directed relations encoding biological connectivity:
  - 8 affinity edges between patient and organ/biomarker nodes.
  - 6 bi-directional cross-talk edges between Liver, Kidney, and Heart.

---

## 2. Programmatic Construction

```python
from organix.data.cohort import load_final_cohort
from organix.graphs.builder import build_cohort_graphs

# Load canonical cohort (N=6,277)
df = load_final_cohort()

# Construct PyG HeteroData graphs
graphs = build_cohort_graphs(df)

print(f"Constructed {len(graphs)} patient graphs.")
print("Sample Graph:", graphs[0])
```

---

## 3. Fold-Safe Graph Preprocessing

To prevent out-of-fold data contamination, all imputers (median) and feature scalers (`StandardScaler`) must be fitted **exclusively on the training fold graph partitions**:

```python
from organix.data.splits import load_or_generate_splits
from organix.graphs.dataset import preprocess_fold_graphs, load_patient_graphs

# Load graphs and split definitions
all_graphs = load_patient_graphs()
splits = load_or_generate_splits()

fold_1 = splits["folds"][0]
train_graphs, val_graphs = preprocess_fold_graphs(
    graph_list=all_graphs,
    train_uids=fold_1["train_patient_uids"],
    val_uids=fold_1["val_patient_uids"],
)
```
