# Setup Guide - Crypto Leverage Bot

## Prerequisites

### Required Software

1. **Node.js 18+** (for Discord bot)
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # macOS (with Homebrew)
   brew install node
   ```

2. **Python 3.10+** (for trading engine)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv

   # macOS
   brew install python@3.11
   ```

3. **Git** (for version control)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install git

   # macOS
   brew install git
   ```

4. **GitHub CLI** (optional, for deployment)
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update
   sudo apt install gh

   # macOS
   brew install gh
   ```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/will08126-blip/crypto-leverage-bot.git
cd crypto-leverage-bot
```

### 2. Setup Discord Bot

```bash
cd discord-bot

# Install dependencies
npm install

# Copy environment file
cp .env.example .env
```

Edit `.env` with your Discord bot credentials.

### 3. Setup Trading Engine

```bash
cd ../trading-engine

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

Edit `.env` with your exchange API credentials.

## Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "Crypto Leverage Bot")
4. Go to "Bot" tab and click "Add Bot"
5. Copy the bot token (you'll need this for `.env`)
6. Enable "Message Content Intent" under Privileged Gateway Intents
7. Generate an OAuth2 URL with these scopes:
   - `bot`
   - `applications.commands`
   - `applications.commands`
   
   Permissions needed:
   - Send Messages
   - Read Messages/View Channels
   - Use Application Commands

8. Invite the bot to your server using the generated URL

## Configuration

### Exchange Setup

1. Create an account on your preferred exchange (Binance, Bybit, etc.)
2. Generate API keys with trading permissions
3. Add API keys to `trading-engine/.env`:
   ```env
   EXCHANGE_API_KEY=your_api_key
   EXCHANGE_API_SECRET=your_api_secret
   PAPER_TRADING=true  # Start with paper trading!
   ```

### Strategy Configuration

Edit `trading-engine/utils/config.py` or use environment variables to configure:
- Leverage settings
- Risk management parameters
- Trading symbols
- Strategy parameters

## Running the Bot

### Start Discord Bot

```bash
cd discord-bot
npm run dev
```

### Start Trading Engine

```bash
cd ../trading-engine
python main.py
```

## Testing

### Run Backtests

```bash
cd trading-engine
python scripts/backtest.py --strategy rsi_strategy --symbol BTC/USDT --timeframe 1h
```

### Run Unit Tests

```bash
# Discord Bot
cd discord-bot
npm test

# Trading Engine
cd ../trading-engine
pytest
```

## Deployment

### Deploy to Render

1. Fork this repository on GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Background Worker"
4. Connect your GitHub account
5. Select your forked repository
6. Use `deploy/render.yaml` as the blueprint
7. Add environment variables:
   - `DISCORD_BOT_TOKEN`
   - `EXCHANGE_API_KEY`
   - `EXCHANGE_API_SECRET`
8. Deploy!

### Environment Variables on Render

Add these in the Render dashboard under "Environment" tab:

```
DISCORD_BOT_TOKEN=your_token
DISCORD_CLIENT_ID=your_client_id
EXCHANGE_API_KEY=your_api_key
EXCHANGE_API_SECRET=your_api_secret
PAPER_TRADING=true
```

## Troubleshooting

### Bot not responding to commands

- Check if bot has proper permissions
- Verify bot token in .env file
- Check bot is online in Discord

### API connection issues

- Verify API keys are correct
- Check if API keys have trading permissions
- Ensure IP whitelisting if required by exchange

### Deployment fails on Render

- Check environment variables are set correctly
- Verify Python version in render.yaml
- Check build logs for errors

## Next Steps

1. Test with paper trading
2. Run backtests on historical data
3. Gradually increase leverage
4. Monitor performance and adjust strategies
5. Consider adding more strategies
