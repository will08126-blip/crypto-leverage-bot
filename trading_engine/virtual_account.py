"""
Virtual account for paper trading simulation
"""
from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime


@dataclass
class VirtualPosition:
    symbol: str
    side: str  # 'long' or 'short'
    entry_price: float
    size: float
    leverage: float
    timestamp: datetime
    pnl: Optional[float] = None

    def update_pnl(self, current_price: float) -> None:
        if self.side == "long":
            self.pnl = (current_price - self.entry_price) / self.entry_price
        else:
            self.pnl = (self.entry_price - current_price) / self.entry_price
        self.pnl = self.pnl * self.size * self.leverage

    def __str__(self):
        pnl_str = f" PnL: {self.pnl:.2f}" if self.pnl is not None else ""
        return f"{self.symbol} {self.side.upper()} | Entry: {self.entry_price} | Size: {self.size} | Lev: {self.leverage}x{pnl_str}"


class VirtualAccount:
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.positions: Dict[str, VirtualPosition] = {}
        self.trades = []  # history

    def open_position(self, symbol: str, side: str, entry_price: float, size: float, leverage: float) -> Optional[VirtualPosition]:
        """Open a new position if sufficient balance."""
        # Calculate required margin (size * entry_price / leverage)
        required_margin = (size * entry_price) / leverage
        if required_margin > self.balance:
            print(f"Insufficient balance: need {required_margin}, have {self.balance}")
            return None

        # Deduct margin from balance
        self.balance -= required_margin

        position = VirtualPosition(
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            size=size,
            leverage=leverage,
            timestamp=datetime.now(),
        )
        self.positions[symbol] = position
        return position

    def close_position(self, symbol: str, exit_price: float) -> Optional[float]:
        """Close position and return realized PnL."""
        if symbol not in self.positions:
            return None
        position = self.positions[symbol]
        position.update_pnl(exit_price)
        realized_pnl = position.pnl * position.size * position.leverage  # already includes size*leverage?
        # Actually position.pnl is already multiplied by size and leverage (see update_pnl)
        realized_pnl = position.pnl

        # Return margin + profit/loss to balance
        margin = (position.size * position.entry_price) / position.leverage
        self.balance += margin + realized_pnl

        # Record trade
        self.trades.append({
            "symbol": symbol,
            "side": position.side,
            "entry_price": position.entry_price,
            "exit_price": exit_price,
            "size": position.size,
            "leverage": position.leverage,
            "pnl": realized_pnl,
            "timestamp": datetime.now(),
        })
        del self.positions[symbol]
        return realized_pnl

    def get_balance(self) -> float:
        return self.balance

    def get_positions(self) -> Dict[str, VirtualPosition]:
        return self.positions

    def reset_balance(self, new_balance: float = 1000.0):
        """Reset account to new balance, close all positions."""
        self.positions.clear()
        self.balance = new_balance
        self.trades.clear()