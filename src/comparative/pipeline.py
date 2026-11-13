import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

FINAL_COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"

# Excluded direct mathematical FIB-4 inputs
EXCLUDED_FEATURES = {'RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI'}

# 25 Leakage-Free Manifest Features grouped by domain
FEATURE_DOMAINS = {
    'Demographics': ['RIAGENDR'],
    'Liver': ['LBXSGTSI', 'LBXSAL', 'LBXSTB', 'LBXSAPSI', 'LUXSMED', 'LUXCAPM'],
    'Kidney': ['LBXSCR', 'LBXSBU', 'LBXSUA', 'URXUMA', 'URXUCR', 'KIQ022'],
    'Heart': ['BPXOSY1', 'BPXODI1', 'BPXOPLS1', 'LBDHDD', 'LBXTC', 'BPQ020', 'MCQ160C', 'MCQ160E'],
    'Biomarker': ['LBXWBCSI', 'LBXRBCSI', 'LBXHGB', 'LBXHSCRP']
}

def get_leak_free_feature_list():
    features = []
    for domain, cols in FEATURE_DOMAINS.items():
        features.extend(cols)
    return features

def get_5fold_splits(df, n_splits=5, seed=42):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    patient_ids = df['patient_uid'].unique()
    splits = []
    for train_idx, val_idx in kf.split(patient_ids):
        train_uids = patient_ids[train_idx]
        val_uids = patient_ids[val_idx]
        splits.append((train_uids, val_uids))
    return splits

def preprocess_fold_tabular(df, train_uids, val_uids, feature_cols):
    train_df = df[df['patient_uid'].isin(train_uids)].copy()
    val_df = df[df['patient_uid'].isin(val_uids)].copy()
    
    X_train_raw = train_df[feature_cols].values
    y_train = train_df['fib4_target'].values
    
    X_val_raw = val_df[feature_cols].values
    y_val = val_df['fib4_target'].values
    
    # Fold-safe median imputation & standardization
    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    
    X_train = scaler.fit_transform(imputer.fit_transform(X_train_raw))
    X_val = scaler.transform(imputer.transform(X_val_raw))
    
    return X_train, y_train, X_val, y_val, imputer, scaler

def preprocess_fold_graphs(graph_list, train_uids, val_uids):
    # Separate graph lists by fold
    train_graphs = [g for g in graph_list if g.patient_uid in set(train_uids)]
    val_graphs = [g for g in graph_list if g.patient_uid in set(val_uids)]
    
    # Extract node type dimensions
    node_types = train_graphs[0].node_types
    
    # Fit imputers and scalers per node type strictly on train_graphs
    preprocessors = {}
    for ntype in node_types:
        raw_node_feats = torch.cat([g[ntype].x for g in train_graphs], dim=0).numpy()
        imp = SimpleImputer(strategy='median')
        scl = StandardScaler()
        scl.fit(imp.fit_transform(raw_node_feats))
        preprocessors[ntype] = (imp, scl)
        
    # Transform train and val graph node feature matrices
    processed_train_graphs = []
    for g in train_graphs:
        g_proc = g.clone()
        for ntype in node_types:
            imp, scl = preprocessors[ntype]
            raw_x = g[ntype].x.numpy()
            proc_x = scl.transform(imp.transform(raw_x))
            g_proc[ntype].x = torch.tensor(proc_x, dtype=torch.float32)
        processed_train_graphs.append(g_proc)
        
    processed_val_graphs = []
    for g in val_graphs:
        g_proc = g.clone()
        for ntype in node_types:
            imp, scl = preprocessors[ntype]
            raw_x = g[ntype].x.numpy()
            proc_x = scl.transform(imp.transform(raw_x))
            g_proc[ntype].x = torch.tensor(proc_x, dtype=torch.float32)
        processed_val_graphs.append(g_proc)
        
    return processed_train_graphs, processed_val_graphs
