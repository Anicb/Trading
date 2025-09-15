import numpy as np
import pandas as pd


def moving_average(series: pd.Series, method: str, periods: int) -> pd.Series:
    """Compute a moving average of a price series.

    method: one of 'simple', 'exponential', 'triangular'
    periods: lookback window length
    """
    method = method.lower()
    if method == "simple":
        return series.rolling(periods).mean()
    if method == "exponential":
        return series.ewm(span=periods, adjust=False).mean()
    if method == "triangular":
        first = series.rolling(periods).mean()
        return first.rolling(periods).mean()
    raise ValueError("Method must be 'simple', 'exponential', or 'triangular'")


def add_high_low_bands(
    df: pd.DataFrame,
    averaging_method: str = "simple",
    periods: int = 20,
    offset: float = 2.0,
) -> pd.DataFrame:
    """Return a copy of df with UpperBand, LowerBand, and Signal columns.

    Signal is 1 if Close > UpperBand, -1 if Close < LowerBand, else 0.
    Expected columns: 'High', 'Low', 'Close'.
    """
    required_cols = {"High", "Low", "Close"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {sorted(missing)}")

    out = df.copy()
    ma_high = moving_average(out["High"], averaging_method, periods)
    ma_low = moving_average(out["Low"], averaging_method, periods)
    out["UpperBand"] = ma_high * (1 + offset / 100.0)
    out["LowerBand"] = ma_low * (1 - offset / 100.0)
    out["Signal"] = np.where(
        out["Close"] > out["UpperBand"],
        1,
        np.where(out["Close"] < out["LowerBand"], -1, 0),
    )
    return out


def latest_signal(
    df: pd.DataFrame,
    averaging_method: str = "simple",
    periods: int = 20,
    offset: float = 2.0,
) -> int:
    """Return the latest trading signal: 1 (buy), -1 (sell), or 0 (none)."""
    with_bands = add_high_low_bands(df, averaging_method, periods, offset)
    return int(with_bands["Signal"].iloc[-1])

