def plot_sarimax_forecast(ticker, data, forecast_steps=180):
    """
    Plots the historical close prices and the SARIMA forecast for a given stock.

    Args:
        ticker: The ticker symbol of the stock.
        data: A DataFrame containing 'Close' and 'Volume' columns.
        forecast_steps: The number of steps to forecast (default: 180).
    """
    if ticker not in data.columns:
        print(f"Data not found for ticker: {ticker}")
        return  # Exit function if data is missing

    df = data[ticker][['Close', 'Volume']]
    model = SARIMAX(df['Close'], exog=df['Volume'], order=(1,1,1), seasonal_order=(0,0,0,0))
    result = model.fit()

    # Limit forecast_steps to available volume data
    max_forecast_steps = len(df['Volume'])
    forecast_steps = min(forecast_steps, max_forecast_steps)  # Use minimum of desired and available steps

    try:
        forecast = result.get_forecast(steps=forecast_steps, exog=df['Volume'][-forecast_steps:])
        forecast_prices = forecast.predicted_mean
        forecast_conf_int = forecast.conf_int(alpha=0.05)  # 95% confidence interval
        forecast_dates = forecast_conf_int.index  # Extract dates from index

        prices_dict[ticker]["Prediction"] = forecast_prices[-1]  # Last predicted value

        # Slice forecast_dates to match forecast_prices
        forecast_dates = forecast.dates[1:]  # Exclude the first element


        # Plot historical close prices
        plt.plot(df.index, df['Close'], label='Historical Close')

        # Plot forecast prices
        plt.plot(forecast_dates, forecast_prices, label='SARIMA Forecast')

        # Set labels and title
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'SARIMA Forecast for {ticker} (using {forecast_steps} steps)')  # Indicate used steps
        plt.legend()
        plt.grid(True)
        plt.show()
    except KeyError:
        print(f"Insufficient data for forecast steps: {forecast_steps} for ticker: {ticker}")



# def plot_sarimax_forecast(ticker, data, forecast_steps=180):
    """
    Plots the historical close prices and the SARIMA forecast for a given stock.

    Args:
        ticker: The ticker symbol of the stock.
        data: A DataFrame containing 'Close' and 'Volume' columns.
        forecast_steps: The number of steps to forecast (default: 180).
    """
    if ticker not in data.columns:
        print(f"Data not found for ticker: {ticker}")
        return  # Exit function if data is missing

    df = data[ticker][['Close', 'Volume']]

    # Check for missing values
    if df['Volume'].isnull().sum() > 0:
        print(f"Warning: Missing values found in 'Volume' data for {ticker}")

    # Check data structure (assuming 'Date' column exists)
    if not isinstance(df.index, pd.DatetimeIndex):
        df.set_index('Date', inplace=True)

    # Limit forecast steps based on available volume data
    max_forecast_steps = len(df['Volume'])
    if forecast_steps > max_forecast_steps:
        print(f"Warning: Insufficient volume data for {forecast_steps} steps. Using maximum available steps: {max_forecast_steps}")
        forecast_steps = max_forecast_steps

    try:
        forecast = result.get_forecast(steps=forecast_steps, exog=df['Volume'][-forecast_steps:])
        forecast_prices = forecast.predicted_mean
        forecast_conf_int = forecast.conf_int(alpha=0.05)  # 95% confidence interval
        forecast_dates = forecast_conf_int.index  # Extract dates from index

        prices_dict[ticker]["Prediction"] = forecast_prices[-1]  # Last predicted value

        # Slice forecast_dates to match forecast_prices
        forecast_dates = forecast.dates[1:]  # Exclude the first element


        # Plot historical close prices
        plt.plot(df.index, df['Close'], label='Historical Close')

        # Plot forecast prices
        plt.plot(forecast_dates, forecast_prices, label='SARIMA Forecast')

        # Set labels and title
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'SARIMA Forecast for {ticker} (using {forecast_steps} steps)')  # Indicate used steps
        plt.legend()
        plt.grid(True)
        plt.show()
    except KeyError:
        print(f"Insufficient data for forecast steps: {forecast_steps} for ticker: {ticker}")


# Assuming 'data' has been populated with downloaded stock data
plot_sarimax_forecast(ticker='J', data=data) 
