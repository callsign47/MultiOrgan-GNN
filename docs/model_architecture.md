# ORGANIX: Model Architecture Specification

## 1. HSGIN: Heterogeneous Systemic Graph Interaction Network

The **HSGIN** model is specifically designed for multi-organ clinical cross-talk reasoning.

### Architecture Overview

1. **Node Feature Encoders**:
   Each node type $t \in \{\text{patient}, \text{liver}, \text{kidney}, \text{heart}, \text{biomarker}\}$ has a dedicated projection block:
   $$h_t^{(0)} = \text{Dropout}(\text{ReLU}(\text{LayerNorm}(\mathbf{W}_t x_t)))$$
   where $h_t^{(0)} \in \mathbb{R}^{H}$, $H = 64$.

2. **Heterogeneous Message Passing (HeteroOrganConvBlock)**:
   Message passing is executed across the 14 directed relations using multi-head Graph Attention Networks (`GATConv`):
   $$h_i^{(l+1)} = \text{ReLU}\left(h_i^{(l)} + \sum_{r \in \mathcal{R}} \sum_{j \in \mathcal{N}_r(i)} \alpha_{ij}^{(r)} \mathbf{W}_r h_j^{(l)}\right)$$
   - Number of message passing layers: 2
   - Attention heads: 2 heads $\times$ 32 channels = 64 hidden dimensions
   - Residual skip connections are applied after each HeteroConv block.

3. **Organ-Aware Readout Layer**:
   Unlike standard GNNs that perform flat global mean pooling across all nodes or read only from the root patient node, HSGIN explicitly preserves modular organ representations:
   $$h_{\text{organ\_pool}} = \frac{1}{|\mathcal{O}|} \sum_{o \in \{\text{liver}, \text{kidney}, \text{heart}\}} h_o^{(L)}$$
   The final composite patient representation is formed by concatenation:
   $$h_{\text{repr}} = [h_{\text{patient}}^{(L)} \,\|\, h_{\text{organ\_pool}} \,\|\, h_{\text{biomarker}}^{(L)}] \in \mathbb{R}^{3H}$$

4. **Multi-Organ Prediction MLP Head**:
   A 3-layer MLP maps the concatenated representation $h_{\text{repr}} \in \mathbb{R}^{192}$ to the continuous scalar FIB-4 score:
   $$\hat{y} = \mathbf{W}_3 \cdot \text{ReLU}\left(\mathbf{W}_2 \cdot \text{ReLU}\left(\text{LayerNorm}(\mathbf{W}_1 h_{\text{repr}})\right)\right)$$

---

## 2. Competitive Baseline Architectures

ORGANIX implements and benchmarks 15 comparative architectures across 6 distinct model families:

| Model Family | Architectures Implemented |
| :--- | :--- |
| **Regularized Linear** | Ridge Regression, ElasticNet |
| **Conventional Tree Ensembles** | Random Forest Regressor, Extra Trees Regressor |
| **Modern Gradient Boosted Trees** | XGBoost (tuned), LightGBM, CatBoost, HistGradientBoosting |
| **Deep Tabular Neural Networks** | Deep MLP (PyTorch), FT-Transformer (Feature Tokenizer + Transformer), TabNet |
| **Graph Neural Networks** | Classical HGNN (HeteroSAGE), HSGIN (Proposed GAT + Organ Readout) |
| **Ensembles & Stacking** | Simple Average, Non-Negative Least Squares (NNW) Blend, Ridge Stacking |
