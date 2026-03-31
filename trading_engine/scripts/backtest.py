#!/usr/bin/env python3
"""
Backtesting script for trading strategies
"""

import argparse
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

import pandas as pd
from loguru import logger

from trading_engine.models import TradeSignal
from trading_engine.core.strategy_manager import StrategyManager
from trading_engine.utils.config import load_config


async def run_backtest(
    strategy_name: str,
    symbol: str,
    timeframe: str = "1h",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    initial_capital: float = 10000.0,
) -> dict:
    """Run backtest for a specific strategy"""

    config = load_config()
    strategy_manager = StrategyManager(config)

    if strategy_name not in strategy_manager.strategies:
        logger.error(f"Strategy {strategy_name} not found")
        return {}

    strategy = strategy_manager.strategies[strategy_name]

    # Load historical data (in real implementation, fetch from exchange)
    # For now, we'll simulate some data
    logger.info(f"Running backtest for {strategy_name} on {symbol}")

    # Simulate historical data
    num_candles = 1000
    base_price = 50000.0
    prices = []
    current_price = base_price

    import random
    for _ in range(num_candles):
        # Simulate price movement
        change = random.uniform(-0.01, 0.01)
        current_price *= (1 + change)
        prices.append(current_price)

    # Run strategy on historical data
    signals: List[TradeSignal] = []
    positions = []
    trades = []

    for i, price in enumerate(prices):
        signal_list = strategy.generate_signal(symbol, price)
        if signal_list:
            signals.extend(signal_list)

    # Process signals into trades (simplified)
    capital = initial_capital
    position = None

    for signal in signals[:100]:  # Limit for demo
        if signal.action == "open" and position is None:
            # Open position
            position_size = capital * 0.1 / signal.price  # 10% of capital
            position = {
                "symbol": symbol,
                "direction": signal.direction,
                "entry_price": signal.price,
                "size": position_size,
                "timestamp": signal.timestamp,
            }
        elif signal.action == "close" and position is not None:
            # Close position
            pnl = (signal.price - position["entry_price"]) / position["entry_price"]
            if position["direction"] == "short":
                pnl = -pnl

            trades.append({
                "entry_price": position["entry_price"],
                "exit_price": signal.price,
                "pnl": pnl,
                "pnl_percent": pnl * 100,
            })
            position = None

    # Calculate statistics
    winning_trades = [t for t in trades if t["pnl"] > 0]
    losing_trades = [t for t in trades if t["pnl"] <= 0]

    total_pnl = sum(t["pnl"] for t in trades)
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0

    results = {
        "strategy": strategy_name,
        "symbol": symbol,
        "timeframe": timeframe,
        "total_trades": len(trades),
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "total_pnl_percent": total_pnl * 100,
        "final_capital": capital * (1 + total_pnl),
        "initial_capital": initial_capital,
    }

    return results


def main():
    parser = argparse.ArgumentParser(description="Run trading strategy backtest")
    parser.add_argument("--strategy", required=True, help="Strategy name to backtest")
    parser.add_argument("--symbol", default="BTC/USDT", help="Trading symbol")
    parser.add_argument("--timeframe", default="1h", help="Timeframe for data")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=10000.0, help="Initial capital")

    args = parser.parse_args()

    # Run backtest
    results = asyncio.run(
        run_backtest(
            strategy_name=args.strategy,
            symbol=args.symbol,
            timeframe=args.timeframe,
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital,
        )
    )

    # Print results
    print("\n" + "=" * 60)
    print("📊 BACKTEST RESULTS")
    print("=" * 60)
    print(f"Strategy: {results.get('strategy', 'N/A')}")
    print(f"Symbol: {results.get('symbol', 'N/A')}")
    print(f"Timeframe: {results.get('timeframe', 'N/A')}")
    print("-" * 60)
    print(f"Total Trades: {results.get('total_trades', 0)}")
    print(f"Winning Trades: {results.get('winning_trades', 0)}")
    print(f"Losing Trades: {results.get('losing_trades', 0)}")
    print(f"Win Rate: {results.get('win_rate', 0):.2f}%")
    print("-" * 60)
    print(f"Total PnL: ${results.get('total_pnl', 0):.2f}")
    print(f"Total PnL %: {results.get('total_pnl_percent', 0):.2f}%")
    print(f"Initial Capital: ${results.get('initial_capital', 0):.2f}")
    print(f"Final Capital: ${results.get('final_capital', 0):.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
