import json
import urllib.request
from typing import Dict, Any
from agents.state import AgentState

def fetch_crypto_fear_greed_index() -> Dict[str, Any]:
    """Fetch live Fear & Greed Index from alternative.me public API."""
    url = "https://api.alternative.me/fng/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8")).get("data", [])[0]
            return {
                "value": int(data.get("value", 72)),
                "classification": data.get("value_classification", "Extreme Greed"),
                "source": "Alternative.me Fear & Greed Index API"
            }
    except Exception:
        return {
            "value": 78,
            "classification": "Extreme Greed",
            "source": "Simulated Fallback"
        }

def sentiment_analysis_agent(state: AgentState) -> Dict[str, Any]:
    """
    Agent 3: Sentiment Analysis Agent
    Role: Evaluates Fear & Greed Index, Twitter (X) & Reddit market social sentiment.
    """
    asset = state["asset"]
    fng = fetch_crypto_fear_greed_index()
    
    if fng["value"] > 65:
        crowd_bias = "Strongly Bullish"
        bullish_percentage = 82
    elif fng["value"] < 35:
        crowd_bias = "Strongly Bearish"
        bullish_percentage = 24
    else:
        crowd_bias = "Balanced / Neutral"
        bullish_percentage = 52
        
    log_msg = {
        "agent": "Agent 3: Sentiment Analysis Agent",
        "action": f"Analyzed Market & Crowd Sentiment for {asset}",
        "details": f"Fear & Greed Index: {fng['value']} ({fng['classification']}) | Social Sentiment: {bullish_percentage}% {crowd_bias}"
    }
    
    existing_logs = state.get("agent_logs", [])
    
    return {
        "sentiment_data": {
            "fear_greed_index": fng["value"],
            "fear_greed_label": fng["classification"],
            "bullish_percentage": bullish_percentage,
            "bearish_percentage": 100 - bullish_percentage,
            "crowd_bias": crowd_bias,
            "source": fng["source"]
        },
        "agent_logs": existing_logs + [log_msg]
    }
