% linearize_greenhouse.m
clear; clc;

% 1. Define our Operating Point (A typical Nighttime scenario)
% Updated 8-state version (includes 4 delay states at the end)
x0 = [15;     % Air Temp
      0.01;   % Humidity
      400;    % CO2
      14;     % Leaf Temp
      0;      % Delay state: Heater (starts at 0W)
      0.05;   % Delay state: Vent (starts at 5% open)
      0;      % Delay state: Fogger (starts at 0)
      0];     % Delay state: CO2 injector (starts at 0)

u0 = [10000;  % Heater on low (10 kW)
      0.05;   % Vents 5% open
      0;      % No fog
      0];     % No CO2 injected

d0 = [10;     % Outside Temp: 10 C
      0;      % Solar: 0 (It's night!)
      0.005;  % Outside Humidity
      400];   % Outside CO2

% 2. Calculate the baseline rate of change
dx_baseline = greenhouse_ode(0, x0, u0, d0);

% 3. Perturb each state to build the A matrix (Jacobian)
num_states = 8;
A = zeros(num_states, num_states);
delta = 1e-4; % A tiny nudge

for i = 1:num_states
    x_perturbed = x0;
    x_perturbed(i) = x0(i) + delta; % Nudge one state
    
    % See how the system reacts to the nudge
    dx_perturbed = greenhouse_ode(0, x_perturbed, u0, d0);
    
    % Calculate the slope (Rise over Run)
    A(:, i) = (dx_perturbed - dx_baseline) / delta;
end

disp('--- The A Matrix (Jacobian) ---');
disp(A);

% 4. Eigenvalue Stability Analysis
eigenvalues = eig(A);
disp('--- The Eigenvalues ---');
disp(eigenvalues);

% Check stability
if all(real(eigenvalues) < 0)
    disp('Result: All real parts are NEGATIVE. The greenhouse is Open-Loop STABLE.');
else
    disp('Result: System is unstable! (Something is wrong with the physics)');
end
% 5. Build the B Matrix (Input Jacobian)
num_inputs = 4;
B = zeros(num_states, num_inputs);
for i = 1:num_inputs
    u_perturbed = u0;
    u_perturbed(i) = u0(i) + delta; % Nudge one actuator
    
    % See how the system reacts to the nudged actuator
    dx_perturbed = greenhouse_ode(0, x0, u_perturbed, d0);
    
    % Calculate slope
    B(:, i) = (dx_perturbed - dx_baseline) / delta;
end

disp('--- The B Matrix ---');
disp(B);

% 6. Check Controllability
Ctr = ctrb(A, B); % MATLAB's built-in controllability command
rank_Ctr = rank(Ctr);
disp(['Controllability Matrix Rank: ', num2str(rank_Ctr)]);

if rank_Ctr == num_states
    disp('Result: System is FULLY CONTROLLABLE. We have enough actuators!');
else
    disp('Result: System is NOT fully controllable. We cannot reach all states.');
end