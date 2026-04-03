"""
Analysis and logging module for trading data
"""
import sqlite3
import datetime
from typing import Optional, Dict, List
from loguru import logger

class TradeLogger:
    def __init__(self, db_path: str = "trading_data.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                symbol TEXT,
                direction TEXT,
                action TEXT,
                price REAL,
                indicator TEXT,
                confidence REAL,
                strategy TEXT
            )
        ''')
        
        # Trades table (closed positions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_time DATETIME,
                exit_time DATETIME,
                symbol TEXT,
                direction TEXT,
                entry_price REAL,
                exit_price REAL,
                size REAL,
                leverage REAL,
                pnl REAL,
                duration REAL
            )
        ''')
        
        # Balance history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                balance REAL
            )
        ''')
        
        # Config changes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                key TEXT,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Analysis database initialized at {self.db_path}")
    
    def log_signal(self, signal):
        """Log a trading signal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO signals (timestamp, symbol, direction, action, price, indicator, confidence, strategy)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal.timestamp, signal.symbol, signal.direction, signal.action, signal.price,
              signal.indicator, signal.confidence, signal.strategy))
        conn.commit()
        conn.close()
    
    def log_trade(self, entry_time, exit_time, symbol, direction, entry_price, exit_price, size, leverage, pnl):
        """Log a completed trade"""
        duration = (exit_time - entry_time).total_seconds()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trades (entry_time, exit_time, symbol, direction, entry_price, exit_price, size, leverage, pnl, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry_time, exit_time, symbol, direction, entry_price, exit_price, size, leverage, pnl, duration))
        conn.commit()
        conn.close()
    
    def log_balance(self, balance: float):
        """Log current balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO balance_history (timestamp, balance)
            VALUES (?, ?)
        ''', (datetime.datetime.now(), balance))
        conn.commit()
        conn.close()
    
    def log_config_change(self, key: str, value):
        """Log a configuration change"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO config_changes (timestamp, key, value)
            VALUES (?, ?, ?)
        ''', (datetime.datetime.now(), key, str(value)))
        conn.commit()
        conn.close()
    
    def get_recent_signals(self, limit: int = 100) -> List[Dict]:
        """Get recent signals"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM signals ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_recent_trades(self, limit: int = 100) -> List[Dict]:
        """Get recent trades"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM trades ORDER BY entry_time DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_balance_history(self, limit: int = 1000) -> List[Dict]:
        """Get balance history"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM balance_history ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

# Global instance
trade_logger = TradeLogger()