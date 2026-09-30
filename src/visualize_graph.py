import os
import sys
import torch
import networkx as nx
import matplotlib.pyplot as plt

GRAPH_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
OUTPUT_DIR = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def visualize_patient_graph(sample_idx=0):
    if not os.path.exists(GRAPH_PATH):
        print(f"Error: {GRAPH_PATH} not found!")
        return

    graph_list = torch.load(GRAPH_PATH)
    data = graph_list[sample_idx]

    print(f"Visualizing Patient Graph index {sample_idx} (UID: {data.patient_uid}, FIB-4: {data['patient'].y.item():.4f})...")

    G = nx.DiGraph()

    # Define Node Colors & Positions
    # Center: Patient. Inner ring: Organs & Biomarkers.
    node_colors = {
        'patient': '#1f77b4',     # Steel Blue
        'liver': '#2ca02c',       # Forest Green
        'kidney': '#ff7f0e',      # Amber / Orange
        'heart': '#d62728',       # Crimson Red
        'biomarker': '#9467bd'    # Purple
    }

    pos = {
        'patient': (0, 0),
        'liver': (-1.5, 1.2),
        'kidney': (1.5, 1.2),
        'heart': (-1.5, -1.2),
        'biomarker': (1.5, -1.2)
    }

    labels = {}
    color_map = []
    node_sizes = []

    # Add Nodes with Metadata Labels
    for ntype in data.node_types:
        G.add_node(ntype)
        feat_dim = data[ntype].x.shape[1]
        color_map.append(node_colors.get(ntype, '#7f7f7f'))

        if ntype == 'patient':
            labels[ntype] = f"PATIENT\n(UID: {data.patient_uid})\nFIB-4: {data['patient'].y.item():.2f}"
            node_sizes.append(4000)
        else:
            labels[ntype] = f"{ntype.upper()}\n({feat_dim} features)"
            node_sizes.append(3000)

    # Add Edges from HeteroData
    edge_tuples = []
    for edge_type in data.edge_types:
        src, rel, dst = edge_type
        # Extract edge connection
        edge_index = data[edge_type].edge_index
        if edge_index.shape[1] > 0:
            G.add_edge(src, dst, label=rel)
            edge_tuples.append((src, dst, rel))

    # Plot Figure
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_title(f"HSGIN 3-Organ Heterogeneous Patient Graph\nPatient UID: {data.patient_uid} | Target FIB-4 = {data['patient'].y.item():.3f}", fontsize=14, fontweight='bold', pad=15)

    # Draw Nodes
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=node_sizes, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='white', font_weight='bold', ax=ax)

    # Draw Edges (Curved for bidirectional readability)
    patient_edges = [(u, v) for u, v, r in edge_tuples if 'pertains' in r]
    organ_edges = [(u, v) for u, v, r in edge_tuples if 'interacts' in r]

    nx.draw_networkx_edges(G, pos, edgelist=patient_edges, edge_color='#555555', width=2, arrowsize=15, connectionstyle="arc3,rad=0.1", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=organ_edges, edge_color='#d62728', width=2.5, style='dashed', arrowsize=15, connectionstyle="arc3,rad=0.15", ax=ax)

    # Legend
    plt.plot([], [], color='#555555', linewidth=2, label='Patient-Organ Affinity Edges')
    plt.plot([], [], color='#d62728', linewidth=2.5, linestyle='--', label='Inter-Organ Systemic Interaction Edges')
    plt.legend(loc='upper right', frameon=True, facecolor='#f8f9fa', edgecolor='none')

    plt.axis('off')
    plt.tight_layout()

    out_file = os.path.join(OUTPUT_DIR, "patient_graph_sample.png")
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved patient graph visualization to: {out_file}")

if __name__ == "__main__":
    visualize_patient_graph()
