% pinn_predict.m
% Evaluates the forward pass of our trained PINN in native MATLAB matrix math.
function [T_leaf_hat, E_T_hat] = pinn_predict(meas, model)
    % meas: [T_air, W, C_CO2, I_solar, T_out, W_out] (1x6 row vector)
    
    % 1. Standardize inputs
    x_norm = (meas - model.scaler_X_mean) ./ model.scaler_X_scale;
    
    % 2. 3-Layer Dense Network with Tanh activations
    h1 = tanh(x_norm * model.W1 + model.b1);
    h2 = tanh(h1 * model.W2 + model.b2);
    h3 = tanh(h2 * model.W3 + model.b3);
    
    % 3. Linear Output Layer
    y_norm = h3 * model.W4 + model.b4;
    
    % 4. Inverse transform to physical units
    y_raw = y_norm .* model.scaler_Y_scale + model.scaler_Y_mean;
    
    T_leaf_hat = y_raw(1);
    E_T_hat    = y_raw(2);
end