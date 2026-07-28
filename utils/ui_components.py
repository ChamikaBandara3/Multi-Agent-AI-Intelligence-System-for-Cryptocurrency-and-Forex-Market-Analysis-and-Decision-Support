import streamlit as st
import streamlit.components.v1 as components

def inject_custom_css():
    """Injects custom CSS styling for dark glassmorphism design."""
    st.markdown("""
    <style>
    /* Dark Glassmorphic Theme Styling */
    .stApp {
        background-color: #0B0E14;
        color: #E6E8EC;
    }
    
    .glass-card {
        background: rgba(21, 25, 34, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #00F0FF;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-title {
        font-size: 14px;
        color: #8A92A6;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .badge-buy {
        background-color: rgba(0, 230, 118, 0.15);
        color: #00E676;
        border: 1px solid #00E676;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 18px;
        display: inline-block;
    }
    
    .badge-sell {
        background-color: rgba(255, 23, 68, 0.15);
        color: #FF1744;
        border: 1px solid #FF1744;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 18px;
        display: inline-block;
    }
    
    .badge-hold {
        background-color: rgba(255, 171, 0, 0.15);
        color: #FFAB00;
        border: 1px solid #FFAB00;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 18px;
        display: inline-block;
    }
    
    .agent-box {
        border-left: 4px solid #00F0FF;
        background: rgba(255, 255, 255, 0.03);
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_tradingview_chart(symbol: str = "BINANCE:BTCUSDT", height: int = 450):
    """Embeds live interactive TradingView Widget."""
    html_code = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:{height}px;width:100%;">
      <div id="tradingview_chart" style="height:calc(100% - 32px);width:100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{symbol}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    components.html(html_code, height=height)

def render_metric_card(title: str, value: str, subtext: str = "", delta_color: str = "#00F0FF"):
    """Renders styled metric card."""
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {delta_color};">{value}</div>
        <div style="font-size: 12px; color: #8A92A6; margin-top: 4px;">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)
