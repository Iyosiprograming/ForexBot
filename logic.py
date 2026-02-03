import MetaTrader5 as mt5
import pandas as pd
from config import Trade_Symbol, EMA_FAST, EMA_SLOW
from datetime import datetime

_last_candle_time = None

def get_signal():
    global _last_candle_time

    rates = mt5.copy_rates_from_pos(Trade_Symbol, mt5.TIMEFRAME_M1, 0, 100)
    if rates is None or len(rates) < EMA_SLOW + 2:
        print("🔴 Symbol not found or insufficient data")
        print(f"   Symbol: {Trade_Symbol}")
        print(f"   Data points: {len(rates) if rates else 0}, Required: {EMA_SLOW + 2}")
        return None

    df = pd.DataFrame(rates)

    candle_time = df.iloc[-1]["time"]
    human_time = datetime.fromtimestamp(candle_time).strftime('%Y-%m-%d %H:%M:%S')
    
    if candle_time == _last_candle_time:
        print(f"⏸️  No new candle")
        print(f"   Last candle: {human_time}")
        print(f"   Symbol: {Trade_Symbol}")
        return None

    _last_candle_time = candle_time

    close = df["close"]
    ema_fast = close.ewm(span=EMA_FAST, adjust=False).mean()
    ema_slow = close.ewm(span=EMA_SLOW, adjust=False).mean()

    fast_prev, fast_curr = ema_fast.iloc[-2], ema_fast.iloc[-1]
    slow_prev, slow_curr = ema_slow.iloc[-2], ema_slow.iloc[-1]
    
    current_price = close.iloc[-1]
    
    print("=" * 50)
    print(f"📊 SIGNAL ANALYSIS - {Trade_Symbol}")
    print("=" * 50)
    print(f"📅 Time: {human_time}")
    print(f"💰 Price: {current_price:.5f}")
    print(f"📈 EMA{EMA_FAST}: {fast_curr:.5f}")
    print(f"📉 EMA{EMA_SLOW}: {slow_curr:.5f}")
    print(f"📏 Spread: {abs(fast_curr - slow_curr):.5f}")
    print("-" * 50)

    if fast_prev <= slow_prev and fast_curr > slow_curr:
        print("✅ BUY SIGNAL DETECTED")
        print(f"   EMA{EMA_FAST} crossed above EMA{EMA_SLOW}")
        print(f"   Previous: Fast={fast_prev:.5f}, Slow={slow_prev:.5f}")
        print(f"   Current:  Fast={fast_curr:.5f}, Slow={slow_curr:.5f}")
        print("=" * 50)
        return "BUY"

    if fast_prev >= slow_prev and fast_curr < slow_curr:
        print("✅ SELL SIGNAL DETECTED")
        print(f"   EMA{EMA_FAST} crossed below EMA{EMA_SLOW}")
        print(f"   Previous: Fast={fast_prev:.5f}, Slow={slow_prev:.5f}")
        print(f"   Current:  Fast={fast_curr:.5f}, Slow={slow_curr:.5f}")
        print("=" * 50)
        return "SELL"

    print("⏸️  NO SIGNAL")
    print(f"   EMA{EMA_FAST}: {fast_curr:.5f}")
    print(f"   EMA{EMA_SLOW}: {slow_curr:.5f}")
    print(f"   Relationship: {'Fast > Slow' if fast_curr > slow_curr else 'Fast < Slow'}")
    print("=" * 50)
    return None