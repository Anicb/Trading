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
    # Standardize/flatten columns to expected OHLC casing and ensure simple Index
    # yfinance can return MultiIndex columns (e.g., when requesting multiple tickers
    # or depending on version). Flatten robustly and normalize names.
    if isinstance(df.columns, pd.MultiIndex):
        # If first level contains the ticker symbol, select it
        try:
            level0 = df.columns.get_level_values(0)
            if ticker in level0:
                df = df.xs(ticker, axis=1, level=0, drop_level=True)
            else:
                df.columns = [c[-1] if isinstance(c, tuple) else str(c) for c in df.columns]
        except Exception:
            df.columns = [c[-1] if isinstance(c, tuple) else str(c) for c in df.columns]
    else:
        # Older/newer yfinance combos may still yield tuple-like entries
        if any(isinstance(c, tuple) for c in df.columns):
            df.columns = [c[-1] if isinstance(c, tuple) else str(c) for c in df.columns]

    # Build a case-insensitive, space/underscore-insensitive map
    def _norm(name: str) -> str:
        return str(name).lower().replace(" ", "").replace("_", "")

    colmap = {_norm(c): c for c in df.columns}
    rename = {}
    for target in ["open", "high", "low", "close", "adjclose", "volume"]:
        if target in colmap:
            pretty = "Adj Close" if target == "adjclose" else target.title()
            rename[colmap[target]] = pretty
    df = df.rename(columns=rename)

    # Sanity check required fields for the strategy
    for required in ("High", "Low", "Close"):
        if required not in df.columns:
            raise ValueError(
                f"Downloaded data missing required column '{required}'. Got columns: {list(df.columns)}"
            )
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
    dry_run: bool = False,
    market_data: Optional[pd.DataFrame] = None,
) -> str:
    """Compute latest signal using High-Low bands and execute via IB if needed.

    Trading passes parameters and market data to the logic, which returns a
    buy/sell/none signal. If a trade is signaled, a market order is submitted.

    Set `dry_run=True` to skip placing orders and just report the signal.

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
    if dry_run:
        return f"Dry run: {side} signal for {ticker} (qty {quantity})"
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
