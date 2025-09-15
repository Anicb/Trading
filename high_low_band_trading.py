from trading import trade_high_low_bands as trade


if __name__ == "__main__":
    # Example: trade Apple hourly using simple moving average bands
    print(trade(
        ticker="AAPL",
        averaging_method="simple",
        periods=20,
        offset=2.0,
        quantity=10,
        interval="1h",
        lookback="60d",
    ))
