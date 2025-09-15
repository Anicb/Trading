import numpy as np
import pandas as pd
import yfinance as yf
from ib_insync import IB, Stock, MarketOrder


def moving_average(series: pd.Series, method: str, periods: int) -> pd.Series:
    """Return a moving average of *series* using the specified method."""
    method = method.lower()
    if method == "simple":
        return series.rolling(periods).mean()
    if method == "exponential":
        return series.ewm(span=periods, adjust=False).mean()
    if method == "triangular":
        first = series.rolling(periods).mean()
        return first.rolling(periods).mean()
    raise ValueError("Method must be 'simple', 'exponential', or 'triangular'")


def high_low_band_algo(
    df: pd.DataFrame,
    averaging_method: str = "simple",
    periods: int = 20,
    offset: float = 2.0,
) -> pd.DataFrame:
    """Add high/low bands and trading signals to *df*.

    The signal is 1 when close price is above the upper band,
    -1 when below the lower band, and 0 otherwise.
    """
    df = df.copy()
    ma_high = moving_average(df["High"], averaging_method, periods)
    ma_low = moving_average(df["Low"], averaging_method, periods)
    df["UpperBand"] = ma_high * (1 + offset / 100.0)
    df["LowerBand"] = ma_low * (1 - offset / 100.0)
    df["Signal"] = np.where(
        df["Close"] > df["UpperBand"],
        1,
        np.where(df["Close"] < df["LowerBand"], -1, 0),
    )
    return df


def trade(
    ticker: str,
    averaging_method: str = "simple",
    interval: str = "1d",
    periods: int = 20,
    offset: float = 2.0,
    quantity: int = 100,
    host: str = "127.0.0.1",
    port: int = 7497,
    client_id: int = 1,
) -> str:
    """Fetch data, compute signal, and place an IB market order if signaled."""
    df = yf.download(ticker, period="60d", interval=interval, progress=False)
    if df.empty:
        raise ValueError("No data returned; check ticker or interval")

    results = high_low_band_algo(df, averaging_method, periods, offset)
    signal = int(results["Signal"].iloc[-1])
    if signal == 0:
        return "No trade signal"

    ib = IB()
    ib.connect(host, port, clientId=client_id)
    contract = Stock(ticker, "SMART", "USD")
    side = "BUY" if signal > 0 else "SELL"
    order = MarketOrder(side, quantity)
    ib.placeOrder(contract, order)
    ib.disconnect()
    return f"Placed {side} order for {quantity} shares of {ticker}"


if __name__ == "__main__":
    # Example: trade Apple hourly using simple moving average bands
    print(
        trade(
            ticker="AAPL",
            averaging_method="simple",
            interval="1h",
            periods=20,
            offset=2.0,
            quantity=10,
        )
    )
