# export_pinn_to_matlab.py
# Exports the trained PyTorch PINN model weights and scalers to MATLAB format.

import torch
import numpy as np
import scipy.io as sio

print("Loading trained PINN model checkpoint...")
checkpoint = torch.load('pinn_greenhouse.pth', map_location='cpu')
state_dict = checkpoint['model_state_dict']

# Extract weights and biases
W1 = state_dict['net.0.weight'].numpy().T  # (6, 64)
b1 = state_dict['net.0.bias'].numpy()      # (64,)
W2 = state_dict['net.2.weight'].numpy().T  # (64, 64)
b2 = state_dict['net.2.bias'].numpy()      # (64,)
W3 = state_dict['net.4.weight'].numpy().T  # (64, 64)
b3 = state_dict['net.4.bias'].numpy()      # (64,)
W4 = state_dict['net.6.weight'].numpy().T  # (64, 2)
b4 = state_dict['net.6.bias'].numpy()      # (2,)

mat_data = {
    'W1': W1, 'b1': b1,
    'W2': W2, 'b2': b2,
    'W3': W3, 'b3': b3,
    'W4': W4, 'b4': b4,
    'scaler_X_mean': checkpoint['scaler_X_mean'],
    'scaler_X_scale': checkpoint['scaler_X_scale'],
    'scaler_Y_mean': checkpoint['scaler_Y_mean'],
    'scaler_Y_scale': checkpoint['scaler_Y_scale']
}

output_file = 'pinn_weights_for_matlab.mat'
sio.savemat(output_file, mat_data)

print(f"Successfully exported PINN weights to {output_file}!")
print("Network architecture: 6 -> 64 -> 64 -> 64 -> 2 (Tanh activations)")