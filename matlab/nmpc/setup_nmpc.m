% setup_nmpc.m — FINAL CLEAN VERSION

nx = 8; 
ny = 4; 
nlobj = nlmpc(nx, ny, 'mv', 1:4, 'md', 5:8);

nlobj.Ts = 60;                 
nlobj.PredictionHorizon = 20;  
nlobj.ControlHorizon = 5;      

nlobj.Model.StateFcn = "greenhouse_ode";
nlobj.Model.OutputFcn = "greenhouse_output";
nlobj.Model.IsContinuousTime = true;

% Actuator Constraints
nlobj.ManipulatedVariables(1).Min = 0;
nlobj.ManipulatedVariables(1).Max = 50000;  % Heater

nlobj.ManipulatedVariables(2).Min = 0.1;    % Vents ALWAYS at least 10% open!
nlobj.ManipulatedVariables(2).Max = 1;      % Vents max 100%

nlobj.ManipulatedVariables(3).Min = 0;
nlobj.ManipulatedVariables(3).Max = 0.015;  % Fogger reduced to 15 g/s

nlobj.ManipulatedVariables(4).Min = 0;
nlobj.ManipulatedVariables(4).Max = 0.05;   % CO2 Injector

% WEIGHTS
nlobj.Weights.OutputVariables          = [10, 0, 0, 0];
nlobj.Weights.ManipulatedVariables     = [0, 0, 0, 0];
nlobj.Weights.ManipulatedVariablesRate = [0.001, 0.1, 300, 0.1];
%  Fogger rate weight = 300 → ramps up very slowly → vents always open first

disp('--- NMPC Brain Successfully Built! ---');