# Blockchain Transaction Monitoring Bot - API Documentation

## Overview

This project consists of three main modules that implement a Telegram bot for monitoring blockchain transactions and token burns across multiple networks (Ethereum, PulseChain, and Binance Smart Chain). The bot provides real-time alerts for wallet transactions and token burn events.

## Modules

- **`burnBot.py`** - Advanced token burn monitoring bot with wallet and token management
- **`NewBurnAlertBot.py`** - Enhanced burn alert bot (similar to burnBot.py with updated configuration)
- **`burnAlertBot.py`** - Basic wallet transaction monitoring bot

## Configuration

### Environment Variables
Before using any module, configure the following constants in the respective files:

```python
ETHERSCAN_API_KEY = 'your_etherscan_api_key'     # Required for Ethereum blockchain access
BSCSCAN_API_KEY = 'your_bscscan_api_key'         # Required for BSC blockchain access (burnAlertBot.py only)
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'   # Required for Telegram bot functionality
TELEGRAM_CHAT_ID = '@your_telegram_group'        # Target chat/group for notifications
```

## Core Functions

### Transaction Management

#### `get_wallet_transactions(wallet_address, token_address, blockchain)`

Fetches transaction history for a specific wallet and token on a specified blockchain.

**Parameters:**
- `wallet_address` (str): The wallet address to query (40-character hex string starting with '0x')
- `token_address` (str): The token contract address to filter transactions
- `blockchain` (str): Target blockchain ('eth' for Ethereum, 'pls' for PulseChain)

**Returns:**
- `list`: List of transaction dictionaries containing transaction details

**Raises:**
- `ValueError`: If an invalid blockchain is specified

**Example:**
```python
# Get transactions for a specific wallet and token on Ethereum
transactions = get_wallet_transactions(
    wallet_address='0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42',
    token_address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    blockchain='eth'
)

# Response format:
[
    {
        'hash': '0x123...',
        'from': '0xabc...',
        'to': '0xdef...',
        'value': '1000000000000000000',
        'timeStamp': '1640995200',
        'blockNumber': '13916165',
        'tokenSymbol': 'USDC'
    }
]
```

#### `get_wallet_transactions(wallet_address, blockchain)` (burnAlertBot.py variant)

Simpler version that fetches all transactions for a wallet without token filtering.

**Parameters:**
- `wallet_address` (str): The wallet address to query
- `blockchain` (str): Target blockchain ('eth', 'bnb', 'pls')

**Returns:**
- `list`: List of all transactions for the wallet

### Notification System

#### `send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to, token_symbol)`

Sends formatted transaction alerts to a Telegram chat.

**Parameters:**
- `message` (str): Alert message text
- `value` (float): Transaction value in native token units
- `usd_value` (float): USD equivalent of the transaction
- `tx_hash` (str): Transaction hash for linking
- `blockchain` (str): Source blockchain
- `w_from` (str): Sender wallet address
- `w_to` (str): Recipient wallet address
- `token_symbol` (str): Token symbol (burnBot.py/NewBurnAlertBot.py only)

**Returns:**
- `requests.Response`: Response from Telegram API

**Example:**
```python
# Send a burn notification
response = send_telegram_notification(
    message="Token burn detected",
    value=1000.0,
    usd_value=2500.0,
    tx_hash="0x123456789abcdef",
    blockchain="eth",
    w_from="0xabc123...",
    w_to="0x000000000000000000000000000000000000dEaD",
    token_symbol="USDC"
)
```

**Notification Format:**
```
Token Burn transaction.
Blockchain: ETH
Burn Address: [Clickable burn address link]
Burnt: 1,000 USDC
Worth: (~$2,500.00)
From: [Clickable sender address link]
[Transaction hash link]
```

### Wallet Management

#### `add_wallet(wallet_address, blockchain)`

Adds a new wallet to the monitoring list.

**Parameters:**
- `wallet_address` (str): Valid wallet address (0x format, 40 characters)
- `blockchain` (str): Target blockchain identifier

**File Operation:**
- Appends `blockchain:wallet_address` to `watched_wallets.txt`

**Example:**
```python
# Add an Ethereum wallet to monitoring
add_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')

# Add a PulseChain wallet to monitoring  
add_wallet('0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d', 'pls')
```

#### `remove_wallet(wallet_address, blockchain)`

Removes a wallet from the monitoring list.

**Parameters:**
- `wallet_address` (str): Wallet address to remove
- `blockchain` (str): Source blockchain

**File Operation:**
- Removes matching `blockchain:wallet_address` line from `watched_wallets.txt`

**Example:**
```python
# Remove a wallet from monitoring
remove_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')
```

### Token Management (burnBot.py & NewBurnAlertBot.py)

#### `add_token(token_address, blockchain)`

Adds a new token contract to the monitoring list.

**Parameters:**
- `token_address` (str): Valid token contract address
- `blockchain` (str): Target blockchain identifier

**File Operation:**
- Appends `blockchain:token_address` to `watched_tokens.txt`

