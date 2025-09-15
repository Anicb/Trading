import os
import sys
import unittest

import pandas as pd

# Ensure project root is on sys.path so Logic_Code is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Logic_Code.high_low_logic import add_high_low_bands, latest_signal


def _make_df(last_close: float) -> pd.DataFrame:
    # 3 rows to satisfy a rolling window of 3 periods
    return pd.DataFrame({
        "High": [100.0, 100.0, 100.0],
        "Low": [100.0, 100.0, 100.0],
        "Close": [100.0, 100.0, last_close],
    })


class TestHighLowLogic(unittest.TestCase):
    def test_buy_signal_when_close_above_upper_band(self):
        df = _make_df(last_close=120.0)  # Upper band at 110 with 10% offset
        sig = latest_signal(df, averaging_method="simple", periods=3, offset=10.0)
        self.assertEqual(sig, 1)

    def test_sell_signal_when_close_below_lower_band(self):
        df = _make_df(last_close=80.0)  # Lower band at 90 with 10% offset
        sig = latest_signal(df, averaging_method="simple", periods=3, offset=10.0)
        self.assertEqual(sig, -1)

    def test_no_signal_when_close_within_bands(self):
        df = _make_df(last_close=100.0)  # Between 90 and 110 with 10% offset
        sig = latest_signal(df, averaging_method="simple", periods=3, offset=10.0)
        self.assertEqual(sig, 0)

    def test_add_high_low_bands_outputs_expected_columns_and_values(self):
        df = _make_df(last_close=100.0)
        out = add_high_low_bands(df, averaging_method="simple", periods=3, offset=10.0)
        for col in ("UpperBand", "LowerBand", "Signal"):
            self.assertIn(col, out.columns)
        # Last row bands should be 110 and 90 given 10% offset on MA=100
        self.assertAlmostEqual(float(out["UpperBand"].iloc[-1]), 110.0, places=6)
        self.assertAlmostEqual(float(out["LowerBand"].iloc[-1]), 90.0, places=6)
        self.assertEqual(int(out["Signal"].iloc[-1]), 0)

    def test_missing_required_columns_raises(self):
        bad = pd.DataFrame({"High": [1, 2, 3], "Close": [1, 2, 3]})
        with self.assertRaises(ValueError):
            add_high_low_bands(bad, averaging_method="simple", periods=3, offset=10.0)


if __name__ == "__main__":
    unittest.main()
