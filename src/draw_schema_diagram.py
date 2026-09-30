import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\hsgin_hetero_schema.png"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def draw_schema():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    # Positions
    pos = {
        'patient': (0.5, 0.5),
        'liver': (0.2, 0.8),
        'kidney': (0.8, 0.8),
        'heart': (0.2, 0.2),
        'biomarker': (0.8, 0.2)
    }

    colors = {
        'patient': '#38bdf8',    # Sky Blue
        'liver': '#4ade80',      # Green
        'kidney': '#fb923c',     # Orange
        'heart': '#f87171',      # Red
        'biomarker': '#c084fc'   # Purple
    }

    labels = {
        'patient': "PATIENT NODE\n[1 Feature: Gender]\nTarget: FIB-4 Score",
        'liver': "LIVER NODE\n[6 Features]\n(GGT, Albumin, Bilirubin,\nALP, FibroScan, CAP)",
        'kidney': "KIDNEY NODE\n[6 Features]\n(Creatinine, BUN, Uric Acid,\nUrine Alb/Cr, Kidney Hist)",
        'heart': "HEART NODE\n[8 Features]\n(BP Sys/Dia, Pulse, HDL,\nChol, HTN, CHD, Heart Attack)",
        'biomarker': "BIOMARKER NODE\n[4 Features]\n(WBC, RBC, HGB, hs-CRP)"
    }

    # Draw Inter-Organ Edges (Red dashed, bidirectional)
    inter_organ_pairs = [
        ('liver', 'kidney'),
        ('liver', 'heart'),
        ('kidney', 'heart')
    ]

    for src, dst in inter_organ_pairs:
        x1, y1 = pos[src]
        x2, y2 = pos[dst]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color="#f43f5e", lw=2.5, linestyle="--", shrinkA=45, shrinkB=45))

    # Draw Patient-Organ Edges (Solid blue/grey, bidirectional)
    organ_nodes = ['liver', 'kidney', 'heart', 'biomarker']
    for org in organ_nodes:
        x1, y1 = pos['patient']
        x2, y2 = pos[org]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color="#94a3b8", lw=2, shrinkA=45, shrinkB=45))

    # Draw Nodes
    for node, (x, y) in pos.items():
        size = 0.12 if node == 'patient' else 0.10
        circle = plt.Circle((x, y), size, color=colors[node], ec='white', lw=2, zorder=4)
        ax.add_patch(circle)
        
        # Node Text
        ax.text(x, y, labels[node], color='#0f172a' if node == 'patient' else '#0f172a',
                fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)

    # Title & Edge Legend
    ax.set_title("HSGIN 3-Organ Heterogeneous Graph Architecture Schema\n(5 Node Types | 14 Bidirectional Edge Types | Leakage-Controlled Setup)",
                 color='#f8fafc', fontsize=14, fontweight='bold', pad=20)

    # Legend patches
    solid_patch = mpatches.Patch(color='#94a3b8', label='Patient-Organ Edges (8 edge types: pertains_to / rev_pertains_to)')
    dash_patch = mpatches.Patch(color='#f43f5e', label='Inter-Organ Systemic Edges (6 edge types: interacts_with bidirectional)')
    ax.legend(handles=[solid_patch, dash_patch], loc='lower center', bbox_to_anchor=(0.5, -0.05),
              ncol=2, facecolor='#1e293b', edgecolor='none', labelcolor='#f8fafc', fontsize=9.5)

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.08, 1.05)
    ax.axis('off')

    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    plt.close()
    print(f"Saved precise schema diagram to {OUTPUT_PATH}")

if __name__ == "__main__":
    draw_schema()
