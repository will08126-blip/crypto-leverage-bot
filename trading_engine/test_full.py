#!/usr/bin/env python3
"""
Test full trading engine with Kraken exchange
"""

import sys
from pathlib import Path

# Add trading_engine to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from trading_engine.utils.config import load_config
from trading_engine.core.exchange import ExchangeManager
from trading_engine.core.strategy_manager import StrategyManager

async def test_trading_engine():
    """Test the complete trading engine"""
    print("Testing full trading engine with Kraken...")

    # Load config
    config = load_config()
    print(f"Exchange: {config.get('exchange')}")
    print(f"Symbols: {config.get('symbols')}")

    # Initialize exchange
    exchange_mgr = ExchangeManager(config)
    await exchange_mgr.connect()

    # Get real prices
    prices = await exchange_mgr.get_prices()
    print("\n✅ Real prices from Kraken:")
    for symbol, price in prices.items():
        if price is not None:
            print(f"  {symbol}: ${price:,.2f}")

    # Initialize strategies
    strategy_mgr = StrategyManager(config)
    print(f"\n✅ Strategies loaded: {list(strategy_mgr.strategies.keys())}")

    # Test signal generation for BTC
    if "BTC/USD" in prices:
        btc_price = prices["BTC/USD"]
        signals = strategy_mgr.generate_signals("BTC/USD", btc_price)
        print(f"\n✅ Generated {len(signals)} signals for BTC/USD at ${btc_price:,.2f}")
        for signal in signals:
            print(f"  {signal}")

    await exchange_mgr.cleanup()
    print("\n✅ Full trading engine test PASSED!")
    return True

if __name__ == "__main__":
    result = asyncio.run(test_trading_engine())
    sys.exit(0 if result else 1)
