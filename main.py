import time
from datetime import datetime, timezone
from mt5_connect import connect_mt5, shutdown_mt5
from logic import get_signal
from trade_execute import open_trade, trailing_sl, monitor_tp_sl
from config import USE_TRAILING_SL

if not connect_mt5():
    exit()

print("🚀 Smart Forex Bot started")

try:
    counter = 0
    while True:
        monitor_tp_sl()
        signal = get_signal()
        if signal:
            open_trade(signal)
        if USE_TRAILING_SL:
            trailing_sl()

        # Print live status every 5 seconds
        counter += 1
        if counter % 5 == 0:
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            position = open_trade.__globals__["get_position"]()  # safe call to current position
            status = "No open trade"
            if position:
                trade_type = "BUY" if position.type == 0 else "SELL"
                status = f"{trade_type} | Entry: {position.price_open:.5f}"
            print(f"\r⏱ {now} | Status: {status}", end="")


        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Bot stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    shutdown_mt5()
