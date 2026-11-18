function y = greenhouse_output(x, u)
    % Output the first 4 states: [T_air, W, C_CO2, T_leaf]
    y = x(1:4);
end