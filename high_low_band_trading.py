import argparse
import csv
import os
from datetime import datetime, timezone
from typing import List

from trading import trade_high_low_bands as trade, fetch_market_data
from Logic_Code.high_low_logic import latest_signal


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="High-Low band trading wrapper over trading.trade_high_low_bands",
    )
    p.add_argument("--ticker", default="AAPL", help="Ticker symbol, e.g. AAPL")
    p.add_argument(
        "--symbol-list",
        nargs="+",
        help="Space- or comma-separated list of symbols (e.g. AAPL MSFT, or AAPL,MSFT)",
    )
    p.add_argument(
        "--averaging-method",
        default="simple",
        choices=["simple", "exponential", "triangular"],
        help="Moving average method",
    )
    p.add_argument("--periods", type=int, default=20, help="Lookback periods for MA")
    p.add_argument(
        "--offset",
        type=float,
        default=2.0,
        help="Percent offset for bands (e.g. 2.0 = ±2%)",
    )
    p.add_argument("--quantity", type=int, default=10, help="Order quantity")
    p.add_argument(
        "--interval",
        default="1h",
        help="yfinance interval (e.g. 1m, 5m, 15m, 1h, 1d)",
    )
    p.add_argument(
        "--lookback",
        default="60d",
        help="yfinance period to download (e.g. 5d, 60d, 1y)",
    )
    p.add_argument("--host", default="127.0.0.1", help="IB host")
    p.add_argument("--port", type=int, default=7497, help="IB port")
    p.add_argument("--client-id", type=int, default=1, help="IB client ID")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print signal; do not place orders",
    )
    p.add_argument(
        "--csv",
        metavar="PATH",
        help="Write results to CSV file (use '-' for stdout)",
    )
    p.add_argument(
        "--append",
        action="store_true",
        help="Append to CSV file if it exists (otherwise create)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    # Build tickers list from --symbol-list or fallback to --ticker
    tickers = []
    if args.symbol_list:
        for item in args.symbol_list:
            for sym in str(item).split(","):
                sym = sym.strip()
                if sym:
                    tickers.append(sym)
    if not tickers:
        tickers = [args.ticker]

    rows: List[dict] = []
    ts = datetime.now(timezone.utc).isoformat()
    for sym in tickers:
        # Fetch once; reuse for signal and trade to avoid double download
        df = fetch_market_data(sym, interval=args.interval, lookback=args.lookback)
        sig = latest_signal(
            df,
            averaging_method=args.averaging_method,
            periods=args.periods,
            offset=args.offset,
        )
        result = trade(
            ticker=sym,
            averaging_method=args.averaging_method,
            periods=args.periods,
            offset=args.offset,
            quantity=args.quantity,
            interval=args.interval,
            lookback=args.lookback,
            host=args.host,
            port=args.port,
            client_id=args.client_id,
            dry_run=args.dry_run,
            market_data=df,
        )
        side = "BUY" if sig > 0 else ("SELL" if sig < 0 else "NONE")
        print(f"{sym}: {result}")
        rows.append(
            {
                "timestamp": ts,
                "ticker": sym,
                "interval": args.interval,
                "lookback": args.lookback,
                "method": args.averaging_method,
                "periods": args.periods,
                "offset": args.offset,
                "quantity": args.quantity,
                "signal": int(sig),
                "side": side,
                "action": "dry_run" if args.dry_run else "order",
                "message": result,
            }
        )

    if args.csv:
        fieldnames = [
            "timestamp",
            "ticker",
            "interval",
            "lookback",
            "method",
            "periods",
            "offset",
            "quantity",
            "signal",
            "side",
            "action",
            "message",
        ]
        if args.csv == "-":
            writer = csv.DictWriter(
                f=__import__("sys").stdout, fieldnames=fieldnames, lineterminator="\n"
            )
            writer.writeheader()
            writer.writerows(rows)
        else:
            mode = "a" if args.append else "w"
            write_header = True
            if args.append and os.path.exists(args.csv):
                try:
                    write_header = os.path.getsize(args.csv) == 0
                except OSError:
                    write_header = True
            with open(args.csv, mode, newline="") as f:
                writer = csv.DictWriter(f=f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerows(rows)


if __name__ == "__main__":
    main()
