# train_pinn.py
# Phase 3, Day 21-23: Physics-Informed Neural Network (PINN) State Estimator
# Novelty N1: Penman-Monteith energy balance encoded as a physics residual loss.

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ============================================================
# 0. Reproducibility
# ============================================================
torch.manual_seed(42)
np.random.seed(42)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# ============================================================
# 1. Load Dataset from MATLAB
# ============================================================
print("Loading dataset from MATLAB...")
df = pd.read_csv('pinn_training_data.csv')
print(f"  Dataset shape: {df.shape}")

# Input features (cheap sensors — what we CAN measure)
# [T_air, W, C_CO2, I_solar, T_out, W_out]
X_raw = df[['T_air', 'W', 'C_CO2', 'I_solar', 'T_out', 'W_out']].values.astype(np.float32)

# Target outputs (what we CANNOT directly measure without expensive sensors)
Y_raw = df[['T_leaf', 'E_T']].values.astype(np.float32)

# ============================================================
# 2. Normalize Inputs & Outputs
# ============================================================
scaler_X = StandardScaler()
scaler_Y = StandardScaler()
X_norm = scaler_X.fit_transform(X_raw)
Y_norm = scaler_Y.fit_transform(Y_raw)

# Train/Validation Split (80/20)
X_train, X_val, Y_train, Y_val = train_test_split(X_norm, Y_norm, test_size=0.2, random_state=42)

X_train_t = torch.tensor(X_train, device=device)
Y_train_t = torch.tensor(Y_train, device=device)
X_val_t   = torch.tensor(X_val,   device=device)
Y_val_t   = torch.tensor(Y_val,   device=device)

# Also keep raw values for physics loss calculation
X_raw_t = torch.tensor(X_raw, dtype=torch.float32, device=device)
Y_raw_t = torch.tensor(Y_raw, dtype=torch.float32, device=device)

# ============================================================
# 3. PINN Architecture
# ============================================================
class PINN(nn.Module):
    """
    Physics-Informed Neural Network.
    Inputs:  [T_air, W, C_CO2, I_solar, T_out, W_out]  (6 cheap sensors)
    Outputs: [T_leaf_hat, E_T_hat]                      (2 unmeasured states)
    """
    def __init__(self):
        super(PINN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 64),   nn.Tanh(),
            nn.Linear(64, 64),  nn.Tanh(),
            nn.Linear(64, 64),  nn.Tanh(),
            nn.Linear(64, 2)
        )
    def forward(self, x):
        return self.net(x)

# ============================================================
# 4. Penman-Monteith Physics Residual Loss (THE CORE NOVELTY)
# ============================================================
def penman_monteith_residual(X_raw_batch, E_T_pred):
    """
    Encodes the Penman-Monteith energy balance as a loss term.
    The network is PENALIZED if its E_T_hat prediction violates the
    Penman-Monteith equation — the fundamental law of plant transpiration.

    PM equation:
        E_T = A_leaf * (5e-8 * I_solar + 1e-6 * VPD)
    where VPD = e_s(T_air) - e_a(W)
    """
    T_air   = X_raw_batch[:, 0]
    W       = X_raw_batch[:, 1]
    I_solar = X_raw_batch[:, 3]
    A_leaf  = 400.0

    # Saturation vapor pressure (Magnus formula)
    e_s = 0.6108 * torch.exp(17.27 * T_air / (T_air + 237.3))
    # Actual vapor pressure from absolute humidity
    e_a = 101.325 * W / (0.622 + W)
    # Vapor Pressure Deficit (VPD)
    VPD = torch.clamp(e_s - e_a, min=0.0)

    # Penman-Monteith theoretical transpiration rate
    E_T_pm = A_leaf * (5e-8 * I_solar + 1e-6 * VPD)

    # Physics residual: how much does the PINN's E_T deviate from the physics law?
    residual = E_T_pred - E_T_pm
    return torch.mean(residual ** 2)

# ============================================================
# 5. Training Setup
# ============================================================
model = PINN().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=5000, eta_min=1e-5)

data_loss_fn = nn.MSELoss()

# Physics loss weight: controls how strongly Penman-Monteith is enforced
lambda_physics = 10.0

epochs = 5000
history = {'train_loss': [], 'val_loss': [], 'physics_loss': []}

# ============================================================
# 6. Training Loop
# ============================================================
print("\nStarting PINN Training (5000 epochs)...")
print("-" * 55)

