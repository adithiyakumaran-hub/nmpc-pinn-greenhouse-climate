% run_pinn_nmpc_closedloop.m
% Closed-Loop NMPC driven by PINN State Estimates (Novelty N1 Closed-Loop Validation)
clear; clc; close all;

%% 1. Setup Weather, NMPC & PINN Model
weather_ts = generate_weather(); 
setup_nmpc;

disp('Loading exported PINN model weights...');
pinn_model = load('pinn_weights_for_matlab.mat');

%% 2. Simulation Setup
t_sim = 86400;      % 24 hours
dt = 60;            % 1-minute steps
steps = t_sim / dt; 

x_history_pinn = zeros(steps+1, 8);
u_history_pinn = zeros(steps, 4);
T_leaf_hat_history = zeros(steps, 1);
t_history = (0:steps)*dt;

x0 = [15, 0.01, 400, 15, 0, 0.1, 0, 0];
u0 = [10000, 0.1, 0, 0];
d0 = [10, 0, 0.005, 400];

x_current = x0';
x_history_pinn(1, :) = x0;

y_ref = [22, 0.008, 800, 22];

weather_time = weather_ts.Time;
weather_data = weather_ts.Data;

disp('Running Closed-Loop PINN-NMPC Simulation...');
nlmpc_options = nlmpcmoveopt;

%% 3. Closed-Loop Simulation
for k = 1:steps
    t_curr = (k-1)*dt;
    
    % Interpolate current ambient weather
    d_curr = [interp1(weather_time, weather_data(:,1), t_curr); ...
              interp1(weather_time, weather_data(:,2), t_curr); ...
              interp1(weather_time, weather_data(:,3), t_curr); ...
              interp1(weather_time, weather_data(:,4), t_curr)];
          
    if k == 1
        last_u = u0;
    else
        last_u = u_history_pinn(k-1, :);
    end
    
    % --- PINN STATE ESTIMATION STEP ---
    % Read cheap measurements: [T_air, W, C_CO2, I_solar, T_out, W_out]
    meas = [x_current(1), x_current(2), x_current(3), d_curr(2), d_curr(1), d_curr(3)];
    [T_leaf_hat, ~] = pinn_predict(meas, pinn_model);
    T_leaf_hat_history(k) = T_leaf_hat;
    
    % Assemble estimated state vector for NMPC:
    % Notice: x(4) (true leaf temp) is REPLACED by the PINN estimate!
    x_estimated = x_current;
    x_estimated(4) = T_leaf_hat;
    
    % --- NMPC OPTIMIZATION ---
    [u_optimal, nlmpc_options] = nlmpcmove(nlobj, x_estimated, last_u, y_ref, d_curr', nlmpc_options);
    u_history_pinn(k, :) = u_optimal';
    
    % --- PHYSICAL PLANT INTEGRATION ---
    u_combined = [u_optimal; d_curr];
    tspan = [t_curr, t_curr + dt];
    [~, x_next] = ode15s(@(t, x) greenhouse_ode(x, u_combined), tspan, x_current);
    
    x_current = x_next(end, :)';
    x_history_pinn(k+1, :) = x_current';
    
    if mod(k, 120) == 0
        fprintf('Simulated %d / 24 hours...\n', k/60);
    end
end
disp('Simulation complete!');

% Save results
save('pinn_nmpc_results.mat', 't_history', 'x_history_pinn', 'u_history_pinn', 'T_leaf_hat_history');

%% 4. Plot Comparison: True vs PINN-Estimated Leaf Temperature
figure('Name', 'PINN-in-the-Loop Validation', 'Position', [100, 100, 1100, 600]);

subplot(2,2,1);
plot(t_history/3600, x_history_pinn(:, 1), 'b', 'LineWidth', 2);
hold on;
plot(t_history/3600, y_ref(1)*ones(size(t_history)), 'r--', 'LineWidth', 1.5);
title('Air Temperature Tracking (PINN-NMPC)');
xlabel('Time (Hours)'); ylabel('Temp (°C)');
legend('Actual Temp', 'Target (22°C)'); grid on;

subplot(2,2,2);
% Compare True Leaf Temp vs PINN Estimated Leaf Temp
plot(t_history(1:end-1)/3600, x_history_pinn(1:end-1, 4), 'k-', 'LineWidth', 2);
hold on;
plot(t_history(1:end-1)/3600, T_leaf_hat_history, 'r--', 'LineWidth', 1.5);
title('Leaf Temperature: True vs PINN Estimate');
xlabel('Time (Hours)'); ylabel('T_{leaf} (°C)');
legend('True Plant State', 'PINN Observer \hat{T}_{leaf}'); grid on;

subplot(2,2,3);
yyaxis left
plot(t_history(1:end-1)/3600, u_history_pinn(:, 1)/1000, 'Color', [0.85 0.33 0.1], 'LineWidth', 1.5);
hold on;
plot(t_history(1:end-1)/3600, u_history_pinn(:, 3)*1000, 'Color', [0.47 0.67 0.19], 'LineWidth', 1.5);
ylabel('Heater (kW) & Fogger (g/s)');
yyaxis right
plot(t_history(1:end-1)/3600, u_history_pinn(:, 2)*100, 'Color', [0 0.44 0.74], 'LineWidth', 1.5);
ylabel('Vents Open (%)');
title('Actuator Commands'); xlabel('Time (Hours)');
legend('Heater (kW)', 'Fogger (g/s)', 'Vents (%)'); grid on;

subplot(2,2,4);
% Estimation error over time
estimation_error = abs(x_history_pinn(1:end-1, 4) - T_leaf_hat_history);
plot(t_history(1:end-1)/3600, estimation_error, 'm', 'LineWidth', 1.5);
title('PINN Estimation Error (|T_{leaf} - \hat{T}_{leaf}|)');
xlabel('Time (Hours)'); ylabel('Error (°C)');
grid on;

fprintf('\nMean Absolute Observer Error on T_leaf: %.4f °C\n', mean(estimation_error));