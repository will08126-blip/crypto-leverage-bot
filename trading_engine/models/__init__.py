"""
Trading Models and Data Structures
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Position:
    """Represents an open trading position"""

    symbol: str
    side: str  # "long" or "short"
    entry_price: float
    size: float
    leverage: int
    timestamp: datetime
    pnl: float = 0.0

    def update_pnl(self, current_price: float):
        """Update PnL based on current price"""
        if self.side == "long":
            price_change = current_price - self.entry_price
        else:
            price_change = self.entry_price - current_price

        self.pnl = (price_change / self.entry_price) * self.size * self.leverage


@dataclass
class TradeSignal:
    """Represents a trading signal from a strategy"""

    symbol: str
    direction: str  # "long" or "short"
    action: str  # "open" or "close"
    price: float
    timestamp: datetime
    indicator: Optional[str] = None
    confidence: float = 0.5

    def __str__(self):
        return f"{self.action.upper()} {self.symbol} {self.direction} @ {self.price} (confidence: {self.confidence:.2f})"


@dataclass
class Trade:
    """Represents a completed trade"""

    symbol: str
    side: str
    entry_price: float
    exit_price: float
    size: float
    leverage: int
    entry_timestamp: datetime
    exit_timestamp: datetime
    pnl: float
    pnl_percent: float

    @property
    def is_profitable(self) -> bool:
        return self.pnl > 0


@dataclass
class AccountBalance:
    """Represents account balance information"""

    total: float
    available: float
    in_positions: float
    currency: str = "USDT"

    @property
    def used_percentage(self) -> float:
        return (self.in_positions / self.total * 100) if self.total > 0 else 0