for epoch in range(epochs):
    model.train()

    # --- Data Loss (MSE on T_leaf and E_T) ---
    Y_pred_train = model(X_train_t)
    loss_data = data_loss_fn(Y_pred_train, Y_train_t)

    # --- Physics Loss (Penman-Monteith Residual) ---
    # Denormalize E_T prediction to get physical units back
    Y_pred_all = model(X_raw_t)
    E_T_pred_raw = (Y_pred_all[:, 1] * scaler_Y.scale_[1] + scaler_Y.mean_[1])
    loss_physics = penman_monteith_residual(X_raw_t, E_T_pred_raw)

    # --- Total Loss ---
    total_loss = loss_data + lambda_physics * loss_physics

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()
    scheduler.step()

    # Validation
    model.eval()
    with torch.no_grad():
        Y_pred_val = model(X_val_t)
        val_loss = data_loss_fn(Y_pred_val, Y_val_t)

    history['train_loss'].append(total_loss.item())
    history['val_loss'].append(val_loss.item())
    history['physics_loss'].append(loss_physics.item())

    if (epoch + 1) % 500 == 0:
        print(f"  Epoch {epoch+1:5d}/{epochs} | "
              f"Train Loss: {total_loss.item():.5f} | "
              f"Val Loss: {val_loss.item():.5f} | "
              f"PM Residual: {loss_physics.item():.6f}")

print("-" * 55)
print("Training Complete!")

# ============================================================
# 7. Final Validation Metrics
# ============================================================
model.eval()
with torch.no_grad():
    Y_pred_norm = model(torch.tensor(X_norm, dtype=torch.float32, device=device))
    Y_pred_final = scaler_Y.inverse_transform(Y_pred_norm.cpu().numpy())

T_leaf_true = Y_raw[:, 0]
T_leaf_pred = Y_pred_final[:, 0]
E_T_true    = Y_raw[:, 1]
E_T_pred    = Y_pred_final[:, 1]

rmse_Tleaf = np.sqrt(np.mean((T_leaf_true - T_leaf_pred)**2))
rmse_ET    = np.sqrt(np.mean((E_T_true - E_T_pred)**2))
r2_Tleaf   = 1 - np.sum((T_leaf_true - T_leaf_pred)**2) / np.sum((T_leaf_true - np.mean(T_leaf_true))**2)
r2_ET      = 1 - np.sum((E_T_true - E_T_pred)**2) / np.sum((E_T_true - np.mean(E_T_true))**2)

print(f"\n{'='*50}")
print("          PINN VALIDATION RESULTS (Novelty N1)       ")
print(f"{'='*50}")
print(f"  T_leaf  — RMSE: {rmse_Tleaf:.4f} °C  |  R²: {r2_Tleaf:.4f}")
print(f"  E_T     — RMSE: {rmse_ET:.6f} kg/s  |  R²: {r2_ET:.4f}")
print(f"{'='*50}")

# ============================================================
# 8. Save Model
# ============================================================
torch.save({'model_state_dict': model.state_dict(),
            'scaler_X_mean': scaler_X.mean_,
            'scaler_X_scale': scaler_X.scale_,
            'scaler_Y_mean': scaler_Y.mean_,
            'scaler_Y_scale': scaler_Y.scale_},
           'pinn_greenhouse.pth')
print("\nModel saved to pinn_greenhouse.pth")

# ============================================================
# 9. Plot Training History & Predictions (Paper Figure 7 & 8)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('PINN Training Results (Novelty N1)', fontsize=14, fontweight='bold')

# Loss curves
axes[0].semilogy(history['train_loss'], label='Total Train Loss', color='blue', alpha=0.8)
axes[0].semilogy(history['val_loss'], label='Validation Loss', color='orange', alpha=0.8)
axes[0].semilogy(history['physics_loss'], label='PM Physics Residual', color='green', ls='--')
axes[0].set_title('Training Loss Convergence'); axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss (log scale)'); axes[0].legend(); axes[0].grid(True)

# T_leaf scatter plot
axes[1].scatter(T_leaf_true[:500], T_leaf_pred[:500], alpha=0.4, s=8, color='blue')
axes[1].plot([min(T_leaf_true), max(T_leaf_true)], [min(T_leaf_true), max(T_leaf_true)], 'r--', lw=2)
axes[1].set_title(f'Leaf Temp: Predicted vs True\n(RMSE={rmse_Tleaf:.3f}°C, R²={r2_Tleaf:.4f})')
axes[1].set_xlabel('True T_leaf (°C)'); axes[1].set_ylabel('Predicted T_leaf (°C)'); axes[1].grid(True)

# E_T scatter plot
axes[2].scatter(E_T_true[:500], E_T_pred[:500], alpha=0.4, s=8, color='green')
axes[2].plot([min(E_T_true), max(E_T_true)], [min(E_T_true), max(E_T_true)], 'r--', lw=2)
axes[2].set_title(f'Transpiration: Predicted vs True\n(RMSE={rmse_ET:.5f} kg/s, R²={r2_ET:.4f})')
axes[2].set_xlabel('True E_T (kg/s)'); axes[2].set_ylabel('Predicted E_T (kg/s)'); axes[2].grid(True)

plt.tight_layout()
plt.savefig('pinn_training_results.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved figure to pinn_training_results.png")