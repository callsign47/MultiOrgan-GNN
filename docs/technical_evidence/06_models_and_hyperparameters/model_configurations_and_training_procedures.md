# Complete Model Configurations, Hyperparameters, Random Seeds, and Training Procedures

**Specification Sources**:
- Deep Tabular Configs: [`configs/comparative/exp3_deep_tabular/deep_tabular_configs.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp3_deep_tabular/deep_tabular_configs.json)
- GNN Configs: [`configs/comparative/exp4_gnn/gnn_configs.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp4_gnn/gnn_configs.json)
- Ensemble Configs: [`configs/comparative/exp5_ensemble/base_model_selection.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp5_ensemble/base_model_selection.json)
- Ablation Configs: [`configs/comparative/exp6_ablations/exp6_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp6_ablations/exp6_config.json), [`exp7_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp6_ablations/exp7_config.json)
- Controls Configs: [`configs/comparative/exp8_controls/exp8_config.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/configs/comparative/exp8_controls/exp8_config.json)  
**Status**: `VERIFIED-ON-DISK` (All Configurations Frozen Prior to Validation Evaluation)  

---

## 1. Overview of Evaluated Model Families

The comparative framework evaluates 16 distinct model architectures spanning 6 model families across identical 5-fold patient partitions:

```
[Evaluated Model Architectures (16 Models)]
  ├── Family A: Linear Regularized (Ridge, ElasticNet)
  ├── Family B: Conventional Trees (Random Forest, Extra Trees)
  ├── Family C: Advanced Gradient Boosting (XGBoost Tuned, CatBoost, LightGBM, HistGradientBoosting)
  ├── Family D: Deep Tabular Architectures (Retuned MLP, FT-Transformer, TabNet)
  ├── Family E: Graph Neural Networks (Classical HGNN, HSGIN)
  └── Family F: Ensembles (Simple Average, NNW Weighted Blend, Ridge Stacking)
```

---

## 2. Detailed Hyperparameter & Implementation Specifications

### Family A: Linear Regularized Models

