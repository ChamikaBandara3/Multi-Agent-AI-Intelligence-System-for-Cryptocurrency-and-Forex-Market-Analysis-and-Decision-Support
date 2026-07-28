import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from utils.indicators import analyze_all_indicators

def fetch_forex_ticker(symbol: str) -> Dict[str, Any]:
    """Fetch recent price data for Forex pair or Commodity via yfinance or fallback."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5d", interval="1h")
        if not history.empty:
            curr_price = float(history["Close"].iloc[-1])
            prev_price = float(history["Close"].iloc[-2]) if len(history) > 1 else curr_price
            change_pct = ((curr_price - prev_price) / prev_price) * 100
            
            return {
                "symbol": symbol,
                "price": curr_price,
                "high24h": float(history["High"].max()),
                "low24h": float(history["Low"].min()),
                "volume24h": float(history["Volume"].sum()) if "Volume" in history else 0.0,
                "price_change_percent": round(change_pct, 2),
                "source": "Yahoo Finance (Live Feed)"
            }
    except Exception:
        pass
        
    defaults = {
        "EURUSD=X": 1.0850,
        "GBPUSD=X": 1.2920,
        "USDJPY=X": 154.50,
        "GC=F": 2415.80,
        "^NDX": 19850.00
    }
    base = defaults.get(symbol, 1.0850)
    return {
        "symbol": symbol,
        "price": base,
        "high24h": round(base * 1.008, 4),
        "low24h": round(base * 0.992, 4),
        "volume24h": 1254000.0,
        "price_change_percent": 0.42,
        "source": "Simulated Forex Feed"
    }

def fetch_forex_klines(symbol: str, limit: int = 100) -> pd.DataFrame:
    """Fetch historical dataframe for Forex pair or Commodity."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1mo", interval="1d")
        if not df.empty and len(df) >= 10:
            df = df.rename(columns={
                "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"
            })
            df["timestamp"] = df.index
            return df.tail(limit)
    except Exception:
        pass
        
    dates = pd.date_range(end=pd.Timestamp.now(), periods=limit, freq="D")
    defaults = {"EURUSD=X": 1.0850, "GBPUSD=X": 1.2920, "USDJPY=X": 154.50, "GC=F": 2415.80, "^NDX": 19850.00}
    base_price = defaults.get(symbol, 1.0850)
    np.random.seed(42)
    noise = np.random.normal(0, base_price * 0.003, limit).cumsum()
    prices = base_price + noise
    
    return pd.DataFrame({
        "timestamp": dates,
        "open": prices - (base_price * 0.001),
        "high": prices + (base_price * 0.003),
        "low": prices - (base_price * 0.003),
        "close": prices,
        "volume": np.random.uniform(50000, 200000, limit)
    })

def get_forex_market_analysis(symbol: str) -> Tuple[Dict[str, Any], Dict[str, Any], pd.DataFrame]:
    """Fetch forex data and run full technical analysis suite."""
    ticker = fetch_forex_ticker(symbol)
    df = fetch_forex_klines(symbol)
    indicators = analyze_all_indicators(df)
    return ticker, indicators, df
