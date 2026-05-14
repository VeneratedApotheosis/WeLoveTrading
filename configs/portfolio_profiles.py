# configs/portfolio_profiles.py

def get_tsl_profile(df, entries, exits=None):
    """
    Profile 1: The Trend Rider
    Ignores strategy exits and uses a 15% Trailing Stop Loss instead.
    """
    return dict(
        close=df['Close'],
        entries=entries,
        exits=None,          # Explicitly ignoring the strategy's exits
        sl_stop=0.15,        # 15% Stop Loss
        sl_trail=True,       # Trailing activated
        init_cash=10000,
        fees=0.0005,
        freq='d'
    )

def get_strategy_exit_profile(df, entries, exits):
    return dict(
        close=df['Close'],
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.0005,
        freq='d',
        # --- ADD THESE FOR COMPOUNDING ---
        size=1.0,           # Use 100% of available cash
        size_type='percent' # Tells VBT to reinvest profits
    )