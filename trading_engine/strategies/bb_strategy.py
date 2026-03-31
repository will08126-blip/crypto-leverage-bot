"""
Bollinger Bands Strategy - Volatility-based trading signals
"""

import numpy as np
from typing import Dict, List, Optional

from .base import BaseStrategy
from trading_engine.models import TradeSignal


class BBStrategy(BaseStrategy):
    """Bollinger Bands-based trading strategy"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = "bb_strategy"
        self.description = "Bollinger Bands breakout strategy"
        self.period = config.get("bb_period", 20)
        self.std_dev = config.get("bb_std", 2.0)
        self.price_history: Dict[str, List[float]] = {}

    def generate_signal(self, symbol: str, price: float) -> List[TradeSignal]:
        """Generate Bollinger Bands-based trading signals"""
        signals = []

        # Add price to history
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        self.price_history[symbol].append(price)

        # Keep only last 100 prices
        if len(self.price_history[symbol]) > 100:
            self.price_history[symbol] = self.price_history[symbol][-100:]

        # Need enough data points
        if len(self.price_history[symbol]) < self.period:
            return signals

        # Calculate Bollinger Bands
        upper_band, middle_band, lower_band = self._calculate_bb(self.price_history[symbol])

        if upper_band is None or middle_band is None or lower_band is None:
            return signals

        # Generate signals
        # Buy signal: Price touches or breaks below lower band (oversold)
        if price <= lower_band:
            signals.append(
                self.create_signal(
                    symbol=symbol,
                    direction="long",
                    action="open",
                    price=price,
                    confidence=0.65,
                    indicator=f"BB Oversold (Price: {price:.2f}, Lower: {lower_band:.2f})",
                )
            )

        # Sell signal: Price touches or breaks above upper band (overbought)
        elif price >= upper_band:
            signals.append(
                self.create_signal(
                    symbol=symbol,
                    direction="short",
                    action="open",
                    price=price,
                    confidence=0.65,
                    indicator=f"BB Overbought (Price: {price:.2f}, Upper: {upper_band:.2f})",
                )
            )

        return signals

    def _calculate_bb(self, prices: List[float]) -> tuple[Optional[float], Optional[float], Optional[float]]:
        """Calculate Bollinger Bands"""
        if len(prices) < self.period:
            return None, None, None

        # Calculate SMA (Simple Moving Average)
        slice_prices = prices[-self.period:]
        sma = np.mean(slice_prices)

        # Calculate standard deviation
        std = np.std(slice_prices)

        # Calculate bands
        upper_band = sma + (self.std_dev * std)
        lower_band = sma - (self.std_dev * std)

        return upper_band, sma, lower_band
