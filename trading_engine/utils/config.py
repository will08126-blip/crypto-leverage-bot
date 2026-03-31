"""
Configuration loading utilities
"""

import os
from typing import Dict

from dotenv import load_dotenv


def load_config() -> Dict:
    """Load configuration from environment and defaults"""
    load_dotenv()

    config = {
        # Exchange configuration
        "exchange": os.getenv("EXCHANGE", "kraken"),
        "paper_trading": os.getenv("PAPER_TRADING", "true").lower() == "true",

        # Trading parameters
        "leverage": int(os.getenv("LEVERAGE", "10")),
        "risk_per_trade": float(os.getenv("RISK_PER_TRADE", "0.01")),
        "stop_loss": float(os.getenv("STOP_LOSS", "0.02")),
        "take_profit": float(os.getenv("TAKE_PROFIT", "0.04")),
        "max_positions": int(os.getenv("MAX_POSITIONS", "3")),

        # Trading intervals
        "interval": int(os.getenv("INTERVAL", "1")),

        # Strategies to use
        "strategies": ["rsi_strategy", "macd_strategy", "bb_strategy"],

        # RSI Strategy settings
        "rsi_period": int(os.getenv("RSI_PERIOD", "14")),
        "rsi_overbought": float(os.getenv("RSI_OVERBOUGHT", "70")),
        "rsi_oversold": float(os.getenv("RSI_OVERSOLD", "30")),

        # MACD Strategy settings
        "macd_fast": int(os.getenv("MACD_FAST", "12")),
        "macd_slow": int(os.getenv("MACD_SLOW", "26")),
        "macd_signal": int(os.getenv("MACD_SIGNAL", "9")),

        # BB Strategy settings
        "bb_period": int(os.getenv("BB_PERIOD", "20")),
        "bb_std": float(os.getenv("BB_STD", "2.0")),

        # Symbols to trade (Kraken format: BTC/USD, ETH/USD, etc.)
        "symbols": os.getenv("SYMBOLS", "BTC/USD,ETH/USD,SOL/USD,XRP/USD,DOGE/USD").split(","),

        # Discord integration
        "discord_webhook": os.getenv("DISCORD_WEBHOOK_URL"),
        "discord_channel_id": os.getenv("DISCORD_CHANNEL_ID"),
    }

    return config
