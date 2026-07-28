from typing import Dict, Any
from agents.state import AgentState
from agents.market_agent import market_data_agent
from agents.news_agent import news_intelligence_agent
from agents.sentiment_agent import sentiment_analysis_agent
from agents.risk_agent import risk_management_agent
from agents.decision_agent import decision_agent

class NativeStateGraphWorkflow:
    """Native Python State Machine for 5-Agent Pipeline execution."""
    def __init__(self):
        self.nodes = {
            "market_agent": market_data_agent,
            "news_agent": news_intelligence_agent,
            "sentiment_agent": sentiment_analysis_agent,
            "risk_agent": risk_management_agent,
            "decision_agent": decision_agent,
        }
        
    def invoke(self, state: AgentState) -> AgentState:
        # Sequential State Pipeline Execution
        s1 = self.nodes["market_agent"](state)
        state.update(s1)
        
        s2 = self.nodes["news_agent"](state)
        state.update(s2)
        
        s3 = self.nodes["sentiment_agent"](state)
        state.update(s3)
        
        s4 = self.nodes["risk_agent"](state)
        state.update(s4)
        
        s5 = self.nodes["decision_agent"](state)
        state.update(s5)
        
        return state

def create_multi_agent_workflow():
    """Builds LangGraph StateGraph if available, or native StateMachine fallback."""
    try:
        from langgraph.graph import StateGraph, END
        workflow = StateGraph(AgentState)
        
        workflow.add_node("market_agent", market_data_agent)
        workflow.add_node("news_agent", news_intelligence_agent)
        workflow.add_node("sentiment_agent", sentiment_analysis_agent)
        workflow.add_node("risk_agent", risk_management_agent)
        workflow.add_node("decision_agent", decision_agent)
        
        workflow.set_entry_point("market_agent")
        workflow.add_edge("market_agent", "news_agent")
        workflow.add_edge("news_agent", "sentiment_agent")
        workflow.add_edge("sentiment_agent", "risk_agent")
        workflow.add_edge("risk_agent", "decision_agent")
        workflow.add_edge("decision_agent", END)
        
        return workflow.compile()
    except Exception:
        return NativeStateGraphWorkflow()

# Global compiled graph instance
multi_agent_app = create_multi_agent_workflow()

def run_market_intelligence_analysis(asset: str) -> Dict[str, Any]:
    """Helper execution function to trigger full 5-agent LangGraph analysis pipeline."""
    initial_state: AgentState = {
        "asset": asset,
        "asset_type": "crypto" if "USDT" in asset else "forex",
        "market_data": {},
        "technical_indicators": {},
        "news_data": {},
        "sentiment_data": {},
        "risk_assessment": {},
        "decision_recommendation": {},
        "agent_logs": []
    }
    
    result_state = multi_agent_app.invoke(initial_state)
    return result_state
