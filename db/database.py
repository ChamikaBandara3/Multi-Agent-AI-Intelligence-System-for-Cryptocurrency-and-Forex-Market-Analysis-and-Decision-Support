import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any
from config import SQLITE_DB_PATH

def init_db():
    """Initialize SQLite database for persisting analysis logs."""
    db_file = Path(SQLITE_DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        asset TEXT,
        price REAL,
        action TEXT,
        confidence INTEGER,
        risk_label TEXT,
        stop_loss REAL,
        take_profit REAL,
        rationale TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rag_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        question TEXT,
        sources TEXT,
        answer TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def save_analysis(asset: str, price: float, action: str, confidence: int, risk_label: str, stop_loss: float, take_profit: float, rationale: str):
    """Saves a multi-agent decision analysis record."""
    init_db()
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    INSERT INTO analysis_history (timestamp, asset, price, action, confidence, risk_label, stop_loss, take_profit, rationale)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (now_str, asset, price, action, confidence, risk_label, stop_loss, take_profit, rationale))
    
    conn.commit()
    conn.close()

def get_recent_analyses(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves recent saved analysis records."""
    init_db()
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM analysis_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
