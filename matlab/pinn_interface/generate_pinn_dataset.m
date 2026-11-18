% generate_pinn_dataset.m
% Generates a multi-day training dataset for the PyTorch PINN state estimator.
clear; clc;

disp('Generating 7-day multi-condition training dataset for PINN...');

%% 1. Simulation Parameters
days = 7;
dt = 60;                        % 1-minute sampling
total_steps = (days * 86400) / dt;
t_vec = (0:total_steps-1)' * dt;

%% 2. Generate Multi-Day Weather with Variations
% Base diurnal patterns with day-to-day weather fluctuations (clouds, heatwaves)
rng(42); % For reproducible research

T_out_base = 15 + 8 * sin(2*pi*t_vec/86400 - pi/2);
I_solar_base = max(0, 850 * sin(2*pi*t_vec/86400));

% Add day-to-day stochastic cloud covers and ambient noise
cloud_factor = 0.7 + 0.3 * rand(total_steps, 1);
I_solar = I_solar_base .* cloud_factor;
T_out = T_out_base + 2 * randn(total_steps, 1);
W_out = 0.005 + 0.002 * sin(2*pi*t_vec/86400);
C_out = 400 * ones(total_steps, 1);

%% 3. Simulate System Response
% Initial state
x = [18; 0.009; 600; 18; 0; 0.1; 0; 0];

% Storage arrays
dataset = zeros(total_steps, 9);
% Columns: [t, T_air, W, C_CO2, T_leaf, I_solar, T_out, W_out, E_T]

A_leaf = 400;

for k = 1:total_steps
    t_curr = t_vec(k);
    d_curr = [T_out(k); I_solar(k); W_out(k); C_out(k)];
    
    % Semi-random realistic actuator operation during data collection
    u_heat = (T_out(k) < 18) * 15000 * rand();
    u_vent = 0.1 + 0.4 * (I_solar(k) > 200) * rand();
    u_fog  = 0.005 * (I_solar(k) > 400) * rand();
    u_co2  = 0.01 * (I_solar(k) > 100);
    u_curr = [u_heat; u_vent; u_fog; u_co2];
    
    u_combined = [u_curr; d_curr];
    
    % Step physics
    [~, x_next] = ode15s(@(t, x) greenhouse_ode(x, u_combined), [t_curr, t_curr + dt], x);
    x = x_next(end, :)';
    
    % Calculate true Penman-Monteith transpiration E_T for validation
    T_air = x(1); W = x(2);
    e_s = 0.6108 * exp(17.27 * T_air / (T_air + 237.3));
    e_a = 101.325 * W / (0.622 + W);
    VPD = max(0, e_s - e_a);
    E_T = A_leaf * (5e-8 * I_solar(k) + 1e-6 * VPD);
    
    % Store [t, T_air, W, C_CO2, T_leaf, I_solar, T_out, W_out, E_T]
    dataset(k, :) = [t_curr, x(1), x(2), x(3), x(4), I_solar(k), T_out(k), W_out(k), E_T];
    
    if mod(k, 1440) == 0
        fprintf('Generated Day %d / %d...\n', k/1440, days);
    end
end

%% 4. Export to CSV for PyTorch
header = {'time_s', 'T_air', 'W', 'C_CO2', 'T_leaf', 'I_solar', 'T_out', 'W_out', 'E_T'};
data_table = array2table(dataset, 'VariableNames', header);

writetable(data_table, 'pinn_training_data.csv');
disp('--------------------------------------------------------------');
disp('Successfully created pinn_training_data.csv with 10,080 samples!');
disp('--------------------------------------------------------------');