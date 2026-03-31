"""
Strategy Manager - Manages and executes trading strategies
"""

import importlib
import inspect
from typing import Dict, List

from loguru import logger

from trading_engine.models import TradeSignal
from trading_engine.strategies.base import BaseStrategy


class StrategyManager:
    """Manages multiple trading strategies"""

    def __init__(self, config: Dict):
        self.config = config
        self.strategies: Dict[str, BaseStrategy] = {}

        # Load strategies from config
        self._load_strategies()

    def _load_strategies(self):
        """Load strategies from configuration"""
        strategies_config = self.config.get("strategies", ["rsi_strategy"])

        for strategy_name in strategies_config:
            try:
                # Import strategy module
                module = importlib.import_module(f"trading_engine.strategies.{strategy_name}")
                
                # Find strategy class
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseStrategy)
                        and obj != BaseStrategy
                    ):
                        # Instantiate strategy
                        strategy_instance = obj(self.config)
                        self.strategies[strategy_name] = strategy_instance
                        logger.info(f"Loaded strategy: {strategy_name}")
                        break

            except Exception as e:
                logger.error(f"Failed to load strategy {strategy_name}: {e}")

    def generate_signals(self, symbol: str, current_price: float) -> List[TradeSignal]:
        """Generate signals from all loaded strategies"""
        signals = []

        for strategy_name, strategy in self.strategies.items():
            try:
                # Generate signals for this symbol
                strategy_signals = strategy.generate_signal(symbol, current_price)
                if strategy_signals:
                    signals.extend(strategy_signals)
            except Exception as e:
                logger.error(f"Error in strategy {strategy_name}: {e}")

        return signals

    def get_strategy_info(self) -> Dict[str, str]:
        """Get information about loaded strategies"""
        return {
            name: strategy.description
            for name, strategy in self.strategies.items()
        }
