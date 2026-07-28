import numpy as np
import pandas as pd
from typing import Dict, Any

def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate Relative Strength Index (RSI)."""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])

def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal_period: int = 9) -> Dict[str, float]:
    """Calculate Moving Average Convergence Divergence (MACD)."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    
    # Check for recent divergence pattern
    prev_macd = float(macd_line.iloc[-2]) if len(macd_line) > 1 else float(macd_line.iloc[-1])
    curr_macd = float(macd_line.iloc[-1])
    prev_hist = float(histogram.iloc[-2]) if len(histogram) > 1 else float(histogram.iloc[-1])
    curr_hist = float(histogram.iloc[-1])
    
    divergence = "Neutral"
    if curr_hist > 0 and prev_hist <= 0:
        divergence = "Bullish Crossover"
    elif curr_hist < 0 and prev_hist >= 0:
        divergence = "Bearish Crossover"
    elif curr_macd > prev_macd and curr_hist > prev_hist:
        divergence = "Bullish Momentum"
    elif curr_macd < prev_macd and curr_hist < prev_hist:
        divergence = "Bearish Momentum"

    return {
        "macd": float(curr_macd),
        "signal": float(signal_line.iloc[-1]),
        "histogram": float(curr_hist),
        "pattern": divergence
    }

def calculate_ema(prices: pd.Series, span: int) -> float:
    """Calculate Exponential Moving Average (EMA)."""
    ema = prices.ewm(span=span, adjust=False).mean()
    return float(ema.iloc[-1])

def calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std: float = 2.0) -> Dict[str, float]:
    """Calculate Bollinger Bands (Upper, Middle, Lower)."""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    
    return {
        "upper": float(upper.iloc[-1]),
        "middle": float(sma.iloc[-1]),
        "lower": float(lower.iloc[-1]),
        "bandwidth": float(((upper.iloc[-1] - lower.iloc[-1]) / (sma.iloc[-1] + 1e-10)) * 100)
    }

def calculate_support_resistance(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate Key Pivot Support & Resistance Levels."""
    high = float(df['high'].max())
    low = float(df['low'].min())
    close = float(df['close'].iloc[-1])
    
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    
    return {
        "pivot": pivot,
        "resistance_1": r1,
        "resistance_2": r2,
        "support_1": s1,
        "support_2": s2
    }

def calculate_atr(df: pd.DataFrame, period: int = 14) -> float:
    """Calculate Average True Range (ATR) for volatility risk calculation."""
    high = df['high']
    low = df['low']
    close = df['close'].shift(1)
    
    tr1 = high - low
    tr2 = (high - close).abs()
    tr3 = (low - close).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return float(atr.iloc[-1]) if not np.isnan(atr.iloc[-1]) else float(tr.mean())

def analyze_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Runs complete technical analysis suite on OHLCV DataFrame."""
    prices = df['close']
    current_price = float(prices.iloc[-1])
    
    rsi = calculate_rsi(prices)
    macd = calculate_macd(prices)
    ema20 = calculate_ema(prices, 20)
    ema50 = calculate_ema(prices, 50)
    ema200 = calculate_ema(prices, 200)
    bb = calculate_bollinger_bands(prices)
    sr = calculate_support_resistance(df)
    atr = calculate_atr(df)
    
    # Simple overall indicator score
    bullish_signals = 0
    bearish_signals = 0
    
    if rsi < 30:
        bullish_signals += 2  # Oversold reversal
    elif rsi > 70:
        bearish_signals += 2  # Overbought reversal
    elif rsi > 50:
        bullish_signals += 1
    else:
        bearish_signals += 1
        
    if macd['histogram'] > 0:
        bullish_signals += 2
    else:
        bearish_signals += 2
        
    if current_price > ema50:
        bullish_signals += 1
    else:
        bearish_signals += 1
        
    if current_price > ema200:
        bullish_signals += 2 # Strong macro bull trend
    else:
        bearish_signals += 2 # Macro bear trend
        
    trend = "Bullish" if bullish_signals > bearish_signals else ("Bearish" if bearish_signals > bullish_signals else "Neutral")
    
    return {
        "current_price": current_price,
        "rsi": round(rsi, 2),
        "rsi_status": "Oversold" if rsi < 30 else ("Overbought" if rsi > 70 else "Neutral"),
        "macd": macd,
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "ema200": round(ema200, 2),
        "bollinger": bb,
        "levels": sr,
        "atr": round(atr, 4),
        "trend_summary": trend,
        "bullish_score": bullish_signals,
        "bearish_score": bearish_signals
    }
