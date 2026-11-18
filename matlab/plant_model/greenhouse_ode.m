function dx = greenhouse_ode(x, u)
    % States (8 total)
    T_air  = x(1);
    W      = x(2);
    C_CO2  = x(3);
    T_leaf = x(4);
    
    z_heater = x(5);
    z_vent   = x(6);
    z_fog    = x(7);
    z_CO2    = x(8);

    % Inputs 1-4 are Control Commands (MVs)
    u_heater_cmd = u(1); 
    u_vent_cmd   = u(2); 
    u_fog_cmd    = u(3); 
    u_CO2_cmd    = u(4); 

    % Inputs 5-8 are Outdoor Weather Disturbances (MDs)
    T_out   = u(5); 
    I_solar = u(6); 
    W_out   = u(7); 
    C_out   = u(8); 
    
    %% Actuator Delay Math (Padé Approximation)
    tau_heater = 60; 
    tau_vent   = 30;
    tau_fog    = 10;
    tau_CO2    = 20;
    
    dz_heater_dt = (2 / tau_heater) * (u_heater_cmd - z_heater);
    dz_vent_dt   = (2 / tau_vent)   * (u_vent_cmd - z_vent);
    dz_fog_dt    = (2 / tau_fog)    * (u_fog_cmd - z_fog);
    dz_CO2_dt    = (2 / tau_CO2)    * (u_CO2_cmd - z_CO2);
    
    Q_heater   = 2 * z_heater - u_heater_cmd;
    alpha_vent = 2 * z_vent   - u_vent_cmd;
    m_dot_fog  = 2 * z_fog    - u_fog_cmd;
    m_dot_CO2  = 2 * z_CO2    - u_CO2_cmd;
    
    %% Greenhouse Physics
    V = 1000;            
    A_roof = 500;        
    A_leaf = 400;        
    rho_a = 1.2;         
    c_p = 1006;          
    U = 5.0;             
    lambda = 2.45e6;     
    vent_max = 5.0;      

    m_dot_vent = alpha_vent * vent_max;
    e_s = 0.6108 * exp(17.27 * T_air / (T_air + 237.3)); 
    P_atm = 101.325; 
    e_a = P_atm * W / (0.622 + W); 
    VPD = max(0, e_s - e_a);       
    E_T = A_leaf * (5e-8 * I_solar + 1e-6 * VPD); 
    P_photo = A_leaf * (2e-6 * I_solar * C_CO2 / (C_CO2 + 200)); 

    Q_solar_air = 0.3 * A_roof * I_solar; 
    dT_air_dt = (Q_heater - U * A_roof * (T_air - T_out) - m_dot_vent * c_p * (T_air - T_out) + Q_solar_air - lambda * E_T - lambda * m_dot_fog) / (rho_a * c_p * V);
    dW_dt = (E_T + m_dot_fog - m_dot_vent * (W - W_out)) / (rho_a * V);
    dC_CO2_dt = (m_dot_CO2 - P_photo - (m_dot_vent / rho_a) * (C_CO2 - C_out)) / V;
    
    rho_l_cl_Vl = 500000;  
    sigma = 5.67e-8;       
    epsilon = 0.95;        
    h_c = 20;              
    T_air_K = T_air + 273.15;  
    T_leaf_K = T_leaf + 273.15;      
    Q_rad = sigma * epsilon * A_leaf * (T_air_K^4 - T_leaf_K^4); 
    Q_conv = h_c * A_leaf * (T_air - T_leaf);                    
    dT_leaf_dt = (0.5 * A_leaf * I_solar + Q_rad + Q_conv - lambda * E_T) / rho_l_cl_Vl;

    dx = [dT_air_dt; dW_dt; dC_CO2_dt; dT_leaf_dt; dz_heater_dt; dz_vent_dt; dz_fog_dt; dz_CO2_dt];
end