function weather_ts = generate_weather()
    t_end = 86400;     % 24 hours in seconds
    dt = 60;           % 1 minute steps
    time_vector = 0:dt:t_end;

    % 1. Outside Temperature (10°C night to 25°C day)
    T_out = 17.5 - 7.5 * cos(2*pi*(time_vector)/86400); 

    % 2. Solar Radiation (Peaks at 800 W/m^2 at noon)
    I_solar = 800 * max(0, -cos(2*pi*(time_vector)/86400));

    % 3. Outside Humidity and CO2
    W_out = 0.005 * ones(size(time_vector));
    C_out = 400 * ones(size(time_vector));

    weather_data = [T_out', I_solar', W_out', C_out'];
    weather_ts = timeseries(weather_data, time_vector);
end