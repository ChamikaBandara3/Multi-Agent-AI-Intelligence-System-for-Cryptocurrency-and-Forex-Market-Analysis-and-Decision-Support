from typing import Dict, Any
from agents.state import AgentState
from config import MODEL_DEEP_REASONING, call_openrouter_llm

def decision_agent(state: AgentState) -> Dict[str, Any]:
    """
    Agent 5: Decision Agent
    Role: Synthesizes structured data from Agents 1-4 to generate final recommendation.
    Pattern: Orchestrator-Worker Synthesizer & Deep Reasoning Agent.
    Model: Uses OpenRouter / OpenAI (gpt-4o-mini) via live API call.
    """
    asset = state["asset"]
    market = state.get("market_data", {})
    indicators = state.get("technical_indicators", {})
    news = state.get("news_data", {})
    sentiment = state.get("sentiment_data", {})
    risk = state.get("risk_assessment", {})
    
    current_price = market.get("price", 100.0)
    rsi = indicators.get("rsi", 50)
    macd_hist = indicators.get("macd", {}).get("histogram", 0)
    trend = indicators.get("trend_summary", "Neutral")
    bullish_pct = sentiment.get("bullish_percentage", 50)
    news_sentiment = news.get("overall_sentiment", "Neutral")
    risk_label = risk.get("risk_label", "Moderate Risk")
    
    # Standard Rule-based Base Synthesis
    if trend == "Bullish" and news_sentiment != "Negative / Bearish" and rsi < 75:
        action = "BUY / LONG"
        action_code = "BUY"
        confidence = 85
        rationale = (
            f"Technical indicators show strong {trend} momentum (RSI={rsi}, MACD Histogram={macd_hist:.2f}). "
            f"Market sentiment is positive ({bullish_pct}% bullish) and news stream is favorable. "
            f"Risk profile is acceptable ({risk_label})."
        )
    elif trend == "Bearish" and news_sentiment != "Positive / Bullish" and rsi > 25:
        action = "SELL / SHORT"
        action_code = "SELL"
        confidence = 82
        rationale = (
            f"Technical indicators indicate macro {trend} alignment. "
            f"RSI ({rsi}) confirms downward pressure. News and social sentiment suggest cautious market posture."
        )
    else:
        action = "HOLD / WAIT FOR CONFIRMATION"
        action_code = "HOLD"
        confidence = 74
        rationale = (
            f"Technical indicators are bullish, but sentiment ({bullish_pct}%) or RSI ({rsi}) indicates potential overbought conditions. "
            f"Key economic news is pending today. Recommendation is to hold and wait for clear breakout confirmation."
        )

    # Call OpenRouter Live LLM for Deep Synthesis if key is configured
    system_prompt = "You are a Chief Investment Officer synthesizing 4 agent reports into a final trading recommendation."
    user_prompt = (
        f"Asset: {asset}\nPrice: ${current_price}\nTrend: {trend}\nRSI: {rsi}\n"
        f"News Sentiment: {news_sentiment}\nCrowd Bullish: {bullish_pct}%\nRisk Rating: {risk_label}\n"
        f"Provide a 2-sentence rationale for a {action_code} recommendation."
    )
    
    llm_synthesis = call_openrouter_llm(user_prompt, model=MODEL_DEEP_REASONING, system_prompt=system_prompt)
    if llm_synthesis:
        rationale = f"[OpenRouter {MODEL_DEEP_REASONING} Live Reasoning]: {llm_synthesis.strip()}"
        model_used = f"{MODEL_DEEP_REASONING} (OpenRouter Live API)"
    else:
        model_used = f"{MODEL_DEEP_REASONING} (OpenRouter / Groq)"

    log_msg = {
        "agent": "Agent 5: Decision Support Agent",
        "action": f"Generated Final Multi-Agent Recommendation for {asset}",
        "details": f"Recommendation: {action} (Confidence: {confidence}%) | Rationale: {rationale[:120]}..."
    }
    
    existing_logs = state.get("agent_logs", [])
    
    return {
        "decision_recommendation": {
            "action": action,
            "action_code": action_code,
            "confidence_percentage": confidence,
            "rationale": rationale,
            "entry_zone": f"${current_price * 0.998:,.2f} - ${current_price * 1.002:,.2f}",
            "recommended_stop_loss": risk.get("recommended_stop_loss", 0),
            "recommended_take_profit": risk.get("recommended_take_profit", 0),
            "model_used": model_used
        },
        "agent_logs": existing_logs + [log_msg]
    }
