% run_pid_baseline.m
% Simulates a classical decoupled 4-loop PID controller on the greenhouse.
clear; clc; close all;

%% 1. Load Weather & Setup Time
weather_ts = generate_weather(); 
t_sim = 86400;      % 24 hours
dt = 60;            % 1-minute sampling
steps = t_sim / dt; 

x_history_pid = zeros(steps+1, 8);
u_history_pid = zeros(steps, 4);
t_history = (0:steps)*dt;

% Initial conditions: [T_air, W, C_CO2, T_leaf, z1, z2, z3, z4]
x0 = [15, 0.01, 400, 15, 0, 0.1, 0, 0];
x_current = x0';
x_history_pid(1, :) = x0;

% Target Setpoints: [T_air, W, CO2, T_leaf]
T_ref = 22;       % 22 °C
CO2_ref = 800;    % 800 ppm
W_ref = 0.008;    % ~50% RH

%% 2. PID Gains (Tuned with Ziegler-Nichols rules)
% Loop 1: Heater PID (Acts on negative temperature error: T_ref - T_air)
Kp_heat = 4000; Ki_heat = 8; Kd_heat = 500;
int_err_heat = 0; prev_err_heat = 0;

% Loop 2: Vent PID (Acts on positive temperature error: T_air - T_ref)
Kp_vent = 0.15; Ki_vent = 0.0005; Kd_vent = 0.05;
int_err_vent = 0; prev_err_vent = 0;

% Loop 3: Fogger PID (Acts on humidity deficit)
Kp_fog = 0.001; Ki_fog = 0.00001; Kd_fog = 0.0001;
int_err_fog = 0; prev_err_fog = 0;

% Loop 4: CO2 PID
Kp_co2 = 0.0002; Ki_co2 = 0.000001; Kd_co2 = 0.00005;
int_err_co2 = 0; prev_err_co2 = 0;

weather_time = weather_ts.Time;
weather_data = weather_ts.Data;

disp('Running Decoupled PID Simulation...');

%% 3. Simulation Loop
for k = 1:steps
    t_curr = (k-1)*dt;
    
    % Current weather disturbance
    d_curr = [interp1(weather_time, weather_data(:,1), t_curr); ...
              interp1(weather_time, weather_data(:,2), t_curr); ...
              interp1(weather_time, weather_data(:,3), t_curr); ...
              interp1(weather_time, weather_data(:,4), t_curr)];
          
    T_air = x_current(1);
    W     = x_current(2);
    C_co2 = x_current(3);
    
    % --- Loop 1: Heater PID ---
    e_heat = T_ref - T_air;
    int_err_heat = max(0, min(int_err_heat + e_heat * dt, 50000/Ki_heat)); % Anti-windup
    d_err_heat = (e_heat - prev_err_heat) / dt;
    u_heat = Kp_heat * e_heat + Ki_heat * int_err_heat + Kd_heat * d_err_heat;
    u_heat = max(0, min(50000, u_heat)); % Saturate [0, 50 kW]
    prev_err_heat = e_heat;
    
    % --- Loop 2: Vent PID ---
    e_vent = T_air - T_ref;
    int_err_vent = max(0, min(int_err_vent + e_vent * dt, 1/Ki_vent));
    d_err_vent = (e_vent - prev_err_vent) / dt;
    u_vent = 0.1 + (Kp_vent * e_vent + Ki_vent * int_err_vent + Kd_vent * d_err_vent);
    u_vent = max(0.1, min(1.0, u_vent)); % Saturate [0.1, 1.0]
    prev_err_vent = e_vent;
    
    % --- Loop 3: Fogger PID ---
    e_fog = W_ref - W;
    int_err_fog = max(0, min(int_err_fog + e_fog * dt, 0.015/Ki_fog));
    d_err_fog = (e_fog - prev_err_fog) / dt;
    u_fog = Kp_fog * e_fog + Ki_fog * int_err_fog + Kd_fog * d_err_fog;
    u_fog = max(0, min(0.015, u_fog)); % Saturate [0, 15 g/s]
    prev_err_fog = e_fog;
    
    % --- Loop 4: CO2 PID ---
    e_co2 = CO2_ref - C_co2;
    int_err_co2 = max(0, min(int_err_co2 + e_co2 * dt, 0.05/Ki_co2));
    d_err_co2 = (e_co2 - prev_err_co2) / dt;
    u_co2 = Kp_co2 * e_co2 + Ki_co2 * int_err_co2 + Kd_co2 * d_err_co2;
    u_co2 = max(0, min(0.05, u_co2)); % Saturate [0, 50 g/s]
    prev_err_co2 = e_co2;
    
    % Combine controls & disturbances
    u_ctrl = [u_heat; u_vent; u_fog; u_co2];
    u_history_pid(k, :) = u_ctrl';
    u_combined = [u_ctrl; d_curr];
    
    % Integrate physics for 1 minute
    tspan = [t_curr, t_curr + dt];
    [~, x_next] = ode15s(@(t, x) greenhouse_ode(x, u_combined), tspan, x_current);
    
    x_current = x_next(end, :)';
    x_history_pid(k+1, :) = x_current';
