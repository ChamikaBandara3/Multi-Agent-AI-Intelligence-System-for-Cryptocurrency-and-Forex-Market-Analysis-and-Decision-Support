from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    LangGraph Agent State definition for structured inter-agent communication.
    Transfers data cleanly between Market Data, News, Sentiment, Risk, and Decision agents.
    """
    asset: str                             # Selected ticker (e.g. BTCUSDT, EUR/USD)
    asset_type: str                        # 'crypto', 'forex', 'commodity', 'index'
    market_data: Dict[str, Any]            # Ticker price, 24h change, high, low, volume
    technical_indicators: Dict[str, Any]   # RSI, MACD, EMA, Bollinger, S/R levels, ATR
    news_data: Dict[str, Any]              # Aggregated headlines & news sentiment
    sentiment_data: Dict[str, Any]         # Fear & Greed Index & crowd score
    risk_assessment: Dict[str, Any]        # Risk rating 1-5, SL, TP, volatility warning
    decision_recommendation: Dict[str, Any]# Final decision (BUY/SELL/HOLD, reasoning, confidence)
    agent_logs: List[Dict[str, str]]       # Inter-agent message logs for transparent visualization
