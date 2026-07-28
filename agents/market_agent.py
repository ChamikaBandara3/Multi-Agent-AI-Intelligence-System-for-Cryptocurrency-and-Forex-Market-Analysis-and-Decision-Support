from typing import Dict, Any
from agents.state import AgentState
from utils.binance_client import get_crypto_market_analysis
from utils.forex_client import get_forex_market_analysis
from config import ASSETS

def market_data_agent(state: AgentState) -> Dict[str, Any]:
    """
    Agent 1: Market Data Agent
    Role: Fetches live price action and computes technical indicator suite.
    Pattern: Tool-Use Pattern.
    """
    asset = state["asset"]
    asset_info = ASSETS.get(asset, {"type": "crypto", "symbol": asset})
    asset_type = asset_info["type"]
    symbol = asset_info["symbol"]
    
    if asset_type == "crypto":
        ticker, indicators, df = get_crypto_market_analysis(symbol)
    else:
        ticker, indicators, df = get_forex_market_analysis(symbol)
        
    log_msg = {
        "agent": "Agent 1: Market Data Agent",
        "action": f"Executed market tool on {asset} ({asset_type.upper()})",
        "details": f"Price: ${ticker['price']:,.2f} | RSI: {indicators['rsi']} ({indicators['rsi_status']}) | Trend: {indicators['trend_summary']}"
    }
    
    existing_logs = state.get("agent_logs", [])
    
    return {
        "market_data": ticker,
        "technical_indicators": indicators,
        "agent_logs": existing_logs + [log_msg]
    }
