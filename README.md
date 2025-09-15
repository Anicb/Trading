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

### CLI Wrapper

You can also call the strategy via a CLI wrapper:

```bash
python high_low_band_trading.py \
  --ticker AAPL \
  --averaging-method simple \
  --periods 20 \
  --offset 2.0 \
  --quantity 10 \
  --interval 1h \
  --lookback 60d \
  --dry-run
```

Omit `--dry-run` to place orders via IB (requires IB Gateway/TWS at `127.0.0.1:7497`).

Run for multiple symbols using `--symbol-list` (space- or comma-separated):

```bash
python high_low_band_trading.py \
  --symbol-list AAPL MSFT NVDA \
  --interval 1h --lookback 60d --dry-run

# or comma-separated
python high_low_band_trading.py --symbol-list AAPL,MSFT,NVDA --dry-run
```

CSV output of results (to stdout or a file):

```bash
# Write to stdout
python high_low_band_trading.py --symbol-list AAPL MSFT --dry-run --csv -

# Write to file
python high_low_band_trading.py --symbol-list AAPL,MSFT,NVDA --dry-run --csv results.csv
```

### Dry Run

To inspect signals without placing any orders, pass `dry_run=True`:

```python
trade_high_low_bands(
    ticker="AAPL",
    averaging_method="simple",
    periods=20,
    offset=2.0,
    quantity=10,
    interval="1h",
    lookback="60d",
    dry_run=True,
)
```
