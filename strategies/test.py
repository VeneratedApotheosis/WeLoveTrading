import pandas_ta as ta

def generate_signals(df):
    
    # --- 1. CALCULATE ALL INDICATORS ---
    sma_200 = ta.sma(df['Close'], length=200)
    fast_sma = ta.sma(df['Close'], length=20)
    slow_sma = ta.sma(df['Close'], length=50)
    
    # Z-Score for the sideways chop
    zscore = ta.zscore(df['Close'], length=30)
    
    # --- 2. DEFINE THE MARKET REGIMES ---
    # We use the 200 SMA as our master switch
    regime_trending = df['Close'] > sma_200
    regime_sideways = df['Close'] <= sma_200

    # --- 3. DEFINE THE DESIRED STATES ---
    # State A: We want the Fast SMA to be above the Slow SMA
    state_sma_bullish = fast_sma > slow_sma
    
    # State B: We want the Z-score to be extremely oversold
    state_zscore_oversold = zscore < -1.5

    # --- 4. COMBINE REGIMES WITH STATES ---
    
    # Strategy 1: Trend Following
    # We are in a trend, AND the fast SMA is currently above the slow SMA
    trend_buy_condition = regime_trending & state_sma_bullish
    
    # Strategy 2: Mean Reversion
    # We are sideways, AND the price just flash-crashed to a statistical extreme
    sideways_buy_condition = regime_sideways & state_zscore_oversold
    
    # Combine both possible buy conditions into one master state
    master_buy_state = trend_buy_condition | sideways_buy_condition

    # --- 5. THE VECTORBT "HISTORIC" TRICK ---
    # We only trigger a buy entry on the exact day our master state FLIPS from False to True.
    # This solves your "missed crossover" problem entirely!
    entries = master_buy_state & (~master_buy_state.shift(1).fillna(False))

    # --- 6. EXITS ---
    # Exit 1: The trend breaks (Fast crosses below Slow)
    trend_exit = (fast_sma < slow_sma) & (fast_sma.shift(1) >= slow_sma.shift(1))
    
    # Exit 2: The sideways bounce finishes (Z-score hits 0)
    sideways_exit = (zscore > 0) & (zscore.shift(1) <= 0)
    
    # The bot will exit if EITHER exit condition is met
    exits = trend_exit | sideways_exit

    return entries, exits