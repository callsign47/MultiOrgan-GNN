import os
import json
import torch

GRAPH_PATH = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\patient_graphs.pt"
OUTPUT_HTML = r"c:\Users\admin_fix\Downloads\3 ORGAN\graphs\hsgin_interactive_graph.html"

def generate_interactive_html(sample_idx=0):
    if not os.path.exists(GRAPH_PATH):
        print(f"Error: {GRAPH_PATH} not found!")
        return

    graph_list = torch.load(GRAPH_PATH)
    data = graph_list[sample_idx]

    # Node attributes
    node_info = {
        'patient': {'label': f"PATIENT ({data.patient_uid})", 'color': '#1f77b4', 'size': 35, 'group': 'Patient', 'details': f"Gender: {int(data['patient'].x[0,0].item())}, Target FIB-4: {data['patient'].y.item():.4f}"},
        'liver': {'label': 'LIVER NODE', 'color': '#2ca02c', 'size': 28, 'group': 'Organ', 'details': f"Features (6): GGT, Albumin, Bilirubin, ALP, FibroScan Median, CAP"},
        'kidney': {'label': 'KIDNEY NODE', 'color': '#ff7f0e', 'size': 28, 'group': 'Organ', 'details': f"Features (6): Creatinine, BUN, Uric Acid, Urine Albumin, Urine Creatinine, Kidney Disease History"},
        'heart': {'label': 'HEART / CARDIO NODE', 'color': '#d62728', 'size': 28, 'group': 'Organ', 'details': f"Features (8): Systolic BP, Diastolic BP, Pulse, HDL, Total Chol, Hypertension, CHD, Heart Attack"},
        'biomarker': {'label': 'BIOMARKER NODE', 'color': '#9467bd', 'size': 28, 'group': 'Biomarker', 'details': f"Features (4): WBC, RBC, Hemoglobin, hs-CRP"}
    }

    nodes = []
    for ntype, info in node_info.items():
        nodes.append({
            'id': ntype,
            'label': info['label'],
            'color': info['color'],
            'size': info['size'],
            'title': f"<b>{info['label']}</b><br>{info['details']}"
        })

    edges = []
    # Add Patient-Organ Edges
    for org in ['liver', 'kidney', 'heart', 'biomarker']:
        edges.append({'from': 'patient', 'to': org, 'label': 'pertains_to', 'color': {'color': '#666666'}, 'arrows': 'to;from'})

    # Add Inter-Organ Systemic Edges
    edges.append({'from': 'liver', 'to': 'kidney', 'label': 'interacts_with', 'color': {'color': '#e74c3c'}, 'dashes': True, 'arrows': 'to;from'})
    edges.append({'from': 'liver', 'to': 'heart', 'label': 'interacts_with', 'color': {'color': '#e74c3c'}, 'dashes': True, 'arrows': 'to;from'})
    edges.append({'from': 'kidney', 'to': 'heart', 'label': 'interacts_with', 'color': {'color': '#e74c3c'}, 'dashes': True, 'arrows': 'to;from'})

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>HSGIN Heterogeneous Graph Visualizer</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #0f172a;
            color: #f8fafc;
        }}
        #header {{
            margin-bottom: 15px;
            text-align: center;
        }}
        h1 {{
            margin: 0 0 5px 0;
            font-size: 24px;
            color: #38bdf8;
        }}
        p {{
            margin: 0;
            color: #94a3b8;
            font-size: 14px;
        }}
        #mynetwork {{
            width: 100%;
            height: 600px;
            border: 1px solid #334155;
            border-radius: 12px;
            background-color: #1e293b;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .legend {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            font-size: 13px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>HSGIN 3-Organ Heterogeneous Patient Graph</h1>
        <p>Patient UID: <b>{data.patient_uid}</b> | Target FIB-4 Score = <b>{data['patient'].y.item():.4f}</b> (Drag nodes to inspect interaction topology)</p>
    </div>

    <div id="mynetwork"></div>

    <div class="legend">
        <div class="legend-item"><div class="dot" style="background: #1f77b4;"></div> Patient Node</div>
        <div class="legend-item"><div class="dot" style="background: #2ca02c;"></div> Liver Domain (6 features)</div>
        <div class="legend-item"><div class="dot" style="background: #ff7f0e;"></div> Kidney Domain (6 features)</div>
        <div class="legend-item"><div class="dot" style="background: #d62728;"></div> Heart Domain (8 features)</div>
        <div class="legend-item"><div class="dot" style="background: #9467bd;"></div> Biomarker Domain (4 features)</div>
    </div>

    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(nodes)});
        var edges = new vis.DataSet({json.dumps(edges)});

        var container = document.getElementById('mynetwork');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{
                shape: 'dot',
                font: {{ size: 14, color: '#ffffff', face: 'Segoe UI' }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                width: 2,
                font: {{ size: 11, align: 'top', color: '#94a3b8' }},
                smooth: {{ type: 'curvedCW', roundness: 0.2 }}
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 150,
                    springConstant: 0.04
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100
            }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully generated interactive HTML visualization at: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_interactive_html()
