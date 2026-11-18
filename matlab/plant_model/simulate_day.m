% simulate_day.m  — Complete 8-State Version
clear; clc; close all;

%% 1. Setup Time and Initial Conditions
tspan = [0, 86400]; % 24 hours in seconds

% 8 initial states: [T_air, W, CO2, T_leaf, z_heater, z_vent, z_fog, z_CO2]
x0 = [15; 0.01; 400; 15; 0; 0.1; 0; 0];

%% 2. Setup Constant Control Inputs (Open Loop - no AI controller yet)
u_const = [10000;  % 10 kW heater
           0.1;    % Vents 10% open
           0.0;    % No fogger
           0.0];   % No CO2 injection

%% 3. Setup Disturbances (Constant weather for this test)
d_const = [10;     % Outside Temp: 10 C
           400;    % Solar Radiation: 400 W/m^2
           0.005;  % Outside Humidity
           400];   % Outside CO2

%% 4. Run the Simulation using ode15s
disp('Simulating 24 hours... please wait...');
[t, x] = ode15s(@(t, x) greenhouse_ode(t, x, u_const, d_const), tspan, x0);
disp('Simulation complete!');

%% 5. Plot the Results
T_air  = x(:, 1);
W      = x(:, 2);
C_CO2  = x(:, 3);
T_leaf = x(:, 4);

% Convert Absolute Humidity to Relative Humidity
e_s = 0.6108 * exp(17.27 * T_air ./ (T_air + 237.3));
e_a = 101.325 * W ./ (0.622 + W);
RH  = (e_a ./ e_s) * 100;

figure('Name', 'Greenhouse Open-Loop Simulation (8-State)', ...
       'Position', [100, 100, 1100, 700]);

% Plot 1: Air Temp vs Leaf Temp
subplot(2,2,1);
plot(t/3600, T_air, 'b', 'LineWidth', 2);
hold on;
plot(t/3600, T_leaf, 'r--', 'LineWidth', 2);
title('Temperatures Over 24 Hours');
xlabel('Time (Hours)');
ylabel('Temperature (°C)');
legend('Air Temp', 'Leaf Temp');
grid on;

% Plot 2: Relative Humidity
subplot(2,2,2);
plot(t/3600, RH, 'g', 'LineWidth', 2);
title('Relative Humidity Over 24 Hours');
xlabel('Time (Hours)');
ylabel('RH (%)');
ylim([0 100]);
grid on;

% Plot 3: CO2 Concentration
subplot(2,2,3);
plot(t/3600, C_CO2, 'k', 'LineWidth', 2);
title('CO_2 Concentration Over 24 Hours');
xlabel('Time (Hours)');
ylabel('CO_2 (ppm)');
grid on;

% Plot 4: Leaf Temp vs Air Temp zoomed in
subplot(2,2,4);
plot(t/3600, T_leaf, 'r', 'LineWidth', 2);
hold on;
plot(t/3600, T_air, 'b--', 'LineWidth', 1.5);
title('Leaf Temp vs Air Temp (Zoomed)');
xlabel('Time (Hours)');
ylabel('Temperature (°C)');
legend('Leaf Temp', 'Air Temp');
grid on;