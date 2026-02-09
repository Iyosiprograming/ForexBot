import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from config import *

_last_candle_time = None

def session_active():
    """Check if current UTC time is within trading session"""
    hour = datetime.utcnow().hour
    return SESSION_START_HOUR <= hour <= SESSION_END_HOUR

def get_signal():
    global _last_candle_time

    if not session_active():
        return None

    # Get last 200 M15 candles
    rates = mt5.copy_rates_from_pos(Trade_Symbol, mt5.TIMEFRAME_M15, 0, 200)
    if rates is None or len(rates) < EMA_SLOW + 2:
        return None

    df = pd.DataFrame(rates)
    candle_time = df.iloc[-1]["time"]

    # Prevent repeated signals on same candle
    if candle_time == _last_candle_time:
        return None
    _last_candle_time = candle_time

    close = df["close"]
    ema_fast = close.ewm(span=EMA_FAST).mean()
    ema_slow = close.ewm(span=EMA_SLOW).mean()

    # H1 trend filter
    rates_h1 = mt5.copy_rates_from_pos(Trade_Symbol, mt5.TIMEFRAME_H1, 0, 200)
    df_h1 = pd.DataFrame(rates_h1)
    ema_fast_h1 = df_h1["close"].ewm(span=TREND_FAST).mean()
    ema_slow_h1 = df_h1["close"].ewm(span=TREND_SLOW).mean()

    trend_up = ema_fast_h1.iloc[-1] > ema_slow_h1.iloc[-1]
    trend_down = ema_fast_h1.iloc[-1] < ema_slow_h1.iloc[-1]

    # EMA cross + trend filter
    if ema_fast.iloc[-2] <= ema_slow.iloc[-2] and ema_fast.iloc[-1] > ema_slow.iloc[-1] and trend_up:
        return "BUY"

    if ema_fast.iloc[-2] >= ema_slow.iloc[-2] and ema_fast.iloc[-1] < ema_slow.iloc[-1] and trend_down:
        return "SELL"

    return None
