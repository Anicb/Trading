# Trading

Tools and Algos for Trading

## High-Low Band Algorithm

This project includes a simple high/low band trading signal generator and a
`trade` function that fetches market data from [Yahoo Finance](https://finance.yahoo.com)
and executes trades through the [Interactive Brokers](https://www.interactivebrokers.com)
API (`ib_insync`).

### Installation

```bash
pip install numpy pandas yfinance ib_insync
```

### Example

```python
from high_low_band_trading import trade

# Trade Apple using hourly data and a simple moving average
trade(
    ticker="AAPL",
    averaging_method="simple",  # 'exponential' or 'triangular' also supported
    interval="1h",
    periods=20,
    offset=2.0,
    quantity=10,
)
```

The function downloads recent price data, calculates high and low bands with the
requested moving average, generates a buy/sell signal, and places a market order
via Interactive Brokers if a signal is present. Ensure that the IB Gateway or
Trader Workstation is running and accessible before running the script.

*This code is for educational purposes only; use it at your own risk.*
