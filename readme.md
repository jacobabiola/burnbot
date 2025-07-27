# Blockchain Transaction Monitoring Bot

A comprehensive Telegram bot system for monitoring blockchain transactions, token burns, and wallet activities across multiple networks including Ethereum, PulseChain, and Binance Smart Chain.

## 📋 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Modules](#modules)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Documentation](#documentation)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## ✨ Features

### Core Functionality
- **Multi-Blockchain Support**: Ethereum, PulseChain, and Binance Smart Chain
- **Real-time Monitoring**: Continuous monitoring with 60-second intervals
- **Token Burn Detection**: Advanced burn event tracking and alerts
- **Whale Wallet Tracking**: Monitor large wallet movements
- **DeFi Protocol Monitoring**: Track protocol treasuries and governance
- **Telegram Integration**: Rich formatted notifications with clickable links

### Advanced Features
- **USD Value Calculations**: Real-time price fetching from CoinGecko
- **Duplicate Prevention**: Transaction hash tracking to avoid duplicate alerts
- **File-based Persistence**: Automatic state management and recovery
- **Address Validation**: Robust input validation with regex patterns
- **Error Handling**: Comprehensive error handling with automatic retries

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd blockchain-monitor

# Install dependencies
pip install -r requirements.txt

# Or install core dependencies manually
pip install requests web3 python-telegram-bot
```

### 2. Setup Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command to create a new bot
3. Save the provided bot token
4. Get your chat/group ID where alerts will be sent

### 3. Configure API Keys
```python
# Edit your chosen module (burnBot.py, NewBurnAlertBot.py, or burnAlertBot.py)
ETHERSCAN_API_KEY = 'your_etherscan_api_key'      # Get from https://etherscan.io/apis
BSCSCAN_API_KEY = 'your_bscscan_api_key'          # Get from https://bscscan.com/apis (burnAlertBot.py only)
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'    # From BotFather
TELEGRAM_CHAT_ID = '@your_group_or_chat_id'       # Your target chat
```

### 4. Run the Bot
```bash
# For advanced burn monitoring
python burnBot.py

# For enhanced burn alerts
python NewBurnAlertBot.py

# For basic wallet monitoring
python burnAlertBot.py
```

## 📦 Modules

### `burnBot.py` - Advanced Token Burn Monitoring
- **Purpose**: Monitor token burn events with wallet and token management
- **Features**: Token-specific monitoring, burn address tracking, advanced notifications
- **Commands**: `/addwallet`, `/addtoken`, `/removewallet`, `/removetoken`, `/listwallets`, `/listtokens`

### `NewBurnAlertBot.py` - Enhanced Burn Alert System
- **Purpose**: Similar to burnBot.py with updated configuration and enhanced features
- **Features**: Improved burn detection, better error handling, enhanced notifications
- **Commands**: Same as burnBot.py

### `burnAlertBot.py` - Basic Wallet Transaction Monitor
- **Purpose**: Simple wallet transaction monitoring without token filtering
- **Features**: Basic transaction alerts, multi-blockchain support, simplified commands
- **Commands**: `/add`, `/remove`, `/list`

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection for API access

### Step-by-Step Installation

1. **Install Python** (if not already installed)
   ```bash
   # Download from https://www.python.org/downloads/
   python --version  # Verify installation
   ```

2. **Install Dependencies**
   ```bash
   # Option 1: Using requirements.txt (recommended)
   pip install -r requirements.txt
   
   # Option 2: Install core dependencies manually
   pip install requests web3 python-telegram-bot
   
   # Option 3: Install with optional dependencies
   pip install requests web3 python-telegram-bot aiohttp flask pandas
   ```

3. **Verify Installation**
   ```python
   # Test imports
   import requests
   import web3
   import telegram
   print("✅ All dependencies installed successfully")
   ```

## ⚙️ Configuration

### Environment Variables (Recommended)
```bash
# Create .env file
echo "ETHERSCAN_API_KEY=your_key_here" >> .env
echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
echo "TELEGRAM_CHAT_ID=@your_chat_id" >> .env
```

### Direct Configuration
Edit the constants in your chosen module:
```python
# Required for all modules
ETHERSCAN_API_KEY = 'your_etherscan_api_key'
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = '@your_telegram_group'