**Example:**
```python
# Add USDC token on Ethereum
add_token('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'eth')

# Add a PulseChain token
add_token('0x6753560538ECa67617A9Ce605178F788bE7E524E', 'pls')
```

#### `remove_token(token_address, blockchain)`

Removes a token from the monitoring list.

**Parameters:**
- `token_address` (str): Token contract address to remove
- `blockchain` (str): Source blockchain

**Example:**
```python
# Remove USDC from monitoring
remove_token('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'eth')
```

## Monitoring System

### `monitor_wallets()`

Main monitoring loop that continuously checks for new transactions and sends alerts.

**Functionality:**
- Loads watched wallets and tokens from files
- Fetches real-time cryptocurrency prices from CoinGecko API
- Polls blockchain APIs for new transactions every 60 seconds
- Filters transactions based on timestamp and hash tracking
- Sends Telegram notifications for qualifying transactions
- Maintains state files for tracking processed transactions

**State Files:**
- `watched_wallets.txt` - List of monitored wallets (format: `blockchain:address`)
- `watched_tokens.txt` - List of monitored tokens (format: `blockchain:address`)
- `latest_tx_hashes.json` - Cache of processed transaction hashes
- `last_run_time.txt` - Timestamp of last successful run

**Supported Price APIs:**
- Ethereum (ETH)
- PulseChain (PLS)  
- Binance Coin (BNB) - burnAlertBot.py only
- Chainlink (LINK) - burnBot.py/NewBurnAlertBot.py only
- DAI, USDC, USDT - burnBot.py/NewBurnAlertBot.py only

**Error Handling:**
- Continues operation on API failures
- 10-second retry delay on exceptions
- Logs all errors with timestamps

## Telegram Bot Commands

### `/start`

Displays welcome message and command help.

**Response:**
```
👋 Welcome to the Ethereum and Pulsechain token burn Monitoring Bot!

Use /addwallet <blockchain> <wallet_address> to add a new wallet to monitor.
Use /addtoken <blockchain> <token_address> to add a new token to monitor.
[... additional help text ...]
```

### `/addwallet <blockchain> <wallet_address>`

Adds a wallet to the monitoring list via Telegram command.

**Parameters:**
- `blockchain`: 'ETH', 'PLS' (case insensitive)
- `wallet_address`: Valid 40-character hex address

**Validation:**
- Validates address format using regex: `^0x[a-fA-F0-9]{40}$`
- Checks blockchain compatibility

**Examples:**
```
/addwallet ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
/addwallet PLS 0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d
```

### `/addtoken <blockchain> <token_address>` (burnBot.py & NewBurnAlertBot.py)

Adds a token to the monitoring list via Telegram command.

**Parameters:**
- `blockchain`: 'ETH', 'PLS' (case insensitive)  
- `token_address`: Valid 40-character hex token contract address

**Examples:**
```
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
/addtoken PLS 0x6753560538ECa67617A9Ce605178F788bE7E524E
```

### `/removewallet <blockchain> <wallet_address>`

Removes a wallet from monitoring.

**Example:**
```
/removewallet ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
```

### `/removetoken <blockchain> <token_address>` (burnBot.py & NewBurnAlertBot.py)

Removes a token from monitoring.

**Example:**
```
/removetoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

### `/listwallets`

Lists all currently monitored wallets by blockchain.

**Response Format:**
```
The following wallets are currently being monitored

Ethereum Wallets:
1. 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
2. 0x000000000000000000000000000000000000dEaD

Pulse Chain Wallets:
1. 0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d
```

### `/listtokens` (burnBot.py & NewBurnAlertBot.py)

Lists all currently monitored tokens by blockchain.

## Data Structures

### Transaction Object
```python
{
    'hash': str,           # Transaction hash
    'from': str,           # Sender address  
    'to': str,             # Recipient address
    'value': str,          # Value in wei (string)
    'timeStamp': str,      # Unix timestamp (string)
    'blockNumber': str,    # Block number (string)
    'tokenSymbol': str     # Token symbol (burn bots only)
}
```

### Price Data Object (from CoinGecko)
```python
{
    'ethereum': {'usd': float},
    'pulsechain': {'usd': float},
    'binancecoin': {'usd': float},    # burnAlertBot.py only
    'chainlink': {'usd': float},      # burnBot.py/NewBurnAlertBot.py only
    'dai': {'usd': float},            # burnBot.py/NewBurnAlertBot.py only
    'usd-coin': {'usd': float},       # burnBot.py/NewBurnAlertBot.py only
    'tether': {'usd': float}          # burnBot.py/NewBurnAlertBot.py only
}
```

## Error Handling

### Common Exceptions

#### `ValueError`
- **Cause:** Invalid blockchain parameter
- **Message:** "Invalid blockchain specified"
- **Resolution:** Use supported blockchain identifiers

#### `requests.RequestException` 
- **Cause:** API connection failures
- **Handling:** Automatic retry with 10-second delay

#### `json.JSONDecodeError`
- **Cause:** Invalid API response format
- **Handling:** Logged and operation continues

#### `FileNotFoundError`
- **Cause:** Missing configuration files
- **Handling:** Files created automatically with empty content

## Installation and Setup

### Prerequisites
```bash
pip install requests web3 python-telegram-bot
```

### Required Files
- `watched_wallets.txt` (created automatically)
- `watched_tokens.txt` (created automatically, burn bots only)
- `latest_tx_hashes.json` (created automatically)
- `last_run_time.txt` (created automatically)

### Configuration Steps

1. **Create Telegram Bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Save the provided bot token

2. **Get API Keys:**
   - Etherscan: https://etherscan.io/apis
   - BSCScan: https://bscscan.com/apis (for burnAlertBot.py)

3. **Update Configuration:**
   ```python
   ETHERSCAN_API_KEY = 'your_api_key'
   TELEGRAM_BOT_TOKEN = 'your_bot_token' 
   TELEGRAM_CHAT_ID = '@your_group_or_chat_id'
   ```

4. **Run Bot:**
   ```bash
   python burnBot.py
   # or
   python NewBurnAlertBot.py  
   # or
   python burnAlertBot.py
   ```

## Usage Examples

### Basic Wallet Monitoring
```python
# Start the basic wallet monitoring bot
python burnAlertBot.py

