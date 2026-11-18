% test_delay.m
clear; clc; close all;

% Create a mathematical 's' variable for transfer functions
s = tf('s');

% 1. A pure 60-second delay (This is reality)
tau = 60; 
pure_delay = exp(-tau * s);

% 2. First-order Padé approximation (This is the math trick we will use)
% Formula: e^(-tau*s) ~ (1 - (tau/2)*s) / (1 + (tau/2)*s)
pade_approx = (1 - (tau/2)*s) / (1 + (tau/2)*s);

% 3. Plot a "Step Response" (What happens if we turn the switch ON at time = 0)
figure('Name', 'Understanding Actuator Delay', 'Position', [300, 300, 700, 400]);
step(pure_delay, 'b', pade_approx, 'r--', 150); % Simulate for 150 seconds

title('Turning on a Heater Switch at Time = 0');
ylabel('Heater Output');
xlabel('Time (Seconds)');
legend('Pure Delay (Reality)', 'Padé Approximation (Our Math)', 'Location', 'NorthWest');
grid on;