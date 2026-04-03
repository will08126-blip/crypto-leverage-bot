"""
Base Strategy Class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from trading_engine.models import TradeSignal
from datetime import datetime


class BaseStrategy(ABC):
    """Abstract base class for all trading strategies"""

    def __init__(self, config: Dict):
        self.config = config
        self.name = "Base Strategy"
        self.description = "Base strategy class"
        self.state = {}  # Strategy state (e.g., previous signals)

    @abstractmethod
    def generate_signal(self, symbol: str, price: float) -> List[TradeSignal]:
        """Generate trading signals based on strategy logic"""
        pass

    def create_signal(
        self,
        symbol: str,
        direction: str,
        action: str,
        price: float,
        confidence: float = 0.5,
        indicator: Optional[str] = None,
    ) -> TradeSignal:
        """Helper method to create a trade signal"""
        return TradeSignal(
            symbol=symbol,
            direction=direction,
            action=action,
            price=price,
            timestamp=datetime.now(),
            indicator=indicator,
            confidence=confidence,
            strategy=self.name,
        )

    def should_close_position(self, symbol: str, current_price: float) -> bool:
        """Check if position should be closed based on strategy rules"""
        return False

    def get_state(self, symbol: str) -> Dict:
        """Get strategy state for a symbol"""
        return self.state.get(symbol, {})

    def update_state(self, symbol: str, state: Dict):
        """Update strategy state for a symbol"""
        self.state[symbol] = state
