#!/usr/bin/env python3
"""
Test Kraken exchange connectivity and real price fetching
"""

import sys
from pathlib import Path

# Add trading_engine to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import ccxt
import asyncio

async def test_kraken():
    """Test Kraken exchange connection"""
    print("Testing Kraken exchange connectivity...")

    # Initialize Kraken exchange
    exchange = ccxt.kraken({
        "enableRateLimit": True,
    })

    try:
        # Load markets
        print("Loading markets...")
        await asyncio.to_thread(exchange.load_markets)
        print(f"✅ Markets loaded: {len(exchange.markets)} markets available")

        # Test fetching tickers for our symbols
        symbols = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "DOGE/USD"]
        print(f"\nFetching prices for: {symbols}")

        for symbol in symbols:
            try:
                ticker = await asyncio.to_thread(exchange.fetch_ticker, symbol)
                price = ticker["last"]
                print(f"  {symbol}: ${price:,.2f}")
            except Exception as e:
                print(f"  {symbol}: ❌ Error - {e}")

        # Try bulk fetch
        print("\nFetching all tickers at once...")
        tickers = await asyncio.to_thread(exchange.fetch_tickers)
        print(f"✅ Successfully fetched {len(tickers)} tickers")

        # Show some prices
        print("\nSample prices:")
        for symbol, ticker in list(tickers.items())[:10]:
            print(f"  {symbol}: ${ticker['last']:,.2f}")

        print("\n✅ Kraken exchange test PASSED - real data available!")
        return True

    except Exception as e:
        print(f"\n❌ Kraken exchange test FAILED: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_kraken())
    sys.exit(0 if result else 1)
