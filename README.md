# Crypto Leverage Bot 🚀

A comprehensive Discord trading bot for cryptocurrency leverage trading with paper trading, backtesting capabilities, and real-time alerts.

## Project Overview

This bot provides:
- **Discord Integration** - Real-time trading signals and alerts via Discord
- **Trading Engine** - Paper trading and backtesting framework
- **Strategy System** - Configurable trading strategies with technical indicators
- **Multi-Exchange Support** - Binance, Bybit, and other crypto exchanges via CCXT

## Project Structure

```
crypto-leverage-bot/
├── discord-bot/          # Discord bot implementation (TypeScript)
├── trading-engine/       # Paper trading, backtesting, and execution
├── strategy/             # Strategy designs and configurations
├── deploy/               # Deployment configs (Render, GitHub Actions)
├── docs/                 # Documentation and guides
└── .gitignore            # Git ignore patterns
```

## Quick Start

### Prerequisites

- Node.js 18+ (for Discord bot)
- Python 3.10+ (for trading engine)
- GitHub account
- Discord bot token
- Crypto exchange API keys

### 1. Clone the Repository

```bash
git clone https://github.com/will08126-blip/crypto-leverage-bot.git
cd crypto-leverage-bot
```

### 2. Install Dependencies

**Discord Bot (TypeScript):**
```bash
cd discord-bot
npm install
```

**Trading Engine (Python):**
```bash
cd ../trading-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` files in each directory:

**discord-bot/.env:**
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_GUILD_ID=your_server_id
EXCHANGE_API_KEY=your_api_key
EXCHANGE_API_SECRET=your_api_secret
```

**trading-engine/.env:**
```env
EXCHANGE_API_KEY=your_api_key
EXCHANGE_API_SECRET=your_api_secret
PAPER_TRADING=true
```

### 4. Run the Bot Locally

**Start Discord Bot:**
```bash
cd discord-bot
npm run dev
```

**Run Trading Engine:**
```bash
cd ../trading-engine
python main.py
```

## Usage

### Trading Commands (Discord)

- `/trade <symbol> <direction> <leverage>` - Open a position
- `/close <symbol>` - Close position
- `/positions` - View current positions
- `/balance` - View account balance
- `/backtest <strategy> <timeframe>` - Run backtest
- `/help` - Show all commands

### Configuration

Edit `strategy/config.yaml` to customize:
- Trading pairs
- Leverage settings
- Risk management rules
- Technical indicator parameters

## Deployment

### Deploy to Render

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Background Worker" or "Web Service"
4. Connect your GitHub account and select this repo
5. Select `deploy/render.yaml` as the blueprint
6. Add environment variables from the `.env.example` files
7. Deploy!

### Environment Variables for Render

Required variables:
- `DISCORD_BOT_TOKEN`
- `EXCHANGE_API_KEY`
- `EXCHANGE_API_SECRET`
- `NODE_ENV` (production)

### CI/CD Pipeline

This repository includes GitHub Actions for:
- Automated testing on pull requests
- Code linting and formatting
- Automatic deployment to Render on merge to main

## Backtesting

To run backtests on historical data:

```bash
cd trading-engine
python backtest.py --strategy rsi_strategy --symbol BTC/USDT --timeframe 1h --start 2024-01-01 --end 2024-12-31
```

Available strategies:
- `rsi_strategy` - RSI-based entry/exit
- `macd_strategy` - MACD crossover signals
- `bb_strategy` - Bollinger Bands breakout

## Risk Management

⚠️ **WARNING: Leverage trading is extremely risky**

- This bot supports high leverage (up to 100x)
- Use paper trading mode to test strategies
- Never risk more than 1-2% of capital per trade
- Always use stop-losses
- Monitor positions actively

## Development

### Adding New Strategies

1. Create strategy file in `trading-engine/strategies/`
2. Define entry/exit conditions
3. Add to `strategy/config.yaml`
4. Test with backtesting

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Support

- Create an issue on GitHub
- Join our Discord server for discussions

---

**Disclaimer**: This software is for educational purposes only. Trading cryptocurrencies involves substantial risk of loss and is not suitable for every investor. Past performance is not indicative of future results.
