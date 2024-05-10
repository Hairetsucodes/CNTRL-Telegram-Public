import yfinance as yf
``
def oil_price():
    # Define the crude oil symbol
    symbol = "CL=F"  # Symbol for WTI Crude Oil Futures

    # Create a Ticker object
    ticker = yf.Ticker(symbol)

    # Get the latest price data
    data = ticker.history(period="1d")

    # Extract the latest close price
    latest_price = data["Close"].iloc[-1]

    # Print the latest price
    print(f"The current price of crude oil is: ${latest_price:.2f}")

    return latest_price