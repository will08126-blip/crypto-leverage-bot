"""Trading models and data structures"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """Represents an open trading position"""
    symbol: str
    side: str  # 'long' or 'short'
    entry_price: float
    size: float
    leverage: float
    timestamp: datetime
    pnl: Optional[float] = None

    def update_pnl(self, current_price: float) -> None:
        """Update PnL based on current price"""
        if self.side == "long":
            self.pnl = (current_price - self.entry_price) / self.entry_price
        else:
            self.pnl = (self.entry_price - current_price) / self.entry_price
        self.pnl = self.pnl * self.size * self.leverage

    def __str__(self):
        pnl_str = f" PnL: {self.pnl:.2f}" if self.pnl is not None else ""
        return f"{self.symbol} {self.side.upper()} | Entry: {self.entry_price} | Size: {self.size} | Lev: {self.leverage}x{pnl_str}"


@dataclass
class TradeSignal:
    """Represents a trading signal"""
    symbol: str
    action: str  # 'open' or 'close'
    direction: str  # 'long' or 'short'
    price: float
    timestamp: datetime
    indicator: Optional[str] = None
    confidence: Optional[float] = None

    def __str__(self):
        return f"{self.symbol} {self.direction.upper()} | Action: {self.action} | Price: {self.price} | Indicator: {self.indicator}"