#### 1. Ridge Regression (Tuned)
- **Source Script**: [`src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp1_linear_trees.py#L35-L60)
- **Implementation**: `sklearn.linear_model.RidgeCV`
- **Search Space**: $\alpha \in \{0.01, 0.1, 1.0, 10.0, 50.0, 100.0, 500.0, 1000.0\}$
- **Tuning Strategy**: 3-fold inner cross-validation strictly within each training fold.
- **Preprocessing**: Median imputation + StandardScaler (Z-score).
- **Tuned Best $\alpha$ per Fold**:
  - Fold 1: $\alpha = 100.0$
  - Fold 2: $\alpha = 100.0$
  - Fold 3: $\alpha = 100.0$
  - Fold 4: $\alpha = 50.0$
  - Fold 5: $\alpha = 100.0$
- **Performance**: Pooled $R^2 = 0.3864$, Fold Mean $R^2 = 0.3871 \pm 0.0221$, $\text{RMSE} = 0.6069$, $\text{MAE} = 0.4061$.

#### 2. ElasticNet Regression (Tuned)
- **Source Script**: [`src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp1_linear_trees.py#L62-L95)
- **Implementation**: `sklearn.linear_model.ElasticNetCV`
- **Search Space**: $\text{l1\_ratio} \in \{0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0\}$, 50 $\alpha$ values on log-scale.
- **Tuning Strategy**: 3-fold inner cross-validation, `max_iter=3000`, `random_state=42`.
- **Preprocessing**: Median imputation + StandardScaler.
- **Performance**: Pooled $R^2 = 0.3864$, Fold Mean $R^2 = 0.3870 \pm 0.0221$, $\text{RMSE} = 0.6070$, $\text{MAE} = 0.4060$.

---

### Family B: Conventional Tree Ensembles

#### 3. Random Forest Regressor
- **Source Script**: [`src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp1_linear_trees.py#L97-L130)
- **Implementation**: `sklearn.ensemble.RandomForestRegressor`
- **Hyperparameters**: `n_estimators=300`, `max_depth=12`, `min_samples_split=5`, `min_samples_leaf=2`, `max_features='sqrt'`, `random_state=42`, `n_jobs=-1`.
- **Preprocessing**: Median imputation (unstandardized).
- **Performance**: Pooled $R^2 = 0.4288$, Fold Mean $R^2 = 0.4285 \pm 0.0271$, $\text{RMSE} = 0.5856$, $\text{MAE} = 0.3822$.

#### 4. Extra Trees Regressor
- **Source Script**: [`src/comparative/exp1_linear_trees.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp1_linear_trees.py#L132-L165)
- **Implementation**: `sklearn.ensemble.ExtraTreesRegressor`
- **Hyperparameters**: `n_estimators=300`, `max_depth=12`, `min_samples_split=5`, `min_samples_leaf=2`, `max_features='sqrt'`, `random_state=42`, `n_jobs=-1`.
- **Preprocessing**: Median imputation (unstandardized).
- **Performance**: Pooled $R^2 = 0.4440$, Fold Mean $R^2 = 0.4438 \pm 0.0264$, $\text{RMSE} = 0.5777$, $\text{MAE} = 0.3766$.

---

### Family C: Advanced Gradient Boosting

#### 5. Tuned XGBoost
- **Source Script**: [`src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp2_boosting.py#L40-L80)
- **Implementation**: `xgboost.XGBRegressor`
- **Hyperparameters**: `n_estimators=2000`, `max_depth=5`, `learning_rate=0.03`, `subsample=0.8`, `colsample_bytree=0.8`, `min_child_weight=3`, `reg_alpha=0.1`, `reg_lambda=1.0`, `tree_method='hist'`, `random_state=42`, `n_jobs=-1`.
- **Early Stopping**: 50 rounds evaluated on an inner 20% validation split from training fold data (zero outer held-out exposure).
- **Optimal Iterations per Fold**: Fold 1: 384, Fold 2: 494, Fold 3: 316, Fold 4: 271, Fold 5: 303 (Mean: 353.6 iterations, rounded to 360 for Exp 6 ablations).
- **Performance**: Pooled $R^2 = 0.4698$, Fold Mean $R^2 = 0.4701 \pm 0.0340$, $\text{RMSE} = 0.5642$, $\text{MAE} = 0.3699$.

#### 6. CatBoost
- **Source Script**: [`src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp2_boosting.py#L82-L115)
- **Implementation**: `catboost.CatBoostRegressor`
- **Hyperparameters**: `iterations=2000`, `depth=6`, `learning_rate=0.03`, `l2_leaf_reg=3.0`, `early_stopping_rounds=50`, `random_seed=42`, `verbose=False`.
- **Early Stopping**: 50 rounds on inner 20% split.
- **Performance**: Pooled $R^2 = 0.4685$, Fold Mean $R^2 = 0.4692 \pm 0.0345$, $\text{RMSE} = 0.5649$, $\text{MAE} = 0.3693$.

#### 7. LightGBM
- **Source Script**: [`src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp2_boosting.py#L117-L150)
- **Implementation**: `lightgbm.LGBMRegressor`
- **Hyperparameters**: `n_estimators=2000`, `num_leaves=31`, `learning_rate=0.03`, `subsample=0.8`, `colsample_bytree=0.8`, `min_child_samples=20`, `reg_alpha=0.1`, `reg_lambda=1.0`, `early_stopping_rounds=50`, `random_state=42`, `n_jobs=-1`, `verbose=-1`.
- **Performance**: Pooled $R^2 = 0.4516$, Fold Mean $R^2 = 0.4518 \pm 0.0315$, $\text{RMSE} = 0.5738$, $\text{MAE} = 0.3757$.

#### 8. HistGradientBoosting
- **Source Script**: [`src/comparative/exp2_boosting.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp2_boosting.py#L152-L185)
- **Implementation**: `sklearn.ensemble.HistGradientBoostingRegressor`
- **Hyperparameters**: `max_iter=500`, `max_leaf_nodes=31`, `learning_rate=0.03`, `l2_regularization=1.0`, `early_stopping=True`, `validation_fraction=0.2`, `n_iter_no_change=20`, `random_state=42`.
- **Performance**: Pooled $R^2 = 0.4384$, Fold Mean $R^2 = 0.4379 \pm 0.0270$, $\text{RMSE} = 0.5807$, $\text{MAE} = 0.3783$.

---

### Family D: Deep Tabular Architectures

#### 9. Re-Tuned MLP Regressor
- **Architecture**: `[25 -> 128 -> 64 -> 32 -> 1]` with LayerNorm, ReLU, and Dropout(0.2).
- **Source Script**: [`src/comparative/deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/deep_tabular.py#L10-L45)
- **Loss Function**: `nn.SmoothL1Loss(beta=1.0)` (Huber loss).
- **Optimizer**: `AdamW(lr=0.001, weight_decay=0.0001)`.
- **Training Schedule**: `max_epochs=100`, `batch_size=64`, early stopping patience = 15 on inner 20% validation split.
- **Seeds Evaluated**: 42, 43, 44.
- **Performance**:
  - Seed 42: Pooled $R^2 = 0.4495$, Fold Mean $R^2 = 0.4522 \pm 0.0391$
  - Seed 43: Pooled $R^2 = 0.4468$, Fold Mean $R^2 = 0.4498 \pm 0.0336$
  - Seed 44: Pooled $R^2 = 0.4514$, Fold Mean $R^2 = 0.4578 \pm 0.0281$
  - **3-Seed Ensemble**: Pooled $R^2 = \mathbf{0.4582}$, $\text{RMSE} = 0.5703$, $\text{MAE} = 0.3523$.
- *Tuning Resolution Note*: Re-tuning with LayerNorm and Huber loss raised MLP performance from the historical baseline failure of $R^2 = 0.1320$ to $R^2 = 0.4582$, confirming that the earlier result was an artifact of under-regularization.

#### 10. FT-Transformer (Feature Tokenizer + Transformer)
- **Architecture**: FeatureTokenizer ($25 \times d_{\text{embed}}=32$) + 2 Transformer Encoder layers (`embed_dim=32`, `num_heads=4`, `ffn_dim=64`, `dropout=0.1`) + `[CLS]` token readout + Linear head $\mathbb{R}^{32} \to \mathbb{R}^1$.
- **Source Script**: [`src/comparative/deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/deep_tabular.py#L50-L135)
- **Training Schedule**: AdamW (`lr=0.001`, `weight_decay=0.0001`), SmoothL1Loss, `batch_size=64`, `max_epochs=100`, early stopping patience = 15.
- **Seeds Evaluated**: 42, 43, 44.
- **Performance**:
  - Seed 42: Pooled $R^2 = 0.4581$, Fold Mean $R^2 = 0.4589 \pm 0.0312$
  - Seed 43: Pooled $R^2 = 0.4612$, Fold Mean $R^2 = 0.4604 \pm 0.0274$
  - Seed 44: Pooled $R^2 = 0.4598$, Fold Mean $R^2 = 0.4602 \pm 0.0281$
  - **3-Seed Ensemble**: Pooled $R^2 = \mathbf{0.4674}$, $\text{RMSE} = 0.5655$, $\text{MAE} = 0.3511$.

#### 11. TabNet
- **Source Script**: [`src/comparative/exp3_deep_tabular.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp3_deep_tabular.py#L180-L240)
- **Implementation**: `pytorch_tabnet.tab_model.TabNetRegressor`
- **Hyperparameters**: `n_d=16`, `n_a=16`, `n_steps=3`, `gamma=1.3`, `lambda_sparse=0.0001`, `optimizer_fn=torch.optim.Adam`, `optimizer_params={'lr': 0.02}`, `max_epochs=100`, `patience=15`.
- **Seeds Evaluated**: 42, 43, 44.
- **Performance**:
  - Seed 42: Pooled $R^2 = 0.4431$
  - Seed 43: Pooled $R^2 = 0.4402$
  - Seed 44: Pooled $R^2 = 0.4419$
  - **3-Seed Ensemble**: Pooled $R^2 = \mathbf{0.4501}$, $\text{RMSE} = 0.5745$, $\text{MAE} = 0.3564$.

---

### Family E: Graph Neural Networks

#### 12. Classical HGNN (Flat SAGEConv Heterogeneous GNN)
- **Source Script**: [`src/models/baselines.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/models/baselines.py#L42-L84)
- **Convolution**: `pyg_nn.HeteroConv` wrapping `SAGEConv(hidden_dim=64, hidden_dim=64)` across all 14 directed edge types.
- **Readout**: Flat patient-node readout (`h_patient -> Linear(64, 32) -> ReLU -> Linear(32, 1)`).
- **Training**: AdamW (`lr=0.001`, `weight_decay=0.0001`), Huber loss, `epochs=40`, `batch_size=64`.
- **Seeds Evaluated**: 42, 43, 44.
- **Performance**:
  - Seed 42: Pooled $R^2 = 0.4680$, Fold Mean $R^2 = 0.4681 \pm 0.0195$
  - Seed 43: Pooled $R^2 = 0.4704$, Fold Mean $R^2 = 0.4704 \pm 0.0173$
  - Seed 44: Pooled $R^2 = 0.4707$, Fold Mean $R^2 = 0.4703 \pm 0.0148$
  - **3-Seed Ensemble**: Pooled $R^2 = \mathbf{0.4771}$, $\text{RMSE} = 0.5603$, $\text{MAE} = 0.3591$.

#### 13. HSGIN (Heterogeneous Systemic Graph Interaction Network)
- **Source Script**: [`src/models/hsgin.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/models/hsgin.py)
- **Architecture**:
  - Per-node Linear Encoders: $\mathbb{R}^{d_\tau} \to \mathbb{R}^{64}$ + LayerNorm + ReLU + Dropout(0.1).
  - 2 $\times$ `HeteroOrganConvBlock` wrapping `GATConv(64, 32, heads=2, concat=True, add_self_loops=False)`.
  - Residual Skips: $h^{(l+1)} = \text{ReLU}(h^{(l)} + h_{\text{conv}}^{(l+1)})$.
  - Organ-Aware Hierarchical Readout: Concatenation $[h_{\text{patient}} \,\|\, h_{\text{organ\_pool}} \,\|\, h_{\text{biomarker}}] \in \mathbb{R}^{192}$.
  - MLP Prediction Head: $\mathbb{R}^{192} \to \mathbb{R}^{64} \to \mathbb{R}^{32} \to \mathbb{R}^{1}$ with LayerNorm & ReLU.
- **Loss**: SmoothL1Loss (`beta=1.0`).
- **Optimizer**: AdamW (`lr=0.001`, `weight_decay=0.0001`).
- **Training Schedule**: `epochs=50`, `batch_size=64`, fixed across all 5 folds.
- **Seeds Evaluated**: 42, 43, 44.
- **Performance**:
  - Seed 42: Pooled $R^2 = 0.4988$, Fold Mean $R^2 = 0.4976 \pm 0.0285$, $\text{RMSE} = 0.5485$, $\text{MAE} = 0.3509$.
  - Seed 43: Pooled $R^2 = 0.4927$, Fold Mean $R^2 = 0.4919 \pm 0.0198$, $\text{RMSE} = 0.5519$, $\text{MAE} = 0.3508$.
  - Seed 44: Pooled $R^2 = 0.4943$, Fold Mean $R^2 = 0.4936 \pm 0.0219$, $\text{RMSE} = 0.5510$, $\text{MAE} = 0.3559$.
  - Cross-Seed Mean: Fold Mean $R^2 = 0.4944 \pm 0.0024$.
  - **3-Seed Ensemble**: Pooled $R^2 = \mathbf{0.5114}$, $\text{RMSE} = 0.5416$, $\text{MAE} = 0.3456$, Spearman $\rho = 0.7736$.

---

### Family F: Ensembles (Experiment 5)

Base models chosen for ensembling ($M=4$ diverse architectures):
1. `HSGIN_seed42` (Graph Neural Network)
2. `XGBoost_tuned` (Gradient Boosted Trees)
3. `CatBoost` (Gradient Boosted Trees)
4. `FT_Transformer_seed42` (Deep Tabular Attention)

#### 14. Simple Average Ensemble
- **Methodology**: Uniform unweighted mean $\hat{y} = \frac{1}{4} \sum_{m=1}^4 \hat{y}_m$.
- **Performance**: Pooled $R^2 = 0.5004$, Fold Mean $R^2 = 0.5009 \pm 0.0314$, $\text{RMSE} = 0.5477$, $\text{MAE} = 0.3505$.

#### 15. Non-Negative Weighted Blend (NNW Blend)
- **Methodology**: Inner-fold optimization via Sequential Least Squares Programming (SLSQP):
  $$\min_w \sum_{i \in D_{\text{inner}}} \left(y_i - \sum_{m=1}^4 w_m \hat{y}_{i,m}\right)^2 \quad \text{s.t.} \quad w_m \ge 0, \quad \sum_{m=1}^4 w_m = 1$$
- **Fitted Global Weights**: $w_{\text{HSGIN}} = 0.482$, $w_{\text{XGBoost}} = 0.284$, $w_{\text{CatBoost}} = 0.141$, $w_{\text{FT\_Transformer}} = 0.093$.
- **Performance**: Pooled $R^2 = \mathbf{0.5101}$, Fold Mean $R^2 = 0.5100 \pm 0.0293$, $\text{RMSE} = 0.5423$, $\text{MAE} = 0.3466$, Spearman $\rho = 0.7733$.

#### 16. Ridge Stacking
- **Methodology**: Ridge regression meta-learner (`RidgeCV(alphas=np.logspace(-4, 4, 50), cv=5)`) fitted strictly on inner out-of-fold meta-features generated across 10 pair-excluded subsets $D \setminus (F_k \cup F_j)$.
- **Performance**: Pooled $R^2 = \mathbf{0.5089}$, Fold Mean $R^2 = 0.5089 \pm 0.0293$, $\text{RMSE} = 0.5430$, $\text{MAE} = 0.3518$, Spearman $\rho = 0.7722$.
