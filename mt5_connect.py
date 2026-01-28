import MetaTrader5 as mt5
from dotenv import load_dotenv
import os

load_dotenv()

MT5_Login = int(os.getenv("MT5_LOGIN"))
MT5_Password = os.getenv("MT5_PASSWORD")
MT5_Server = os.getenv("MT5_SERVER")

def connect_mt5():
    """Initialize MT5 connection."""
    if not mt5.initialize(login=MT5_Login, password=MT5_Password, server=MT5_Server):
        print("MT5 init failed:", mt5.last_error())
        return False

    print("✅ MT5 initialized successfully")

    from config import Trade_Symbol
    if not mt5.symbol_select(Trade_Symbol, True):
        print(f"⚠ Could not select symbol {Trade_Symbol}")
        return False

    return True


def shutdown_mt5():
    """Clean shutdown."""
    mt5.shutdown()
    print("MT5 shutdown complete")


if __name__ == "__main__":
    if connect_mt5():
        shutdown_mt5()
