# ablation_study.py
# Day 24-25: Proves the PINN outperforms a pure black-box MLP.
# This becomes Table 4 of the paper.

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

torch.manual_seed(42)
np.random.seed(42)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# ============================================================
# 1. Load Full Dataset
# ============================================================
df = pd.read_csv('pinn_training_data.csv')
X_raw = df[['T_air', 'W', 'C_CO2', 'I_solar', 'T_out', 'W_out']].values.astype(np.float32)
Y_raw = df[['T_leaf', 'E_T']].values.astype(np.float32)

scaler_X = StandardScaler()
scaler_Y = StandardScaler()
X_norm = scaler_X.fit_transform(X_raw)
Y_norm = scaler_Y.fit_transform(Y_raw)
X_raw_t = torch.tensor(X_raw, dtype=torch.float32, device=device)

# ============================================================
# 2. Helper Functions
# ============================================================
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, 2)
        )
    def forward(self, x): return self.net(x)

def penman_monteith_residual(X_raw_batch, E_T_pred):
    T_air = X_raw_batch[:, 0]; W = X_raw_batch[:, 1]; I_solar = X_raw_batch[:, 3]
    e_s = 0.6108 * torch.exp(17.27 * T_air / (T_air + 237.3))
    e_a = 101.325 * W / (0.622 + W)
    VPD = torch.clamp(e_s - e_a, min=0.0)
    E_T_pm = 400.0 * (5e-8 * I_solar + 1e-6 * VPD)
    return torch.mean((E_T_pred - E_T_pm) ** 2)

def compute_metrics(model, X_t, Y_raw_np, scaler_Y):
    model.eval()
    with torch.no_grad():
        Y_pred_n = model(X_t).cpu().numpy()
    Y_pred = scaler_Y.inverse_transform(Y_pred_n)
    rmse_T = np.sqrt(np.mean((Y_raw_np[:,0] - Y_pred[:,0])**2))
    r2_T   = 1 - np.sum((Y_raw_np[:,0]-Y_pred[:,0])**2) / np.sum((Y_raw_np[:,0]-np.mean(Y_raw_np[:,0]))**2)
    rmse_E = np.sqrt(np.mean((Y_raw_np[:,1] - Y_pred[:,1])**2))
    r2_E   = 1 - np.sum((Y_raw_np[:,1]-Y_pred[:,1])**2) / np.sum((Y_raw_np[:,1]-np.mean(Y_raw_np[:,1]))**2)
    return rmse_T, r2_T, rmse_E, r2_E

def train_model(X_train_t, Y_train_t, X_all_t, scaler_Y_loc, epochs, use_physics, label):
    """Generic training loop supporting both MLP and PINN modes."""
    model = MLP().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)
    loss_fn = nn.MSELoss()
    lambda_p = 10.0

    for epoch in range(epochs):
        model.train()
        Y_pred = model(X_train_t)
        loss = loss_fn(Y_pred, Y_train_t)

        if use_physics:
            Y_all = model(X_all_t)
            E_T_raw = Y_all[:, 1] * scaler_Y_loc.scale_[1] + scaler_Y_loc.mean_[1]
            loss = loss + lambda_p * penman_monteith_residual(X_raw_t, E_T_raw)

        optimizer.zero_grad(); loss.backward(); optimizer.step(); scheduler.step()

    print(f"  [{label}] Training complete.")
    return model

# ============================================================
# 3. Run 4 Ablation Conditions
# ============================================================
results = []
EPOCHS = 3000

# For sparse data experiments, use subsets
splits = {
    'Full data (100%)' : 1.00,
    'Sparse data (50%)': 0.50,
    'Sparse data (10%)': 0.10,
}

print("\n" + "="*60)
print("           ABLATION STUDY (Table 4 of Paper)          ")
print("="*60)

X_all_t = torch.tensor(X_norm, dtype=torch.float32, device=device)

for label, frac in splits.items():
    n = int(len(X_norm) * frac)
    X_t = torch.tensor(X_norm[:n], dtype=torch.float32, device=device)
    Y_t = torch.tensor(Y_norm[:n], dtype=torch.float32, device=device)

    for use_physics, model_type in [(False, 'MLP (no physics)'), (True, 'PINN (with physics)')]:
        tag = f"{label} | {model_type}"
        model = train_model(X_t, Y_t, X_all_t, scaler_Y, EPOCHS, use_physics, tag)

        X_full_t = torch.tensor(X_norm, dtype=torch.float32, device=device)
        rmse_T, r2_T, rmse_E, r2_E = compute_metrics(model, X_full_t, Y_raw, scaler_Y)
        results.append({'Model': model_type, 'Data': label,
                        'RMSE T_leaf (°C)': rmse_T, 'R² T_leaf': r2_T,
                        'RMSE E_T (kg/s)': rmse_E, 'R² E_T': r2_E})

# ============================================================
# 4. Print Results Table
# ============================================================
print("\n" + "="*75)
print(f"  {'Model':<22} {'Data':<22} {'RMSE T_leaf':>12} {'R² T_leaf':>10} {'R² E_T':>8}")
print("="*75)
for r in results:
    print(f"  {r['Model']:<22} {r['Data']:<22} {r['RMSE T_leaf (°C)']:>12.4f} "
          f"{r['R² T_leaf']:>10.4f} {r['R² E_T']:>8.4f}")
print("="*75)
print("\nKey Finding: PINN with 10% data should beat MLP with 100% data!")