# Add wallets via Telegram
/add ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
/add PLS 0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d

# Monitor transactions
# Bot will automatically send alerts for incoming/outgoing transactions
```

### Token Burn Monitoring
```python
# Start the advanced burn monitoring bot
python burnBot.py

# Add burn address (dead wallet)
/addwallet ETH 0x000000000000000000000000000000000000dEaD

# Add tokens to monitor
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  # USDC
/addtoken ETH 0x6B175474E89094C44Da98b954EedeAC495271d0F  # DAI

# Bot will alert when tokens are sent to burn addresses
```

### Programmatic Usage
```python
# Direct function calls (not recommended for production)
from burnBot import add_wallet, get_wallet_transactions, send_telegram_notification

# Add wallet programmatically
add_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')

# Get transaction history
transactions = get_wallet_transactions(
    wallet_address='0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42',
    token_address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 
    blockchain='eth'
)

# Send custom notification
send_telegram_notification(
    message="Custom alert",
    value=100.0,
    usd_value=250.0,
    tx_hash="0x123...",
    blockchain="eth",
    w_from="0xabc...",
    w_to="0xdef...",
    token_symbol="USDC"
)
```

## Supported Blockchains

| Blockchain | Identifier | API Endpoint | Native Token |
|-----------|------------|--------------|--------------|
| Ethereum | `eth` | api.etherscan.io | ETH |
| PulseChain | `pls` | scan.pulsechain.com | PLS |
| Binance Smart Chain | `bnb` | api.bscscan.com | BNB |

## Rate Limits

- **Etherscan API:** 5 calls/second, 100,000 calls/day
- **BSCScan API:** 5 calls/second, 10,000 calls/day
- **PulseChain API:** No documented limits
- **CoinGecko API:** 10-30 calls/minute (free tier)
- **Telegram Bot API:** 30 messages/second

## Security Considerations

1. **API Keys:** Store in environment variables, not in source code
2. **File Permissions:** Restrict access to configuration files
3. **Input Validation:** All addresses validated with regex patterns
4. **Error Logging:** Avoid logging sensitive information
5. **Rate Limiting:** Built-in delays prevent API abuse

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check Telegram bot token validity
- Verify bot is added to target chat/group
- Ensure bot has permission to send messages

**No transaction alerts:**
- Verify API keys are correct and active
- Check wallet/token addresses are valid
- Confirm blockchain identifier is supported
- Review log output for error messages

**Price data unavailable:**
- CoinGecko API may be temporarily unavailable
- Check internet connectivity
- Verify token IDs in price URL

**File permission errors:**
- Ensure write permissions for working directory
- Check disk space availability
- Verify no other processes are using the files

### Debugging Tips

1. **Enable verbose logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test API connectivity:**
   ```python
   import requests
   response = requests.get('https://api.etherscan.io/api?module=stats&action=ethsupply&apikey=YourAPIKey')
   print(response.json())
   ```

3. **Validate address format:**
   ```python
   import re
   address = '0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42'
   is_valid = re.match(r'^0x[a-fA-F0-9]{40}$', address) is not None
   print(f"Address valid: {is_valid}")
   ```

## Performance Optimization

### Recommended Settings

- **Monitoring Interval:** 60 seconds (default)
- **Maximum Monitored Wallets:** 50-100 per blockchain
- **Maximum Monitored Tokens:** 20-50 per blockchain
- **Transaction History Limit:** Last 10,000 transactions

### Scaling Considerations

For high-volume monitoring:
1. Implement connection pooling for API requests
2. Use database storage instead of text files
3. Add multi-threading for concurrent API calls
4. Implement caching for frequently accessed data
5. Consider using WebSocket connections for real-time data