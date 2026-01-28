import MetaTrader5 as mt5
import pandas as pd
from mt5_connect import connect_mt5
from config import Trade_Symbol, EMA_FAST, EMA_SLOW

def get_signal():
    """Return 'BUY', 'SELL', or None based on EMA crossover."""

    # GET DATA (skip forming candle)
    rates = mt5.copy_rates_from_pos(Trade_Symbol, mt5.TIMEFRAME_M1, 1, 100)
    if rates is None:
        print("Symbol not found")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # EMAs
    df['ema_fast'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()

    # Previous values
    df['prev_fast'] = df['ema_fast'].shift(1)
    df['prev_slow'] = df['ema_slow'].shift(1)

    # Signals
    df['long_signal'] = (df['prev_fast'] <= df['prev_slow']) & (df['ema_fast'] > df['ema_slow'])
    df['short_signal'] = (df['prev_fast'] >= df['prev_slow']) & (df['ema_fast'] < df['ema_slow'])

    last = df.iloc[-1]

    if last['long_signal']:
        print("📈 BUY signal")
        return "BUY"

    elif last['short_signal']:
        print("📉 SELL signal")
        return "SELL"

    else:
        print("⏸️ No signal")
        return None

# Optional: quick test if run directly
if __name__ == "__main__":
    if not connect_mt5():
        mt5.shutdown()
        exit()
    signal = get_signal()
    print("Signal returned:", signal)
    mt5.shutdown()
