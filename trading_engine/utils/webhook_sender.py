"""
Webhook sender for sending trading signals to Discord bot
"""

import os
import requests
from loguru import logger


def send_signal_to_discord(signal: dict) -> bool:
    """
    Send a trading signal to the Discord bot via webhook
    
    Args:
        signal: Dict containing signal data with keys:
            - symbol: str
            - direction: 'long' or 'short'
            - entry_price: float
            - stop_loss: float
            - take_profit: float
            - leverage: float
            - indicator: str
            - confidence: float
    
    Returns:
        bool: True if successful, False otherwise
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    webhook_secret = os.getenv("WEBHOOK_SECRET")
    
    if not webhook_url:
        logger.warning("DISCORD_WEBHOOK_URL not configured - skipping signal send")
        return False
    
    try:
        # Build the signal payload
        payload = {
            "symbol": signal["symbol"],
            "direction": signal["direction"],
            "entryPrice": signal["entry_price"],
            "stopLoss": signal["stop_loss"],
            "takeProfit": signal["take_profit"],
            "leverage": signal["leverage"],
            "indicator": signal.get("indicator", "N/A"),
            "confidence": signal.get("confidence", 0.5),
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if webhook_secret:
            headers["X-Webhook-Secret"] = webhook_secret
        
        # Send POST request to Discord bot webhook
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"✅ Signal sent to Discord: {signal['symbol']} {signal['direction'].upper()}")
            return True
        else:
            logger.error(f"❌ Failed to send signal: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error sending signal to Discord: {e}")
        return False


def send_bulk_signals(signals: list) -> int:
    """
    Send multiple trading signals to Discord
    
    Args:
        signals: List of signal dicts
    
    Returns:
        int: Number of successfully sent signals
    """
    success_count = 0
    for signal in signals:
        if send_signal_to_discord(signal):
            success_count += 1
    return success_count
