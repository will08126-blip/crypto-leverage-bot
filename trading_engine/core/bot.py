"""
Core Trading Bot Implementation
"""

import asyncio
import os
from typing import Dict, List, Optional

import ccxt
from loguru import logger

from trading_engine.models import Position, TradeSignal
from trading_engine.core.exchange import ExchangeManager
from trading_engine.core.strategy_manager import StrategyManager
from trading_engine.utils.webhook_sender import send_signal_to_discord
from trading_engine.analysis import trade_logger


class TradingBot:
    """Main trading bot class"""

    def __init__(self, config: Dict):
        self.config = config
        self.exchange_manager = ExchangeManager(config)
        self.strategy_manager = StrategyManager(config)
        self.positions: Dict[str, Position] = {}
        self.running = False
        
        # Virtual account for paper trading simulation
        from trading_engine.virtual_account import VirtualAccount
        initial_balance = float(config.get("initial_balance", 1000.0))
        self.virtual_account = VirtualAccount(initial_balance)
        logger.info(f"Trading bot initialized with config: {config.get('exchange', 'unknown')}")

    async def run(self):
        """Main trading loop"""
        self.running = True

        # Connect to exchange
        await self.exchange_manager.connect()

        # Start market data streaming
        await self.exchange_manager.start_streams()

        # Main trading loop
        while self.running:
            try:
                # Get latest market data
                await self._process_market_data()

                # Generate trading signals
                signals = await self._generate_signals()

                # Execute trades based on signals
                await self._execute_trades(signals)

                # Update positions
                await self._update_positions()

                # Sleep for next iteration
                await asyncio.sleep(self.config.get("interval", 1))

            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                await asyncio.sleep(5)

    async def _process_market_data(self):
        """Process incoming market data"""
        # This would fetch and process candlestick data, order book, etc.
        pass

    async def _generate_signals(self) -> List[TradeSignal]:
        """Generate trading signals from strategies"""
        signals = []
        # Get current prices
        prices = await self.exchange_manager.get_prices()
        
        # Filter symbols to only those configured
        allowed_symbols = set(self.config.get("symbols", []))
        
        # Collect signals per symbol per direction
        signal_counts = {}  # key: (symbol, direction), value: list of signals
        
        for symbol, price in prices.items():
            if symbol not in allowed_symbols:
                continue
            # Run strategies for this symbol
            strategy_signals = self.strategy_manager.generate_signals(symbol, price)
            for sig in strategy_signals:
                key = (sig.symbol, sig.direction)
                if key not in signal_counts:
                    signal_counts[key] = []
                signal_counts[key].append(sig)
        
        # Keep only signals where strategies agree (configurable)
        require_consensus = self.config.get("require_consensus", True)
        min_strategy_agreement = self.config.get("min_strategy_agreement", 2)
        
        for key, sig_list in signal_counts.items():
            # Decide whether to keep this signal
            keep = False
            if require_consensus:
                if len(sig_list) >= min_strategy_agreement:
                    keep = True
            else:
                # Keep any signal (even single strategy)
                keep = True
            
            if keep:
                # Average confidence
                avg_confidence = sum(s.confidence for s in sig_list) / len(sig_list)
                # Create a combined signal (use the first one as template)
                combined = TradeSignal(
                    symbol=sig_list[0].symbol,
                    direction=sig_list[0].direction,
                    action=sig_list[0].action,
                    price=sig_list[0].price,
                    timestamp=sig_list[0].timestamp,
                    indicator=f"Multiple({', '.join(s.strategy for s in sig_list)})" if len(sig_list) > 1 else sig_list[0].indicator,
                    confidence=avg_confidence,
                    strategy="combined" if len(sig_list) > 1 else sig_list[0].strategy,
                )
                signals.append(combined)
        
        return signals

    async def _execute_trades(self, signals: List[TradeSignal]):
        """Execute trades based on signals"""
        # Get minimum confidence threshold from config (default 0.5)
        min_confidence = self.config.get("min_confidence", 0.5)
        
        for signal in signals:
            if signal.action == "open":
                # Skip if position already exists
                if signal.symbol in self.positions:
                    continue
                # Skip if confidence below threshold
                if signal.confidence < min_confidence:
                    continue
                # await self._send_signal_to_discord(signal) # Disabled for now
                await self._open_position(signal)
            elif signal.action == "close":
                await self._close_position(signal.symbol)

    async def _open_position(self, signal: TradeSignal):
        """Open a new position"""
        try:
            # Check if we already have a position for this symbol
            if signal.symbol in self.positions:
                logger.warning(f"Position already exists for {signal.symbol}")
                return

            # Calculate position size based on risk management
            position_size = self._calculate_position_size(signal)

            # Execute order on exchange (or simulate)
            order = await self.exchange_manager.create_order(
                symbol=signal.symbol,
                side=signal.direction,
                size=position_size,
                leverage=self.config.get("leverage", 10),
            )

            if order:
                # Open position in virtual account (if simulating) first
                virtual_pos = None
                if hasattr(self, 'virtual_account'):
                    virtual_pos = self.virtual_account.open_position(
                        symbol=signal.symbol,
                        side=signal.direction,
                        entry_price=order["price"],
                        size=position_size,
                        leverage=self.config.get("leverage", 10),
                    )
                    if virtual_pos is None:
                        logger.warning("Virtual account rejected position (insufficient balance)")
                        return  # Do not open real position if virtual account rejects
                    else:
                        logger.info(f"Virtual position opened: {virtual_pos}")
                        # Log balance after opening position
                        trade_logger.log_balance(self.virtual_account.get_balance())
                
                # Store position (real) only if virtual account succeeded
                position = Position(
                    symbol=signal.symbol,
                    side=signal.direction,
                    entry_price=order["price"],
                    size=position_size,
                    leverage=self.config.get("leverage", 10),
                    timestamp=order["timestamp"],
                )
                self.positions[signal.symbol] = position
                logger.info(f"Opened position: {position}")

        except Exception as e:
            logger.error(f"Failed to open position for {signal.symbol}: {e}")

    async def _close_position(self, symbol: str):
        """Close an existing position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"No position found for {symbol}")
                return

            position = self.positions[symbol]
            side = "sell" if position.side == "long" else "buy"

            # Execute close order
            order = await self.exchange_manager.create_order(
                symbol=symbol,
                side=side,
                size=position.size,
                leverage=position.leverage,
                reduce_only=True,
            )

            if order:
                # Calculate PnL
                pnl = self._calculate_pnl(position, order["price"])
                logger.info(f"Closed position: {position} | PnL: {pnl}")
                
                # Log the trade completion
                from datetime import datetime
                trade_logger.log_trade(
                    entry_time=position.timestamp,
                    exit_time=datetime.now(),
                    symbol=symbol,
                    direction=position.side,
                    entry_price=position.entry_price,
                    exit_price=order["price"],
                    size=position.size,
                    leverage=position.leverage,
                    pnl=pnl
                )

                # Close virtual account position
                if hasattr(self, 'virtual_account'):
                    virtual_pnl = self.virtual_account.close_position(symbol, order["price"])
                    if virtual_pnl is not None:
                        logger.info(f"Virtual position closed, PnL: {virtual_pnl}")
                        # Log balance after closing position
                        trade_logger.log_balance(self.virtual_account.get_balance())
                    else:
                        logger.warning(f"Virtual position for {symbol} not found")
                
                # Remove position
                del self.positions[symbol]

        except Exception as e:
            logger.error(f"Failed to close position for {symbol}: {e}")

    async def _update_positions(self):
        """Update open positions with current market data"""
        for symbol, position in self.positions.items():
            # Get current price
            current_price = await self.exchange_manager.get_price(symbol)
            if current_price:
                # Update position PnL
                position.update_pnl(current_price)

    async def close_all_positions(self):
        """Close all open positions and reset virtual account."""
        # Close each position
        for symbol in list(self.positions.keys()):
            await self._close_position(symbol)
        # Clear virtual account positions (already done in _close_position)
        # Reset virtual account balance to default (optional)
        if hasattr(self, 'virtual_account'):
            self.virtual_account.reset_balance(self.config.get("initial_balance", 1000.0))
        # Clear any remaining positions (should be empty)
        self.positions.clear()

    def _calculate_position_size(self, signal: TradeSignal) -> float:
        """Calculate position size based on risk management"""
        # Use virtual account balance if simulating, otherwise placeholder
        if hasattr(self, 'virtual_account'):
            account_balance = self.virtual_account.get_balance()
        else:
            account_balance = 10000  # Placeholder
        risk_per_trade = self.config.get("risk_per_trade", 0.01)  # 1% risk
        stop_loss_pct = self.config.get("stop_loss", 0.02)  # 2% stop loss

        risk_amount = account_balance * risk_per_trade
        # Risk per unit = entry_price * stop_loss_pct
        risk_per_unit = signal.price * stop_loss_pct
        # Number of units to trade
        position_size = risk_amount / risk_per_unit
        # Ensure minimum size (e.g., 0.001)
        if position_size < 0.001:
            position_size = 0.001
        return position_size

    def _calculate_pnl(self, position: Position, close_price: float) -> float:
        """Calculate PnL for a position"""
        if position.side == "long":
            pnl = (close_price - position.entry_price) / position.entry_price
        else:
            pnl = (position.entry_price - close_price) / position.entry_price

        return pnl * position.size * position.leverage

    async def _send_signal_to_discord(self, signal: TradeSignal):
        """Send a trading signal to Discord via webhook"""
        # Log the signal
        trade_logger.log_signal(signal)
        
        # Calculate stop loss and take profit based on config
        stop_loss_pct = self.config.get("stop_loss", 0.02)
        take_profit_pct = self.config.get("take_profit", 0.04)
        leverage = self.config.get("leverage", 10)
        
        # Calculate SL/TP prices
        if signal.direction == "long":
            stop_loss = signal.price * (1 - stop_loss_pct)
            take_profit = signal.price * (1 + take_profit_pct)
        else:
            stop_loss = signal.price * (1 + stop_loss_pct)
            take_profit = signal.price * (1 - take_profit_pct)
        
        signal_data = {
            "symbol": signal.symbol,
            "direction": signal.direction,
            "entry_price": signal.price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "leverage": leverage,
            "indicator": signal.indicator or "N/A",
            "confidence": signal.confidence or 0.5,
        }
        
        # Send via webhook
        send_signal_to_discord(signal_data)

    async def cleanup(self):
        """Cleanup resources"""
        self.running = False
        await self.exchange_manager.cleanup()
        logger.info("Trading bot cleaned up")
