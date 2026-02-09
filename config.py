# =========================
# SYMBOL & TRADING
# =========================
Trade_Symbol = "EURUSDm"     # Main pair
MAGIC = 123456
DEVIATION = 10               # Maximum slippage

# =========================
# STRATEGY
# =========================
EMA_FAST = 20                # Fast EMA for intraday trend
EMA_SLOW = 50                # Slow EMA for intraday trend

TREND_FAST = 50              # H1 trend filter fast EMA
TREND_SLOW = 200             # H1 trend filter slow EMA

# =========================
# RISK MANAGEMENT
# =========================
RISK_PERCENT = 1             # Risk 1% of account per trade
STOP_LOSS_PIPS = 40          # Bigger SL for day trading
TAKE_PROFIT_PIPS = 80        # TP 2x SL → 1:2 R:R
MAX_TRADES_PER_DAY = 3       # Only 2 trades/day

# =========================
# SESSION FILTER
# =========================
SESSION_START_HOUR = 7       # UTC, London session start
SESSION_END_HOUR = 16        # UTC, NY close

# =========================
# TRAILING STOP
# =========================
USE_TRAILING_SL = True
BREAKEVEN_R = 1.0            # Move SL to break-even after 1x risk
TRAIL_START_R = 1.5           # Start trailing after 1.5x risk in profit
TRAIL_STEP_PIPS = 5           # Minimum pips to move SL each step
