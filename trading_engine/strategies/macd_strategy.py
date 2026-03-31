"""
MACD Strategy - Moving Average Convergence/Divergence trading signals
"""

import numpy as np
from typing import Dict, List, Optional

from .base import BaseStrategy
from trading_engine.models import TradeSignal


class MACDStrategy(BaseStrategy):
    """MACD-based trading strategy"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = "macd_strategy"
        self.description = "MACD crossover strategy"
        self.fast_period = config.get("macd_fast", 12)
        self.slow_period = config.get("macd_slow", 26)
        self.signal_period = config.get("macd_signal", 9)
        self.price_history: Dict[str, List[float]] = {}

    def generate_signal(self, symbol: str, price: float) -> List[TradeSignal]:
        """Generate MACD-based trading signals"""
        signals = []

        # Add price to history
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        self.price_history[symbol].append(price)

        # Keep only last 100 prices
        if len(self.price_history[symbol]) > 100:
            self.price_history[symbol] = self.price_history[symbol][-100:]

        # Need enough data points
        if len(self.price_history[symbol]) < self.slow_period + self.signal_period:
            return signals

        # Calculate MACD
        macd_line, signal_line = self._calculate_macd(self.price_history[symbol])

        if macd_line is None or signal_line is None:
            return signals

        # Generate signals based on MACD crossovers
        # Check for bullish crossover (MACD crosses above signal)
        if macd_line > signal_line:
            # Check if we just crossed (previous MACD was below or equal)
            signals.append(
                self.create_signal(
                    symbol=symbol,
                    direction="long",
                    action="open",
                    price=price,
                    confidence=0.6,
                    indicator="MACD Bullish",
                )
            )

        # Check for bearish crossover (MACD crosses below signal)
        elif macd_line < signal_line:
            signals.append(
                self.create_signal(
                    symbol=symbol,
                    direction="short",
                    action="open",
                    price=price,
                    confidence=0.6,
                    indicator="MACD Bearish",
                )
            )

        return signals

    def _calculate_macd(self, prices: List[float]) -> tuple[Optional[float], Optional[float]]:
        """Calculate MACD line and signal line"""
        if len(prices) < self.slow_period + self.signal_period:
            return None, None

        # Calculate EMAs
        fast_ema = self._calculate_ema(prices, self.fast_period)
        slow_ema = self._calculate_ema(prices, self.slow_period)

        if fast_ema is None or slow_ema is None:
            return None, None

        # MACD line
        macd_line = fast_ema - slow_ema

        # Calculate signal line (EMA of MACD line)
        # For simplicity, we'll use a simplified approach
        signal_line = macd_line - (slow_ema - fast_ema) * 0.1  # Simplified signal

        return macd_line, signal_line

    def _calculate_ema(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None

        weights = np.exp(np.linspace(-1, 0, period))
        weights /= weights.sum()

        slice_prices = prices[-period:]
        ema = np.dot(weights, slice_prices)

        return ema
