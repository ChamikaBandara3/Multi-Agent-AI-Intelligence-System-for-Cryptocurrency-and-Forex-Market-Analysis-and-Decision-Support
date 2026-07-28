import os
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'\"")
    except Exception:
        pass

def get_secret(key_name: str, default: str = "") -> str:
    """Retrieve secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            return str(st.secrets[key_name])
    except Exception:
        pass
    
    return os.getenv(key_name, default)

# Model & Provider Configuration
GROQ_API_KEY = get_secret("GROQ_API_KEY")
OPENROUTER_API_KEY = get_secret("OPENROUTER_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

# Default Selected Models for Sub-tasks
MODEL_INTENT_ROUTER = "llama-3.1-8b-instant"     # Groq fast routing
MODEL_NEWS_SENTIMENT = "llama-3.3-70b-versatile" # Groq high NLP accuracy
MODEL_DEEP_REASONING = "openai/gpt-4o-mini"      # OpenRouter / OpenAI deep synthesis
MODEL_RAG_QA = "gemini-2.5-flash"                # Grounded QA synthesis

# Vector DB & Storage Paths
CHROMA_DB_DIR = str(BASE_DIR / "db" / "chroma_db")
CORPUS_DIR = str(BASE_DIR / "rag" / "corpus")
SQLITE_DB_PATH = str(BASE_DIR / "db" / "history.db")

# Supported Trading Assets
ASSETS = {
    "BTCUSDT": {"type": "crypto", "symbol": "BTCUSDT", "name": "Bitcoin / USDT", "tv_symbol": "BINANCE:BTCUSDT"},
    "ETHUSDT": {"type": "crypto", "symbol": "ETHUSDT", "name": "Ethereum / USDT", "tv_symbol": "BINANCE:ETHUSDT"},
    "SOLUSDT": {"type": "crypto", "symbol": "SOLUSDT", "name": "Solana / USDT", "tv_symbol": "BINANCE:SOLUSDT"},
    "EUR/USD": {"type": "forex", "symbol": "EURUSD=X", "name": "Euro / US Dollar", "tv_symbol": "FX:EURUSD"},
    "GBP/USD": {"type": "forex", "symbol": "GBPUSD=X", "name": "British Pound / US Dollar", "tv_symbol": "FX:GBPUSD"},
    "USD/JPY": {"type": "forex", "symbol": "USDJPY=X", "name": "US Dollar / Japanese Yen", "tv_symbol": "FX:USDJPY"},
    "Gold (XAU/USD)": {"type": "commodity", "symbol": "GC=F", "name": "Gold / US Dollar", "tv_symbol": "OANDA:XAUUSD"},
    "NAS100": {"type": "index", "symbol": "^NDX", "name": "Nasdaq 100 Index", "tv_symbol": "CAPITALCOM:US100"},
}

def call_groq_llm(prompt: str, model: str = MODEL_NEWS_SENTIMENT, system_prompt: str = "") -> str:
    """Call Groq API directly using urllib REST call."""
    key = GROQ_API_KEY
    if not key:
        return ""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    body = json.dumps({"model": model, "messages": messages, "temperature": 0.3}).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API call error: {e}")
        return ""

def call_openrouter_llm(prompt: str, model: str = MODEL_DEEP_REASONING, system_prompt: str = "") -> str:
    """Call OpenRouter API directly using urllib REST call."""
    key = OPENROUTER_API_KEY
    if not key:
        return ""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "User-Agent": "Mozilla/5.0"
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    body = json.dumps({"model": model, "messages": messages, "temperature": 0.3}).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenRouter API call error: {e}")
        return ""
