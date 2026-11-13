"""
ORGANIX PyG HeteroData Graph Dataset and Fold Preprocessing.
"""

from pathlib import Path
from typing import List, Tuple, Optional, Dict
import torch
from torch_geometric.data import HeteroData
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from organix.utils.paths import get_paths


def load_patient_graphs(graph_path: Optional[Path] = None) -> List[HeteroData]:
    """
    Loads pre-computed patient HeteroData graphs from disk.
    """
    path = graph_path or get_paths().patient_graphs_path
    if not path.is_file():
        raise FileNotFoundError(f"Patient graphs file not found: {path}")
    return torch.load(path, weights_only=False)


def preprocess_fold_graphs(
    graph_list: List[HeteroData],
    train_uids: List[str],
    val_uids: List[str],
) -> Tuple[List[HeteroData], List[HeteroData]]:
    """
    Fold-safe heterogeneous graph preprocessing:
    SimpleImputer (median) and StandardScaler are fitted per node type
    EXCLUSIVELY on train_graphs, strictly preventing out-of-fold leakage.
    """
    train_set = set(train_uids)
    val_set = set(val_uids)

    train_graphs = [g for g in graph_list if getattr(g, "patient_uid", "") in train_set]
    val_graphs = [g for g in graph_list if getattr(g, "patient_uid", "") in val_set]

    if not train_graphs or not val_graphs:
        raise ValueError("Train or validation graph partition is empty! Verify patient_uid matching.")

    node_types = train_graphs[0].node_types
    preprocessors: Dict[str, Tuple[SimpleImputer, StandardScaler]] = {}

    for ntype in node_types:
        raw_feats = torch.cat([g[ntype].x for g in train_graphs], dim=0).numpy()
        imp = SimpleImputer(strategy="median")
        scl = StandardScaler()
        scl.fit(imp.fit_transform(raw_feats))
        preprocessors[ntype] = (imp, scl)

    # Transform train graphs
    processed_train = []
    for g in train_graphs:
        g_proc = g.clone()
        for ntype in node_types:
            imp, scl = preprocessors[ntype]
            raw_x = g[ntype].x.numpy()
            proc_x = scl.transform(imp.transform(raw_x))
            g_proc[ntype].x = torch.tensor(proc_x, dtype=torch.float32)
        processed_train.append(g_proc)

    # Transform val graphs
    processed_val = []
    for g in val_graphs:
        g_proc = g.clone()
        for ntype in node_types:
            imp, scl = preprocessors[ntype]
            raw_x = g[ntype].x.numpy()
            proc_x = scl.transform(imp.transform(raw_x))
            g_proc[ntype].x = torch.tensor(proc_x, dtype=torch.float32)
        processed_val.append(g_proc)

    return processed_train, processed_val
