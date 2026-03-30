#!/usr/bin/env python3
"""
Crypto Leverage Trading Engine
Main entry point for the trading bot
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

from trading_engine.core.bot import TradingBot
from trading_engine.utils.config import load_config


async def main():
    """Main entry point for the trading bot"""
    logger.info("=" * 60)
    logger.info("🚀 Crypto Leverage Trading Engine Starting...")
    logger.info("=" * 60)

    # Load configuration
    config = load_config()

    # Initialize trading bot
    bot = TradingBot(config)

    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise
    finally:
        await bot.cleanup()
        logger.info("✅ Trading engine stopped")


if __name__ == "__main__":
    asyncio.run(main())
