from typing import Optional

import pandas as pd
import yfinance as yf
from ib_insync import IB, Stock, MarketOrder

from Logic_Code.high_low_logic import latest_signal


def fetch_market_data(
    ticker: str,
    interval: str = "1d",
    lookback: str = "60d",
) -> pd.DataFrame:
    """Fetch OHLCV data using yfinance for the given ticker and interval."""
    df = yf.download(ticker, period=lookback, interval=interval, progress=False)
    if df.empty:
        raise ValueError("No data returned; check ticker or interval")
    # Standardize column names to expected OHLC casing
    cols = {c.lower(): c for c in df.columns}
    rename_map = {df.columns[i]: name.title() for i, name in enumerate(cols.keys())}
    df = df.rename(columns=rename_map)
    return df


def execute_ib_order(
    ticker: str,
    side: str,
    quantity: int,
    host: str = "127.0.0.1",
    port: int = 7497,
    client_id: int = 1,
) -> str:
    """Place a market order on Interactive Brokers and return a summary string."""
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id)
        contract = Stock(ticker, "SMART", "USD")
        order = MarketOrder(side.upper(), quantity)
        ib.placeOrder(contract, order)
        return f"Placed {side.upper()} order for {quantity} shares of {ticker}"
    finally:
        try:
            ib.disconnect()
        except Exception:
            pass


def trade_high_low_bands(
    ticker: str,
    averaging_method: str = "simple",
    periods: int = 20,
    offset: float = 2.0,
    quantity: int = 100,
    interval: str = "1d",
    lookback: str = "60d",
    host: str = "127.0.0.1",
    port: int = 7497,
    client_id: int = 1,
    market_data: Optional[pd.DataFrame] = None,
) -> str:
    """Compute latest signal using High-Low bands and execute via IB if needed.

    Trading passes parameters and market data to the logic, which returns a
    buy/sell/none signal. If a trade is signaled, a market order is submitted.

    Returns a human-readable status string.
    """
    df = market_data if market_data is not None else fetch_market_data(
        ticker, interval=interval, lookback=lookback
    )

    signal = latest_signal(
        df,
        averaging_method=averaging_method,
        periods=periods,
        offset=offset,
    )

    if signal == 0:
        return "No trade signal"

    side = "BUY" if signal > 0 else "SELL"
    return execute_ib_order(
        ticker=ticker,
        side=side,
        quantity=quantity,
        host=host,
        port=port,
        client_id=client_id,
    )


if __name__ == "__main__":
    # Example usage
    print(
        trade_high_low_bands(
            ticker="AAPL",
            averaging_method="simple",
            periods=20,
            offset=2.0,
            quantity=10,
            interval="1h",
            lookback="60d",
        )
    )
