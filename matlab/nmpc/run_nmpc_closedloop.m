% run_nmpc_closedloop.m
clear; clc; close all;

%% 1. Weather & Controller Setup
weather_ts = generate_weather(); 
setup_nmpc;       

%% 2. Validate NMPC
x0 = [15, 0.01, 400, 15, 0, 0.1, 0, 0]; % 1x8
u0 = [10000, 0.1, 0, 0];                % 1x4 MVs
d0 = [10, 0, 0.005, 400];               % 1x4 MDs

disp('Validating NMPC functions...');
validateFcns(nlobj, x0, u0, d0);
disp('Validation successful!');

%% 3. Simulation Setup
t_sim = 86400;      % 24 hours
dt = 60;            % 1 min steps
steps = t_sim / dt; 

x_history = zeros(steps+1, 8);
u_history = zeros(steps, 4);
t_history = (0:steps)*dt;

x_current = x0';
x_history(1, :) = x0;

y_ref = [22, 0.008, 800, 22];

weather_time = weather_ts.Time;
weather_data = weather_ts.Data;

%% 4. Closed-Loop Simulation Loop
disp('Running closed-loop NMPC simulation... (This may take ~1 minute)');
nlmpc_options = nlmpcmoveopt;

for k = 1:steps
    t_curr = (k-1)*dt;
    
    % Interpolate weather
    d_curr = [interp1(weather_time, weather_data(:,1), t_curr), ...
              interp1(weather_time, weather_data(:,2), t_curr), ...
              interp1(weather_time, weather_data(:,3), t_curr), ...
              interp1(weather_time, weather_data(:,4), t_curr)];
          
    if k == 1
        last_u = u0;
    else
        last_u = u_history(k-1, :);
    end
    
    % Calculate optimal control action
    [u_optimal, nlmpc_options] = nlmpcmove(nlobj, x_current, last_u, y_ref, d_curr, nlmpc_options);
    u_history(k, :) = u_optimal';
    
    % Combine optimal controls and current weather into 8-element vector for ode15s
    u_combined = [u_optimal; d_curr'];
    
    % Simulate greenhouse physics for 1 minute
    tspan = [t_curr, t_curr + dt];
    [~, x_next] = ode15s(@(t, x) greenhouse_ode(x, u_combined), tspan, x_current);
    
    x_current = x_next(end, :)';
    x_history(k+1, :) = x_current';
    
    if mod(k, 120) == 0
        fprintf('Simulated %d / 24 hours...\n', k/60);
    end
end
disp('Simulation complete!');

%% 5. Plot Results
figure('Name', 'NMPC Closed-Loop Greenhouse Control', 'Position', [100, 100, 1100, 700]);

% Subplot 1: Air Temperature Tracking
subplot(2,2,1);
plot(t_history/3600, x_history(:, 1), 'b', 'LineWidth', 2);
hold on;
plot(t_history/3600, y_ref(1)*ones(size(t_history)), 'r--', 'LineWidth', 1.5);
title('Air Temperature Control');
xlabel('Time (Hours)'); ylabel('Temperature (°C)');
legend('Actual Temp', 'Target (22°C)', 'Location', 'SouthEast');
grid on;

% Subplot 2: CO2 Tracking
subplot(2,2,2);
plot(t_history/3600, x_history(:, 3), 'k', 'LineWidth', 2);
hold on;
plot(t_history/3600, y_ref(3)*ones(size(t_history)), 'r--', 'LineWidth', 1.5);
title('CO_2 Concentration Control');
xlabel('Time (Hours)'); ylabel('CO_2 (ppm)');
legend('Actual CO_2', 'Target (800 ppm)', 'Location', 'SouthEast');
grid on;

% Subplot 3: Actuator Responses (Heater, Vents & Fogger)
subplot(2,2,3);
yyaxis left
plot(t_history(1:end-1)/3600, u_history(:, 1)/1000, 'Color', [0.85 0.33 0.1], 'LineWidth', 1.5);
hold on;
% Plot fogger in grams per second (g/s)
plot(t_history(1:end-1)/3600, u_history(:, 3)*1000, 'Color', [0.47 0.67 0.19], 'LineWidth', 1.5);
ylabel('Heater (kW) & Fogger (g/s)');

yyaxis right
plot(t_history(1:end-1)/3600, u_history(:, 2)*100, 'Color', [0 0.44 0.74], 'LineWidth', 1.5);
ylabel('Vents Open (%)');
title('Actuator Actions'); xlabel('Time (Hours)');
legend('Heater (kW)', 'Fogger (g/s)', 'Vents (%)', 'Location', 'NorthWest'); grid on;

% --- CALCULATE RELATIVE HUMIDITY ---
T_air_hist = x_history(:, 1);
W_hist = x_history(:, 2);
e_s_hist = 0.6108 * exp(17.27 * T_air_hist ./ (T_air_hist + 237.3));
e_a_hist = 101.325 * W_hist ./ (0.622 + W_hist);
RH_hist = (e_a_hist ./ e_s_hist) * 100;

% Subplot 4: Relative Humidity
subplot(2,2,4);
plot(t_history/3600, RH_hist, 'g', 'LineWidth', 2);
title('Relative Humidity'); xlabel('Time (Hours)'); ylabel('RH (%)');
ylim([0 100]); grid on;
% Save NMPC results to file
save('nmpc_closedloop_results.mat', 't_history', 'x_history', 'u_history');
disp('Saved NMPC data to nmpc_closedloop_results.mat');