"""
RSI Strategy - Relative Strength Index based trading signals
"""

import numpy as np
from typing import Dict, List

from .base import BaseStrategy
from trading_engine.models import TradeSignal


class RSIStrategy(BaseStrategy):
    """RSI-based trading strategy"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = "rsi_strategy"
        self.description = "RSI-based entry/exit strategy"
        self.period = config.get("rsi_period", 14)
        self.overbought = config.get("rsi_overbought", 70)
        self.oversold = config.get("rsi_oversold", 30)
        self.rsi_history: Dict[str, List[float]] = {}

    def generate_signal(self, symbol: str, price: float) -> List[TradeSignal]:
        """Generate RSI-based trading signals"""
        signals = []

        # Add price to history
        if symbol not in self.rsi_history:
            self.rsi_history[symbol] = []
        self.rsi_history[symbol].append(price)

        # Keep only last 100 prices
        if len(self.rsi_history[symbol]) > 100:
            self.rsi_history[symbol] = self.rsi_history[symbol][-100:]

        # Need at least period + 1 data points
        if len(self.rsi_history[symbol]) < self.period + 1:
            return signals

        # Calculate RSI
        rsi_value = self._calculate_rsi(self.rsi_history[symbol], self.period)

        # Generate signals based on RSI
        if rsi_value is not None:
            # Oversold condition - potential buy signal
            if rsi_value < self.oversold:
                signals.append(
                    self.create_signal(
                        symbol=symbol,
                        direction="long",
                        action="open",
                        price=price,
                        confidence=0.7,
                        indicator=f"RSI({rsi_value:.1f})",
                    )
                )
            # Overbought condition - potential sell signal
            elif rsi_value > self.overbought:
                signals.append(
                    self.create_signal(
                        symbol=symbol,
                        direction="short",
                        action="open",
                        price=price,
                        confidence=0.7,
                        indicator=f"RSI({rsi_value:.1f})",
                    )
                )

        return signals

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate RSI value from price history"""
        if len(prices) < period + 1:
            return None

        # Calculate price changes
        deltas = np.diff(prices)
        gains = np.maximum(deltas, 0)
        losses = np.abs(np.minimum(deltas, 0))

        # Calculate average gains and losses
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100.0

        # Calculate RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi
