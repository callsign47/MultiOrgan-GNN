"""
ORGANIX Heterogeneous Graph Construction from Patient Clinical Profiles.
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import HeteroData

from organix.core.constants import FEATURE_DOMAINS, EDGE_TYPES
from organix.core.exceptions import GraphConstructionError


def build_patient_hetero_graph(patient_row: pd.Series) -> HeteroData:
    """
    Constructs a 5-node, 14-edge directed HeteroData graph for an individual patient.
    
    Nodes:
      - patient: [1, 1] (Gender: RIAGENDR)
      - liver: [1, 6] (LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM)
      - kidney: [1, 6] (LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022)
      - heart: [1, 8] (BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E)
      - biomarker: [1, 4] (LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP)
      
    Target:
      - patient.y: [1] (Continuous FIB-4 score)
    """
    data = HeteroData()
    data.patient_uid = str(patient_row.get("patient_uid", ""))
    data.SEQN = int(patient_row.get("SEQN", 0))

    # 1. Node Features
    # Patient demographics
    demo_feats = [patient_row[c] for c in FEATURE_DOMAINS["Demographics"]]
    data["patient"].x = torch.tensor([demo_feats], dtype=torch.float32)

    # Organ systems
    liver_feats = [patient_row[c] for c in FEATURE_DOMAINS["Liver"]]
    data["liver"].x = torch.tensor([liver_feats], dtype=torch.float32)

    kidney_feats = [patient_row[c] for c in FEATURE_DOMAINS["Kidney"]]
    data["kidney"].x = torch.tensor([kidney_feats], dtype=torch.float32)

    heart_feats = [patient_row[c] for c in FEATURE_DOMAINS["Heart"]]
    data["heart"].x = torch.tensor([heart_feats], dtype=torch.float32)

    biomarker_feats = [patient_row[c] for c in FEATURE_DOMAINS["Biomarker"]]
    data["biomarker"].x = torch.tensor([biomarker_feats], dtype=torch.float32)

    # Target
    if "fib4_target" in patient_row:
        data["patient"].y = torch.tensor([float(patient_row["fib4_target"])], dtype=torch.float32)

    # 2. Edges: Connect single node of src to single node of dst (index [0, 0])
    edge_idx = torch.tensor([[0], [0]], dtype=torch.long)
    for src, rel, dst in EDGE_TYPES:
        data[src, rel, dst].edge_index = edge_idx.clone()

    return data


def build_cohort_graphs(cohort_df: pd.DataFrame) -> List[HeteroData]:
    """Builds the full collection of HeteroData graphs for all patients in cohort."""
    graphs = []
    for _, row in cohort_df.iterrows():
        graphs.append(build_patient_hetero_graph(row))
    return graphs
