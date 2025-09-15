# Trading

Tools and Algos for Trading

## High-Low Band Algorithm

This project now separates the trading execution from the signal logic:

- `Logic_Code/high_low_logic.py`: pure signal logic (no broker calls)
- `trading.py`: trading orchestration (fetch data, call logic, place orders)

### Installation

```bash
pip install numpy pandas yfinance ib_insync
```

### Example

```python
from trading import trade_high_low_bands

# Trade Apple using hourly data and a simple moving average
trade_high_low_bands(
    ticker="AAPL",
    averaging_method="simple",  # 'exponential' or 'triangular' also supported
    periods=20,
    offset=2.0,
    quantity=10,
    interval="1h",
    lookback="60d",
)
```

Or just run `python trading.py` to execute the example in the module.

The function downloads recent price data, calculates high and low bands with the
requested moving average, generates a buy/sell signal, and places a market order
via Interactive Brokers if a signal is present. Ensure that the IB Gateway or
Trader Workstation is running and accessible before running the script.

*This code is for educational purposes only; use it at your own risk.*
