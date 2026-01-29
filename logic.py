import MetaTrader5 as mt5
import pandas as pd
from config import Trade_Symbol, EMA_FAST, EMA_SLOW

_last_candle_time = None


def get_signal():
    global _last_candle_time

    rates = mt5.copy_rates_from_pos(Trade_Symbol, mt5.TIMEFRAME_M1, 0, 100)
    if rates is None or len(rates) < EMA_SLOW + 2:
        print("Symbol not found")
        return None

    df = pd.DataFrame(rates)

    candle_time = df.iloc[-1]["time"]
    if candle_time == _last_candle_time:
        print("⏸️ No signal")
        return None

    _last_candle_time = candle_time

    close = df["close"]
    ema_fast = close.ewm(span=EMA_FAST, adjust=False).mean()
    ema_slow = close.ewm(span=EMA_SLOW, adjust=False).mean()

    fast_prev, fast_curr = ema_fast.iloc[-2], ema_fast.iloc[-1]
    slow_prev, slow_curr = ema_slow.iloc[-2], ema_slow.iloc[-1]

    if fast_prev <= slow_prev and fast_curr > slow_curr:
        print("📈 BUY signal")
        return "BUY"

    if fast_prev >= slow_prev and fast_curr < slow_curr:
        print("📉 SELL signal")
        return "SELL"

    print("⏸️ No signal")
    return None
