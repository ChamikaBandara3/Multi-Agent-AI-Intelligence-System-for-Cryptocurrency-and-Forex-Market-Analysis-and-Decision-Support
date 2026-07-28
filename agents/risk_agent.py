from typing import Dict, Any
from agents.state import AgentState

def risk_management_agent(state: AgentState) -> Dict[str, Any]:
    """
    Agent 4: Risk Management Agent
    Role: Calculates ATR Volatility, Risk Rating (1-5 Stars), Stop Loss, and Take Profit.
    Pattern: Reflection & Critique Pattern.
    """
    asset = state["asset"]
    market_data = state.get("market_data", {})
    indicators = state.get("technical_indicators", {})
    sentiment = state.get("sentiment_data", {})
    
    current_price = market_data.get("price", 100.0)
    atr = indicators.get("atr", current_price * 0.015)
    trend = indicators.get("trend_summary", "Neutral")
    rsi = indicators.get("rsi", 50)
    fng = sentiment.get("fear_greed_index", 50)
    
    # Calculate Dynamic Stop Loss & Take Profit based on ATR (Volatility multiplier)
    if trend == "Bullish":
        stop_loss = current_price - (1.5 * atr)
        take_profit = current_price + (3.0 * atr)
    elif trend == "Bearish":
        stop_loss = current_price + (1.5 * atr)
        take_profit = current_price - (3.0 * atr)
    else: # Neutral
        stop_loss = current_price - (1.2 * atr)
        take_profit = current_price + (2.0 * atr)
        
    # Calculate Risk Score (1 to 5 Stars)
    risk_score = 3 # Default Moderate
    risk_factors = []
    
    if rsi > 70 or rsi < 30:
        risk_score += 1
        risk_factors.append("Extreme RSI levels (High reversal volatility risk)")
        
    if fng > 80:
        risk_score += 1
        risk_factors.append("Extreme Market Greed (Correction danger)")
        
    if abs(market_data.get("price_change_percent", 0)) > 5.0:
        risk_score += 1
        risk_factors.append("High 24-hour price volatility")
        
    risk_score = min(5, max(1, risk_score))
    
    risk_labels = {
        1: "Low Risk",
        2: "Low-Moderate Risk",
        3: "Moderate Risk",
        4: "High Risk",
        5: "Extreme High Risk"
    }
    
    risk_rating_stars = "⭐" * risk_score + "☆" * (5 - risk_score)
    
    log_msg = {
        "agent": "Agent 4: Risk Management Agent",
        "action": f"Calculated Dynamic Risk Parameters for {asset}",
        "details": f"Risk Rating: {risk_rating_stars} ({risk_labels[risk_score]}) | Stop Loss: ${stop_loss:,.2f} | Take Profit: ${take_profit:,.2f}"
    }
    
    existing_logs = state.get("agent_logs", [])
    
    return {
        "risk_assessment": {
            "risk_score": risk_score,
            "risk_rating_stars": risk_rating_stars,
            "risk_label": risk_labels[risk_score],
            "recommended_stop_loss": round(stop_loss, 2),
            "recommended_take_profit": round(take_profit, 2),
            "risk_reward_ratio": "1:2.0",
            "volatility_atr": atr,
            "risk_warnings": risk_factors if risk_factors else ["Market conditions within standard volatility bounds"]
        },
        "agent_logs": existing_logs + [log_msg]
    }
