import MetaTrader5 as mt5

def connect_mt5():
    if not mt5.initialize():
        print("❌ MT5 initialize failed")
        return False
    print("✅ MT5 connected")
    return True

def shutdown_mt5():
    mt5.shutdown()
    print("ℹ️ MT5 shutdown complete")