# Required for burnAlertBot.py only
BSCSCAN_API_KEY = 'your_bscscan_api_key'
```

### File Structure
The bot creates several files automatically:
```
/your-project/
├── burnBot.py                 # Your chosen module
├── watched_wallets.txt        # Monitored wallets (auto-created)
├── watched_tokens.txt         # Monitored tokens (auto-created)
├── latest_tx_hashes.json      # Transaction cache (auto-created)
├── last_run_time.txt          # Last run timestamp (auto-created)
└── requirements.txt           # Dependencies
```

## 📖 Usage

### Basic Commands

#### Token Burn Monitoring (burnBot.py / NewBurnAlertBot.py)
```
/start                          # Show help and available commands
/addwallet ETH 0x000000000000000000000000000000000000dEaD    # Add burn address
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48     # Add USDC token
/listwallets                    # Show all monitored wallets
/listtokens                     # Show all monitored tokens
/removewallet ETH 0x...         # Remove wallet from monitoring
/removetoken ETH 0x...          # Remove token from monitoring
```

#### Basic Wallet Monitoring (burnAlertBot.py)
```
/start                          # Show help
/add ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42        # Add wallet
/add PLS 0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d         # Add PulseChain wallet
/list                           # Show all monitored wallets
/remove ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42     # Remove wallet
```

### Common Use Cases

#### 1. Monitor Token Burns
```bash
# Add burn addresses
/addwallet ETH 0x000000000000000000000000000000000000dEaD
/addwallet PLS 0x000000000000000000000000000000000000dEaD

# Add tokens to monitor
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  # USDC
/addtoken ETH 0x6B175474E89094C44Da98b954EedeAC495271d0F  # DAI
```

#### 2. Track Whale Wallets
```bash
# Monitor known whale addresses
/addwallet ETH 0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503  # Binance hot wallet
/addwallet ETH 0x8315177aB297bA92A06054cE80a67Ed4DBd7ed3a  # Bitfinex cold wallet
```

#### 3. DeFi Protocol Monitoring
```bash
# Monitor DeFi protocol addresses
/addwallet ETH 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643  # Compound cDAI
/addwallet ETH 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7  # Curve 3pool
```

## 📚 Documentation

### Complete Documentation Files
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference with all functions and examples
- **[FUNCTION_REFERENCE.md](./FUNCTION_REFERENCE.md)** - Detailed function documentation with signatures and usage
- **[USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md)** - Practical examples and integration guides

### Key Features Documentation

#### Supported Blockchains
| Blockchain | Identifier | API Endpoint | Native Token |
|-----------|------------|--------------|--------------|
| Ethereum | `eth` | api.etherscan.io | ETH |
| PulseChain | `pls` | scan.pulsechain.com | PLS |
| Binance Smart Chain | `bnb` | api.bscscan.com | BNB |

#### Notification Format
```
Token Burn transaction.
Blockchain: ETH
Burn Address: [Clickable Address Link]
Burnt: 10,000 USDC
Worth: (~$10,000.00)
From: [Clickable Sender Link]
[Transaction Hash Link]
```

## 🔧 API Reference

### Core Functions
- `get_wallet_transactions(wallet_address, token_address, blockchain)` - Fetch transaction history
- `send_telegram_notification(...)` - Send formatted alerts
- `add_wallet(wallet_address, blockchain)` - Add wallet to monitoring
- `add_token(token_address, blockchain)` - Add token to monitoring
- `monitor_wallets()` - Main monitoring loop

### Telegram Commands
- `/start` - Display help and commands
- `/addwallet <blockchain> <address>` - Add wallet to monitoring
- `/addtoken <blockchain> <address>` - Add token to monitoring (burn bots)
- `/listwallets` - List all monitored wallets
- `/listtokens` - List all monitored tokens (burn bots)

## 🚨 Rate Limits and Considerations

### API Rate Limits
- **Etherscan**: 5 calls/second, 100,000 calls/day
- **BSCScan**: 5 calls/second, 10,000 calls/day
- **PulseChain**: No documented limits
- **CoinGecko**: 10-30 calls/minute (free tier)
- **Telegram Bot**: 30 messages/second

### Performance Recommendations
- **Monitoring Interval**: 60 seconds (default)
- **Maximum Wallets**: 50-100 per blockchain
- **Maximum Tokens**: 20-50 per blockchain

## 🛡️ Security Best Practices

1. **API Keys**: Store in environment variables, not source code
2. **File Permissions**: Restrict access to configuration files
3. **Input Validation**: All addresses validated with regex patterns
4. **Error Logging**: Avoid logging sensitive information
5. **Rate Limiting**: Built-in delays prevent API abuse

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support and Troubleshooting

### Common Issues
- **Bot not responding**: Check Telegram bot token and chat permissions
- **No transaction alerts**: Verify API keys and wallet addresses
- **Price data unavailable**: Check CoinGecko API connectivity

### Getting Help
1. Check the [API Documentation](./API_DOCUMENTATION.md)
2. Review [Usage Examples](./USAGE_EXAMPLES.md)
3. Test API connectivity using provided scripts
4. Create an issue with detailed error logs






