# Trading Strategies Documentation

## Overview

This bot supports multiple trading strategies that can be combined for better performance.

## Available Strategies

### 1. RSI Strategy (rsi_strategy)

**Description**: Uses Relative Strength Index to identify overbought/oversold conditions.

**Parameters**:
- `RSI_PERIOD`: 14 (default) - Lookback period for RSI calculation
- `RSI_OVERBOUGHT`: 70 (default) - RSI level considered overbought
- `RSI_OVERSOLD`: 30 (default) - RSI level considered oversold

**Signals**:
- **Buy**: RSI < 30 (oversold condition)
- **Sell**: RSI > 70 (overbought condition)

**Best Used For**:
- Range-bound markets
- Short-term trading
- Reversal strategies

**Pros**:
- Simple to understand
- Works well in sideways markets
- Good for identifying extremes

**Cons**:
- Can give false signals in trending markets
- Lagging indicator

---

### 2. MACD Strategy (macd_strategy)

**Description**: Uses Moving Average Convergence/Divergence for trend following.

**Parameters**:
- `MACD_FAST`: 12 (default) - Fast EMA period
- `MACD_SLOW`: 26 (default) - Slow EMA period
- `MACD_SIGNAL`: 9 (default) - Signal line period

**Signals**:
- **Buy**: MACD crosses above signal line (bullish crossover)
- **Sell**: MACD crosses below signal line (bearish crossover)

**Best Used For**:
- Trending markets
- Medium-term trading
- Momentum strategies

**Pros**:
- Good for identifying trend direction
- Works well in trending markets
- Can filter out noise

**Cons**:
- Lagging indicator
- Can give false signals during reversals

---

### 3. Bollinger Bands Strategy (bb_strategy)

**Description**: Uses Bollinger Bands for volatility-based trading.

**Parameters**:
- `BB_PERIOD`: 20 (default) - Lookback period
- `BB_STD`: 2.0 (default) - Standard deviation multiplier

**Signals**:
- **Buy**: Price touches or breaks below lower band (oversold)
- **Sell**: Price touches or breaks above upper band (overbought)

**Best Used For**:
- Volatility-based trading
- Range-bound markets
- Mean reversion strategies

**Pros**:
- Adapts to market volatility
- Good for identifying extremes
- Visual and easy to understand

**Cons**:
- Can give false signals in strong trends
- Requires careful parameter tuning

---

## Strategy Combinations

### Conservative Setup
```
strategies:
  - rsi_strategy
  - bb_strategy
```
Uses both RSI and Bollinger Bands for confirmation. More reliable but fewer signals.

### Aggressive Setup
```
strategies:
  - macd_strategy
  - rsi_strategy
```
Combines trend following with momentum. More signals but potentially more false positives.

### All Strategies
```
strategies:
  - rsi_strategy
  - macd_strategy
  - bb_strategy
```
Maximum coverage. Requires careful signal filtering.

---

## Backtesting Parameters

When running backtests, consider these parameters:

| Parameter | Conservative | Moderate | Aggressive |
|-----------|--------------|----------|------------|
| Leverage | 3x | 10x | 25x |
| Risk per trade | 0.5% | 1% | 2% |
| Stop loss | 1% | 2% | 3% |
| Take profit | 3% | 5% | 8% |

---

## Example Backtest Command

```bash
# Test RSI strategy on BTC/USDT
python scripts/backtest.py --strategy rsi_strategy --symbol BTC/USDT --timeframe 1h

# Test multiple timeframes
python scripts/backtest.py --strategy macd_strategy --symbol ETH/USDT --timeframe 4h
```

---

## Risk Management

### Position Sizing Formula

```
Position Size = (Account Balance × Risk per Trade) / Stop Loss %
```

Example:
- Account Balance: $10,000
- Risk per Trade: 1% ($100)
- Stop Loss: 2%
- Position Size = $100 / 0.02 = $5,000

### Leverage Guidelines

| Account Size | Recommended Max Leverage |
|--------------|-------------------------|
| < $1,000 | 5x |
| $1,000 - $5,000 | 10x |
| $5,000 - $10,000 | 15x |
| > $10,000 | 20x |

⚠️ **Warning**: Higher leverage increases both potential profits AND losses!

---

## Creating Custom Strategies

To create a new strategy:

1. Create a new file in `trading-engine/strategies/`
2. Extend the `BaseStrategy` class
3. Implement the `generate_signal` method
4. Add your strategy to the config

Example structure:
```python
from trading_engine.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, config):
        super().__init__(config)
        self.name = "my_strategy"
        self.description = "My custom strategy"

    def generate_signal(self, symbol, price):
        # Your strategy logic here
        signals = []
        # Add signals to list
        return signals
```
