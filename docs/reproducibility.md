# ORGANIX: Reproducibility & Scientific Limitations

## 1. Determinism and Seeding

All random processes across ORGANIX are deterministically seeded using `organix.utils.seeding.seed_everything(seed)`:
- Python standard library `random`
- Environment variable `PYTHONHASHSEED`
- NumPy pseudo-random generator
- PyTorch CPU and CUDA random number generators
- PyTorch CUDNN deterministic algorithms enabled (`benchmark = False`)

---

## 2. Checkpoint & Model Weight Status

In accordance with strict research integrity standards:
- **Trained Model Checkpoint Weights**: Model checkpoint binaries (`.pt`, `.pth`, `.safetensors`) were not stored during benchmark out-of-fold predictions generation due to repository storage constraints (~15 architectures $\times$ 5 folds $\times$ 3 seeds).
- **Out-of-Fold (OOF) Predictions**: Every individual patient prediction ($\hat{y}_i, i=1,\dots,6277$) is preserved in audited CSV format under `artifacts/results/experiments/`.
- **Deterministic Re-training**: Full model weights can be regenerated identically using the locked random seeds and configuration specifications recorded in `configs/experiments/`.

---

## 3. Methodological Limitations

1. **Cross-Sectional Survey Scope**: NHANES provides cross-sectional clinical observations; prospective longitudinal fibrosis transition data are not captured.
2. **Surrogate Target**: Continuous FIB-4 is a clinical biomarker surrogate for liver fibrosis, not a histological liver biopsy stage ($F0\text{--}F4$).
3. **Graph Regularization Effect**: Ablation studies (Exp 7) reveal that Random Edge DIGRAPH models achieve equivalent performance to biologically-motivated topology ($R^2 = 0.5095$ vs $0.5114$, $p=0.814$). This demonstrates that heterogeneous graph message passing functions primarily as a localized architectural regularizer rather than discovering novel biological cross-talk pathways.
