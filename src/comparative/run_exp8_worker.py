import os, sys, json, time, argparse
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader as PyGDataLoader

sys.path.insert(0, os.path.abspath('.'))
from src.comparative.pipeline import (
    FINAL_COHORT_PATH, preprocess_fold_graphs
)
from src.comparative.models.hsgin import HSGIN
from src.comparative.split import generate_or_load_folds
from src.comparative.metrics import compute_regression_metrics

GRAPH_PATH = r"graphs/patient_graphs.pt"
BASE_SEED = 42

def set_seed(s):
    np.random.seed(s)
    torch.manual_seed(s)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(s)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--out", type=str, required=True)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Worker {args.start}-{args.end}] Running on {device}...", flush=True)

    original_graphs = torch.load(GRAPH_PATH, weights_only=False)
    folds_info = generate_or_load_folds()

    y_true_orig = np.array([g["patient"].y.item() for g in original_graphs])
    uid_to_idx = {g.patient_uid: i for i, g in enumerate(original_graphs)}

    node_types = original_graphs[0].node_types
    in_dim_dict = {nt: original_graphs[0][nt].x.shape[1] for nt in node_types}

    t0 = time.time()
    fold_data = []
    for fd in folds_info["folds"]:
        f_num = fd["fold"]
        tr_gs, va_gs = preprocess_fold_graphs(
            original_graphs, fd["train_patient_uids"], fd["val_patient_uids"]
        )
        tr_loader = PyGDataLoader(tr_gs, batch_size=256, shuffle=False)
        va_loader = PyGDataLoader(va_gs, batch_size=256, shuffle=False)

        tr_batches = []
        for b in tr_loader:
            b = b.to(device)
            b.patient_indices = torch.tensor([uid_to_idx[uid] for uid in b.patient_uid], dtype=torch.long, device=device)
            tr_batches.append(b)

        va_batches = []
        for b in va_loader:
            b = b.to(device)
            b.patient_indices = torch.tensor([uid_to_idx[uid] for uid in b.patient_uid], dtype=torch.long, device=device)
            va_batches.append(b)

        fold_data.append({
            "fold": f_num,
            "tr_batches": tr_batches,
            "va_batches": va_batches
        })

    print(f"[Worker {args.start}-{args.end}] Staged batches on CUDA in {time.time()-t0:.1f}s", flush=True)

    results = {}
    for m in range(args.start, args.end + 1):
        t_perm = time.time()
        rng = np.random.default_rng(2000 + m)
        y_perm = rng.permutation(y_true_orig)
        y_perm_t = torch.tensor(y_perm, dtype=torch.float32, device=device)

        oof_preds, oof_true = [], []
        for fd in fold_data:
            f_num = fd["fold"]
            tr_batches = fd["tr_batches"]
            va_batches = fd["va_batches"]

            for b in tr_batches:
                b["patient"].y = y_perm_t[b.patient_indices]
            for b in va_batches:
                b["patient"].y = y_perm_t[b.patient_indices]

            set_seed(BASE_SEED + f_num - 1)
            model = HSGIN(in_dim_dict=in_dim_dict, hidden_dim=64, num_layers=2, dropout=0.1).to(device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
            criterion = nn.SmoothL1Loss()

            for epoch in range(5):
                model.train()
                for batch in tr_batches:
                    optimizer.zero_grad()
                    loss = criterion(model(batch), batch["patient"].y)
                    loss.backward()
                    optimizer.step()

            model.eval()
            preds_list, tgts_list = [], []
            with torch.no_grad():
                for batch in va_batches:
                    preds_list.extend(model(batch).cpu().numpy().flatten())
                    tgts_list.extend(batch["patient"].y.cpu().numpy().flatten())

            oof_preds.extend(preds_list)
            oof_true.extend(tgts_list)

        m_pooled = compute_regression_metrics(oof_true, oof_preds)
        r2_val = round(float(m_pooled["r2"]), 5)
        results[m] = r2_val
        print(f"[Worker {args.start}-{args.end}] Perm {m:3d} -> Null R2 = {r2_val:+.4f} [{time.time()-t_perm:.1f}s]", flush=True)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[Worker {args.start}-{args.end}] Finished and saved to {args.out}", flush=True)

if __name__ == "__main__":
    main()
