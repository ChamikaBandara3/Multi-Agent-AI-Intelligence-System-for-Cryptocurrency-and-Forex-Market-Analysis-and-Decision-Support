import streamlit as st
import pandas as pd
from config import ASSETS, MODEL_INTENT_ROUTER, MODEL_NEWS_SENTIMENT, MODEL_DEEP_REASONING, MODEL_RAG_QA

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Intelligence System | Crypto & Forex",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (inline, no heavy import) ─────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0B0E14; color: #E6E8EC; }
.glass-card {
    background: rgba(21, 25, 34, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.37);
}
.metric-value { font-size: 28px; font-weight: 700; color: #00F0FF; }
.metric-title { font-size: 13px; color: #8A92A6; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px; }
.badge-buy   { background: rgba(0,230,118,.15); color: #00E676; border: 1px solid #00E676; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 18px; }
.badge-sell  { background: rgba(255,23,68,.15);  color: #FF1744; border: 1px solid #FF1744; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 18px; }
.badge-hold  { background: rgba(255,171,0,.15);  color: #FFAB00; border: 1px solid #FFAB00; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 18px; }
.agent-box   { border-left: 4px solid #00F0FF; background: rgba(255,255,255,.03); padding: 12px 16px; margin-bottom: 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────
st.title("🤖 Multi-Agent AI Market Intelligence & Decision Support System")
st.caption("IT41043 Intelligent Systems (Agentic AI) | Autonomous 5-Agent Pipeline & RAG Knowledge Base")

# ── Sidebar ──────────────────────────────────────────
st.sidebar.header("🎯 Market Asset Selector")
selected_asset = st.sidebar.selectbox("Choose Trading Pair / Asset:", list(ASSETS.keys()), index=0)
asset_info = ASSETS[selected_asset]
tv_symbol = asset_info["tv_symbol"]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Multi-Model Strategy Routing")
st.sidebar.markdown(f"""
- **Intent Router**: `{MODEL_INTENT_ROUTER}` (Groq)
- **News NLP**: `{MODEL_NEWS_SENTIMENT}` (Groq)
- **Deep Synthesis**: `{MODEL_DEEP_REASONING}` (OpenRouter)
- **RAG QA**: `{MODEL_RAG_QA}` (Gemini / ChromaDB)
""")

analyze_btn = st.sidebar.button("🚀 Run 5-Agent Intelligence Pipeline", type="primary", use_container_width=True)

# ── Tabs ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Live Market & 5-Agent Decision Hub",
    "📚 RAG AI Trading Mentor",
    "📜 Analysis History Logs",
    "🧩 System Architecture & Rubric Info"
])

# ══════════════════════════════════════════════════════
# TAB 1 — MARKET ANALYSIS (only runs agents on button)
# ══════════════════════════════════════════════════════
with tab1:
    # TradingView chart always renders instantly
    st.subheader(f"📈 Live TradingView Chart — {selected_asset}")
    import streamlit.components.v1 as components
    tv_html = f"""
    <div style="height:480px;width:100%;">
      <div id="tv_chart" style="height:100%;width:100%;"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
      new TradingView.widget({{
        autosize: true, symbol: "{tv_symbol}", interval: "D",
        timezone: "Etc/UTC", theme: "dark", style: "1", locale: "en",
        enable_publishing: false, hide_side_toolbar: false,
        allow_symbol_change: true, container_id: "tv_chart"
      }});
      </script>
    </div>
    """
    components.html(tv_html, height=490)

    st.markdown("---")

    # If user clicked the button, run the pipeline
    if analyze_btn:
        with st.spinner(f"⏳ Running 5-Agent Intelligence Pipeline on **{selected_asset}**... Please wait."):
            from agents.workflow import run_market_intelligence_analysis
            result = run_market_intelligence_analysis(selected_asset)
            st.session_state["analysis_results"] = result
            st.session_state["analysis_asset"] = selected_asset
            # Save to SQLite
            from db.database import save_analysis
            dec = result.get("decision_recommendation", {})
            rsk = result.get("risk_assessment", {})
            mkt = result.get("market_data", {})
            save_analysis(
                asset=selected_asset,
                price=mkt.get("price", 0.0),
                action=dec.get("action_code", "HOLD"),
                confidence=dec.get("confidence_percentage", 70),
                risk_label=rsk.get("risk_label", "Moderate"),
                stop_loss=rsk.get("recommended_stop_loss", 0.0),
                take_profit=rsk.get("recommended_take_profit", 0.0),
                rationale=dec.get("rationale", "")
            )

    # Display results if available
    if "analysis_results" in st.session_state:
        res = st.session_state["analysis_results"]
        market   = res.get("market_data", {})
        ind      = res.get("technical_indicators", {})
        news     = res.get("news_data", {})
        sentiment = res.get("sentiment_data", {})
        risk     = res.get("risk_assessment", {})
        decision = res.get("decision_recommendation", {})
        logs     = res.get("agent_logs", [])

        # ── Metric Cards ──
        c1, c2, c3, c4, c5 = st.columns(5)
        pct = market.get('price_change_percent', 0)
        pct_color = "#00E676" if pct >= 0 else "#FF1744"
        with c1:
            st.markdown(f'<div class="glass-card"><div class="metric-title">Current Price</div><div class="metric-value" style="color:{pct_color}">${market.get("price",0):,.2f}</div><div style="font-size:12px;color:#8A92A6">24h: {pct:+.2f}%</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card"><div class="metric-title">Technical Trend</div><div class="metric-value">{ind.get("trend_summary","N/A")}</div><div style="font-size:12px;color:#8A92A6">RSI: {ind.get("rsi",50)} ({ind.get("rsi_status","Neutral")})</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="glass-card"><div class="metric-title">Fear & Greed</div><div class="metric-value">{sentiment.get("fear_greed_index",50)}/100</div><div style="font-size:12px;color:#8A92A6">{sentiment.get("fear_greed_label","Neutral")}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="glass-card"><div class="metric-title">Risk Level</div><div class="metric-value">{risk.get("risk_rating_stars","N/A")}</div><div style="font-size:12px;color:#8A92A6">{risk.get("risk_label","Moderate")}</div></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="glass-card"><div class="metric-title">News Sentiment</div><div class="metric-value">{news.get("impact_score",50)}%</div><div style="font-size:12px;color:#8A92A6">{news.get("overall_sentiment","Neutral")}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Final Recommendation Card ──
        act_code = decision.get("action_code", "HOLD")
        badge = "badge-buy" if act_code == "BUY" else ("badge-sell" if act_code == "SELL" else "badge-hold")

        st.subheader("💡 Final AI Decision Recommendation")
        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="{badge}">{decision.get('action','HOLD')}</span>
                <span style="font-size:18px;font-weight:700;color:#00F0FF;">Confidence: {decision.get('confidence_percentage',75)}%</span>
            </div>
            <p style="font-size:14px;line-height:1.6;color:#E6E8EC;"><strong>Synthesis Rationale:</strong><br>{decision.get('rationale','')}</p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="display:flex;justify-content:space-between;font-size:14px;">
                <div>🎯 <strong>Entry Zone:</strong> {decision.get('entry_zone','N/A')}</div>
                <div>🛑 <strong>Stop Loss:</strong> ${risk.get('recommended_stop_loss',0):,.2f}</div>
                <div>✅ <strong>Take Profit:</strong> ${risk.get('recommended_take_profit',0):,.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Agent Execution Log ──
        st.subheader("🕵️ Agent-to-Agent Message Execution Flow")
        for log in logs:
            st.markdown(f"""
            <div class="agent-box">
                <strong style="color:#00F0FF;">{log['agent']}</strong> — <em>{log['action']}</em><br>
                <span style="font-size:12px;color:#A0AABF;">{log['details']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Select an asset from the sidebar and click **'🚀 Run 5-Agent Intelligence Pipeline'** to begin analysis.")

# ══════════════════════════════════════════════════════
# TAB 2 — RAG KNOWLEDGE BASE (only queries on button)
# ══════════════════════════════════════════════════════
with tab2:
    st.header("📚 RAG Knowledge Base Chatbot")
    st.caption("Ask questions about Trading Strategies, Technical Indicators, Risk Management & Market Psychology.")
    st.info("💡 Answers are strictly grounded in 21 ingested domain-specific trading documents (ChromaDB + LangChain).")

    user_query = st.text_input("Ask Trading Mentor Question:", placeholder="e.g. What is MACD Divergence?")
    ask_btn = st.button("🔍 Query Knowledge Base", type="primary")

    if ask_btn and user_query:
        with st.spinner("Searching ChromaDB Knowledge Base & generating grounded answer..."):
            from rag.retriever import rag_engine
            rag_res = rag_engine.query(user_query)

        st.markdown("### Answer")
        st.markdown(rag_res["answer"])

        with st.expander("📄 Retrieved Context Chunks & Cited Sources"):
            st.write("**Source Documents Used:**", rag_res["sources"])
            st.text_area("Retrieved Raw Text Snippet:", rag_res["context_sample"], height=180)
    elif ask_btn and not user_query:
        st.warning("Please type a question before clicking Query.")

# ══════════════════════════════════════════════════════
# TAB 3 — ANALYSIS HISTORY (SQLite)
# ══════════════════════════════════════════════════════
with tab3:
    st.header("📜 Past Market Analysis Logs (SQLite DB)")
    from db.database import get_recent_analyses
    records = get_recent_analyses(20)
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No saved analysis logs yet. Run the 5-Agent pipeline to generate entries.")

# ══════════════════════════════════════════════════════
# TAB 4 — ARCHITECTURE & RUBRIC INFO
# ══════════════════════════════════════════════════════
with tab4:
    st.header("🧩 IT41043 Assignment Rubric & System Architecture")

    st.markdown("""
### 1. Agentic Design Patterns Implemented (≥3 Required)
- **Orchestrator-Worker Pattern**: Agent 5 (Decision Agent) orchestrates inputs from 4 specialized worker agents.
- **Tool-Use Pattern**: Market Data Agent invokes Binance REST API & Technical Analysis math engines.
- **Planning & Task Decomposition**: LangGraph StateGraph decomposes comprehensive analysis into distinct parallel state nodes.
- **Router Pattern**: Query Intent Router splits live market analysis execution vs RAG knowledge retrieval.
- **Reflection & Self-Critique Pattern**: Risk Agent critiques signals against ATR volatility & stop-loss rules.

### 2. Multi-Model Strategy Table (Groq & OpenRouter)
    """)

    model_data = [
        {"Sub-Task": "Intent Routing & Classification", "Model": "llama-3.1-8b-instant (Groq)", "Latency": "~150ms", "Cost": "Near-Free", "Justification": "Ultra-fast execution with zero bottleneck."},
        {"Sub-Task": "News & Text Sentiment", "Model": "llama-3.3-70b-versatile (Groq)", "Latency": "~400ms", "Cost": "Low", "Justification": "High NLP extraction precision for headlines."},
        {"Sub-Task": "Deep Reasoning & Final Synthesis", "Model": "gpt-4o-mini (OpenRouter)", "Latency": "~1.0s", "Cost": "Balanced", "Justification": "Complex multi-agent reasoning synthesis."},
        {"Sub-Task": "RAG Knowledge Base QA", "Model": "gemini-2.5-flash / HuggingFace", "Latency": "~350ms", "Cost": "Low", "Justification": "Accurate grounding with source document citations."}
    ]
    st.table(pd.DataFrame(model_data))

    st.markdown("""
### 3. RAG Corpus Details
- **Total Documents Ingested**: 21 Trading Guides (Markdown in `rag/corpus/`)
- **Chunking Strategy**: `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=150)
- **Vector Database**: `ChromaDB` (Persisted locally in `db/chroma_db`)
- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
    """)
