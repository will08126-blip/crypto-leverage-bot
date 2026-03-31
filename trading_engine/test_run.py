#!/usr/bin/env python3
"""
Quick test of trading engine functionality
"""

import sys
from pathlib import Path

# Add trading_engine to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trading_engine.utils.config import load_config
from trading_engine.core.exchange import ExchangeManager

async def test_exchange():
    """Test exchange connection"""
    config = load_config()
    print(f"Exchange: {config.get('exchange')}")
    print(f"Paper trading: {config.get('paper_trading')}")
    print(f"Symbols: {config.get('symbols')}")

    exchange_mgr = ExchangeManager(config)
    await exchange_mgr.connect()

    # Try to get prices
    prices = await exchange_mgr.get_prices()
    print(f"Prices: {prices}")

    await exchange_mgr.cleanup()
    print("✅ Test completed successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_exchange())
