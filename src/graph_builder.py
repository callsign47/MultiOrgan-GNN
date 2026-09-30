import os
import torch
import pandas as pd
import json
from torch_geometric.data import HeteroData

FINAL_COHORT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\final_cohort.csv"
FEATURE_MANIFEST_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\data\feature_manifest.json"
OUTPUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Direct mathematical components excluded to control leakage
EXCLUDED_FEATURES = {'RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI'}

def get_leak_free_organ_taxonomy(manifest):
    taxonomy = {}
    for domain, items in manifest.items():
        retained = [item['feature'] for item in items if item['feature'] not in EXCLUDED_FEATURES]
        if retained:
            taxonomy[domain] = retained
    return taxonomy

def build_patient_hetero_graph(patient_row, taxonomy):
    data = HeteroData()
    
    # Node features (using raw values; scaling/imputation handled in-fold)
    # Patient Node (Gender)
    patient_feats = [patient_row['RIAGENDR']]
    data['patient'].x = torch.tensor([patient_feats], dtype=torch.float32)
    
    # Liver Node
    liver_cols = taxonomy.get('Liver', [])
    liver_feats = [patient_row[c] for c in liver_cols]
    data['liver'].x = torch.tensor([liver_feats], dtype=torch.float32)
    
    # Kidney Node
    kidney_cols = taxonomy.get('Kidney', [])
    kidney_feats = [patient_row[c] for c in kidney_cols]
    data['kidney'].x = torch.tensor([kidney_feats], dtype=torch.float32)
    
    # Heart Node
    heart_cols = taxonomy.get('Heart', [])
    heart_feats = [patient_row[c] for c in heart_cols]
    data['heart'].x = torch.tensor([heart_feats], dtype=torch.float32)
    
    # Biomarker Node
    biomarker_cols = taxonomy.get('Biomarker', [])
    biomarker_feats = [patient_row[c] for c in biomarker_cols]
    data['biomarker'].x = torch.tensor([biomarker_feats], dtype=torch.float32)
    
    # Patient-Organ Edges (bidirectional)
    edge_0_0 = torch.tensor([[0], [0]], dtype=torch.long)
    data['patient', 'pertains_to', 'liver'].edge_index = edge_0_0
    data['liver', 'rev_pertains_to', 'patient'].edge_index = edge_0_0
    
    data['patient', 'pertains_to', 'kidney'].edge_index = edge_0_0
    data['kidney', 'rev_pertains_to', 'patient'].edge_index = edge_0_0
    
    data['patient', 'pertains_to', 'heart'].edge_index = edge_0_0
    data['heart', 'rev_pertains_to', 'patient'].edge_index = edge_0_0
    
    data['patient', 'pertains_to', 'biomarker'].edge_index = edge_0_0
    data['biomarker', 'rev_pertains_to', 'patient'].edge_index = edge_0_0
    
    # Inter-Organ Systemic Directed Edges
    data['liver', 'interacts_with', 'kidney'].edge_index = edge_0_0
    data['kidney', 'interacts_with', 'liver'].edge_index = edge_0_0
    
    data['liver', 'interacts_with', 'heart'].edge_index = edge_0_0
    data['heart', 'interacts_with', 'liver'].edge_index = edge_0_0
    
    data['kidney', 'interacts_with', 'heart'].edge_index = edge_0_0
    data['heart', 'interacts_with', 'kidney'].edge_index = edge_0_0
    
    # Target and Identifiers
    data['patient'].y = torch.tensor([patient_row['fib4_target']], dtype=torch.float32)
    data.patient_uid = str(patient_row['patient_uid'])
    data.SEQN = int(patient_row['SEQN'])
    
    return data

def build_all_graphs(cohort_path=FINAL_COHORT_PATH, manifest_path=FEATURE_MANIFEST_PATH):
    print("--- Starting PyG HeteroData Graph Construction (Leakage-Free Setup) ---")
    df = pd.read_csv(cohort_path)
    with open(manifest_path) as f:
        manifest = json.load(f)
        
    taxonomy = get_leak_free_organ_taxonomy(manifest)
    print("Leakage-Free Taxonomy Node Feature Mapping:")
    for dom, cols in taxonomy.items():
        print(f"  - {dom} ({len(cols)} feats): {cols}")
        
    graph_list = []
    for _, row in df.iterrows():
        g = build_patient_hetero_graph(row, taxonomy)
        graph_list.append(g)
        
    output_path = os.path.join(OUTPUT_DIR, "patient_graphs.pt")
    torch.save(graph_list, output_path)
    print(f"\nSuccessfully generated and saved {len(graph_list)} PyG HeteroData graphs to: {output_path}")
    
    # Verification checks on first graph
    sample_g = graph_list[0]
    print("\nSample Graph Summary:")
    print(f"  - Patient UID: {sample_g.patient_uid}")
    print(f"  - Target FIB-4: {sample_g['patient'].y.item():.4f}")
    print(f"  - Node Types & Feature Shapes:")
    for ntype in sample_g.node_types:
        print(f"      * {ntype}: {sample_g[ntype].x.shape}")
    print(f"  - Edge Types ({len(sample_g.edge_types)} total): {sample_g.edge_types[:4]}...")
    
    return graph_list, taxonomy

if __name__ == "__main__":
    build_all_graphs()