end

disp('PID Simulation Complete!');

%% 4. Plot PID Results
figure('Name', 'Decoupled PID Baseline Simulation', 'Position', [150, 150, 1100, 700]);

% Subplot 1: Temperature
subplot(2,2,1);
plot(t_history/3600, x_history_pid(:, 1), 'r', 'LineWidth', 2);
hold on;
plot(t_history/3600, T_ref*ones(size(t_history)), 'k--', 'LineWidth', 1.5);
title('PID: Air Temperature Control'); xlabel('Time (Hours)'); ylabel('Temp (°C)');
legend('Actual Temp', 'Target (22°C)'); grid on;

% Subplot 2: CO2
subplot(2,2,2);
plot(t_history/3600, x_history_pid(:, 3), 'b', 'LineWidth', 2);
hold on;
plot(t_history/3600, CO2_ref*ones(size(t_history)), 'k--', 'LineWidth', 1.5);
title('PID: CO_2 Concentration'); xlabel('Time (Hours)'); ylabel('CO_2 (ppm)');
legend('Actual CO_2', 'Target (800 ppm)'); grid on;

% Subplot 3: Actuators
subplot(2,2,3);
yyaxis left
plot(t_history(1:end-1)/3600, u_history_pid(:, 1)/1000, 'Color', [0.85 0.33 0.1], 'LineWidth', 1.5);
hold on;
plot(t_history(1:end-1)/3600, u_history_pid(:, 3)*1000, 'Color', [0.47 0.67 0.19], 'LineWidth', 1.5);
ylabel('Heater (kW) & Fogger (g/s)');
yyaxis right
plot(t_history(1:end-1)/3600, u_history_pid(:, 2)*100, 'Color', [0 0.44 0.74], 'LineWidth', 1.5);
ylabel('Vents Open (%)');
title('PID: Actuator Actions'); xlabel('Time (Hours)');
legend('Heater (kW)', 'Fogger (g/s)', 'Vents (%)'); grid on;

% Subplot 4: Relative Humidity
T_air_h = x_history_pid(:, 1);
W_h = x_history_pid(:, 2);
e_s_h = 0.6108 * exp(17.27 * T_air_h ./ (T_air_h + 237.3));
e_a_h = 101.325 * W_h ./ (0.622 + W_h);
RH_h = (e_a_h ./ e_s_h) * 100;

subplot(2,2,4);
plot(t_history/3600, RH_h, 'm', 'LineWidth', 2);
title('PID: Relative Humidity'); xlabel('Time (Hours)'); ylabel('RH (%)');
ylim([0 100]); grid on;

% Save baseline data for comparison
save('pid_baseline_results.mat', 't_history', 'x_history_pid', 'u_history_pid');
disp('Saved baseline data to pid_baseline_results.mat');