"""
Exchange Manager - Handles all exchange interactions via CCXT
"""

import asyncio
import os
from typing import Dict, List, Optional

import ccxt
from loguru import logger


class ExchangeManager:
    """Manages exchange connections and operations"""

    def __init__(self, config: Dict):
        self.config = config
        self.exchange_name = config.get("exchange", "binance")
        self.exchange: Optional[ccxt.Exchange] = None
        self.is_paper_trading = config.get("paper_trading", True)

        # Initialize exchange
        self._initialize_exchange()

    def _initialize_exchange(self):
        """Initialize the CCXT exchange"""
        self.simulate = False  # If True, we simulate trades locally
        api_key = os.getenv("EXCHANGE_API_KEY")
        secret = os.getenv("EXCHANGE_API_SECRET")
        
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            
            if self.is_paper_trading:
                # Use paper trading exchange
                self.exchange = exchange_class({
                    "apiKey": api_key,
                    "secret": secret,
                    "enableRateLimit": True,
                    "sandbox": True,
                })
                logger.info(f"Initialized {self.exchange_name} in sandbox mode")
            else:
                # Use live exchange
                self.exchange = exchange_class({
                    "apiKey": api_key,
                    "secret": secret,
                    "enableRateLimit": True,
                })
                logger.info(f"Initialized {self.exchange_name} in live mode")
            
            # If no API keys, we'll simulate order creation (but still fetch market data)
            if not api_key or not secret:
                self.simulate = True
                logger.info("No API keys provided: order creation will be simulated locally")
                
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            # Fallback to simulation
            self.simulate = True
            logger.warning("Falling back to simulated paper trading")
            # Also create a dummy exchange for public data (optional)
            self.exchange = None

    async def connect(self):
        """Connect to exchange"""
        try:
            # Load markets
            await asyncio.to_thread(self.exchange.load_markets)
            logger.info(f"Loaded {len(self.exchange.markets)} markets")
        except Exception as e:
            logger.error(f"Failed to connect to exchange: {e}")
            logger.warning("Continuing with limited functionality (no market data)")
            # Don't raise - continue with mock data

    async def start_streams(self):
        """Start market data streams"""
        logger.info("Starting market data streams...")

    async def get_prices(self) -> Dict[str, float]:
        """Get current prices for all symbols"""
        try:
            tickers = await asyncio.to_thread(self.exchange.fetch_tickers)
            prices = {symbol: ticker["last"] for symbol, ticker in tickers.items()}
            return prices
        except Exception as e:
            logger.error(f"Failed to fetch prices: {e}")
            raise

    async def get_price(self, symbol: str) -> Optional[float]:
        """Get current price for a single symbol"""
        try:
            ticker = await asyncio.to_thread(self.exchange.fetch_ticker, symbol)
            return ticker["last"]
        except Exception as e:
            logger.error(f"Failed to fetch price for {symbol}: {e}")
            return None

    async def create_order(
        self,
        symbol: str,
        side: str,
        size: float,
        leverage: int = 10,
        order_type: str = "market",
        reduce_only: bool = False,
    ) -> Optional[Dict]:
        """Create an order on the exchange (or simulate locally)"""
        if self.simulate:
            # Simulate order creation locally
            # Get current price for the symbol
            try:
                current_price = await self.get_price(symbol)
                if current_price is None:
                    logger.warning(f"Could not fetch price for {symbol}, using mock price")
                    current_price = 50000.0  # fallback mock price
            except Exception as e:
                logger.warning(f"Error fetching price for {symbol}: {e}, using mock price")
                current_price = 50000.0
            
            # Generate a mock order ID and timestamp
            import time
            from datetime import datetime
            order_id = f"sim_{int(time.time())}_{symbol}"
            timestamp = datetime.now()
            
            logger.info(f"Simulated order created: {symbol} {side} {size} @ {current_price}")
            return {
                "id": order_id,
                "price": current_price,
                "size": size,
                "side": side,
                "timestamp": timestamp,
            }
        
        try:
            # Set leverage for futures
            if "future" in self.exchange_name or self.exchange_name in ["binance", "bybit"]:
                try:
                    await asyncio.to_thread(
                        self.exchange.set_leverage,
                        leverage,
                        symbol,
                    )
                except Exception:
                    pass  # Leverage might already be set

            # Create order
            order = await asyncio.to_thread(
                self.exchange.create_order,
                symbol,
                order_type,
                side.upper(),
                size,
                None,
                {"reduceOnly": reduce_only} if reduce_only else {},
            )

            logger.info(f"Order created: {order}")
            # Convert timestamp (ms) to datetime
            from datetime import datetime
            ts = order["timestamp"]
            if isinstance(ts, (int, float)):
                timestamp = datetime.fromtimestamp(ts / 1000)
            else:
                timestamp = datetime.now()
            return {
                "id": order["id"],
                "price": order["average"] or order["price"],
                "size": order["amount"],
                "side": side,
                "timestamp": timestamp,
            }

        except Exception as e:
            logger.error(f"Failed to create order for {symbol}: {e}")
            return None

    async def get_positions(self) -> List[Dict]:
        """Get all open positions"""
        try:
            if hasattr(self.exchange, "fetch_positions"):
                positions = await asyncio.to_thread(self.exchange.fetch_positions)
                return positions
        except Exception as e:
            logger.error(f"Failed to fetch positions: {e}")
        return []

    async def get_balance(self) -> Dict:
        """Get account balance"""
        try:
            balance = await asyncio.to_thread(self.exchange.fetch_balance)
            return balance
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            return {}

    async def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[List]:
        """Get OHLCV data"""
        try:
            ohlcv = await asyncio.to_thread(
                self.exchange.fetch_ohlcv,
                symbol,
                timeframe,
                limit=limit,
            )
            return ohlcv
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            return []

    async def cleanup(self):
        """Cleanup exchange connection"""
        if self.exchange:
            try:
                await asyncio.to_thread(self.exchange.close)
            except Exception:
                pass
        logger.info("Exchange manager cleaned up")
