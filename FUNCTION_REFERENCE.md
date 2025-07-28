# Function Reference Guide

## Core Transaction Functions

### `get_wallet_transactions(wallet_address, token_address, blockchain)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Retrieves token transaction history for a specific wallet and token contract.

```python
def get_wallet_transactions(wallet_address, token_address, blockchain):
    """
    Fetch token transactions for a wallet from blockchain API.
    
    Args:
        wallet_address (str): Target wallet address (0x format)
        token_address (str): Token contract address to filter
        blockchain (str): 'eth' or 'pls'
        
    Returns:
        list: Transaction objects with keys:
            - hash: Transaction hash
            - from: Sender address
            - to: Recipient address  
            - value: Value in wei (string)
            - timeStamp: Unix timestamp (string)
            - blockNumber: Block number (string)
            - tokenSymbol: Token symbol
            
    Raises:
        ValueError: If blockchain not supported
        
    Example:
        >>> txs = get_wallet_transactions(
        ...     '0x000000000000000000000000000000000000dEaD',
        ...     '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 
        ...     'eth'
        ... )
        >>> print(f"Found {len(txs)} transactions")
    """
```

### `get_wallet_transactions(wallet_address, blockchain)`
**Module:** `burnAlertBot.py`

Simplified version for all wallet transactions without token filtering.

```python
def get_wallet_transactions(wallet_address, blockchain):
    """
    Fetch all transactions for a wallet from blockchain API.
    
    Args:
        wallet_address (str): Target wallet address
        blockchain (str): 'eth', 'bnb', or 'pls'
        
    Returns:
        list: All transaction objects for the wallet
        
    Example:
        >>> txs = get_wallet_transactions(
        ...     '0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42',
        ...     'eth'
        ... )
    """
```

## Notification Functions

### `send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to, token_symbol)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Sends formatted burn notification to Telegram with transaction details.

```python
def send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to, token_symbol):
    """
    Send formatted burn alert to Telegram chat.
    
    Args:
        message (str): Base alert message
        value (float): Token amount burned
        usd_value (float): USD equivalent value
        tx_hash (str): Transaction hash for linking
        blockchain (str): Source blockchain ('eth', 'pls')
        w_from (str): Sender wallet address
        w_to (str): Recipient (burn) address
        token_symbol (str): Token symbol/name
        
    Returns:
        requests.Response: Telegram API response
        
    Example:
        >>> response = send_telegram_notification(
        ...     "Token burn detected",
        ...     1000.0,
        ...     2500.0,
        ...     "0x123...",
        ...     "eth",
        ...     "0xsender...",
        ...     "0x000000000000000000000000000000000000dEaD",
        ...     "USDC"
        ... )
        >>> print(f"Status: {response.status_code}")
    """
```

### `send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to)`
**Module:** `burnAlertBot.py`

Basic notification without token symbol parameter.

```python
def send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to):
    """
    Send transaction alert to Telegram chat.
    
    Args:
        message (str): Alert message
        value (float): Transaction value in native token
        usd_value (float): USD equivalent
        tx_hash (str): Transaction hash
        blockchain (str): Source blockchain ('eth', 'bnb', 'pls')
        w_from (str): Sender address
        w_to (str): Recipient address
        
    Returns:
        requests.Response: Telegram API response
    """
```

## Wallet Management Functions

### `add_wallet(wallet_address, blockchain)`
**Module:** All modules

Adds a wallet to the monitoring watchlist.

```python
def add_wallet(wallet_address, blockchain):
    """
    Add wallet to monitoring list.
    
    Args:
        wallet_address (str): Valid wallet address (40 hex chars)
        blockchain (str): Target blockchain identifier
        
    Side Effects:
        Appends "blockchain:address" to watched_wallets.txt
        
    Example:
        >>> add_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')
        >>> add_wallet('0x000000000000000000000000000000000000dEaD', 'pls')
    """
```

### `remove_wallet(wallet_address, blockchain)`
**Module:** All modules

Removes a wallet from the monitoring watchlist.

```python
def remove_wallet(wallet_address, blockchain):
    """
    Remove wallet from monitoring list.
    
    Args:
        wallet_address (str): Wallet address to remove
        blockchain (str): Source blockchain
        
    Side Effects:
        Removes matching line from watched_wallets.txt
        Creates temporary file during operation
        
    Example:
        >>> remove_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')
    """
```

## Token Management Functions

### `add_token(token_address, blockchain)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Adds a token contract to the monitoring list.

```python
def add_token(token_address, blockchain):
    """
    Add token to monitoring list.
    
    Args:
        token_address (str): Valid token contract address
        blockchain (str): Target blockchain identifier
        
    Side Effects:
        Appends "blockchain:address" to watched_tokens.txt
        
    Example:
        >>> add_token('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'eth')  # USDC
        >>> add_token('0x6B175474E89094C44Da98b954EedeAC495271d0F', 'eth')   # DAI
    """
```

### `remove_token(token_address, blockchain)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Removes a token from the monitoring list.

```python
def remove_token(token_address, blockchain):
    """
    Remove token from monitoring list.
    
    Args:
        token_address (str): Token contract address to remove
        blockchain (str): Source blockchain
        
    Side Effects:
        Removes matching line from watched_tokens.txt
        
    Example:
        >>> remove_token('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'eth')
    """
```

## Monitoring Functions

### `monitor_wallets()`
**Module:** All modules

Main monitoring loop that checks for new transactions and sends alerts.

```python
def monitor_wallets():
    """
    Continuous monitoring loop for wallet transactions.
    
    Functionality:
        - Loads configuration from text files
        - Fetches current cryptocurrency prices
        - Polls blockchain APIs every 60 seconds
        - Filters new transactions by timestamp/hash
        - Sends Telegram notifications
        - Updates state files
        
    State Management:
        - watched_wallets.txt: Monitored wallet list
        - watched_tokens.txt: Monitored token list (burn bots)
        - latest_tx_hashes.json: Processed transaction cache
        - last_run_time.txt: Last execution timestamp
        
    Error Handling:
        - Continues on API failures
        - 10-second retry delay on exceptions
        - Comprehensive error logging
        
    Example:
        >>> monitor_wallets()  # Runs indefinitely
    """
```

## Telegram Bot Command Handlers

### `start(update, context)`
**Module:** All modules

Handles `/start` command and displays help information.

```python
def start(update, context):
    """
    Handle /start command - show welcome and help.
    
    Args:
        update: Telegram update object
        context: Bot context object
        
    Response:
        Sends formatted help message with available commands
        
    Example:
        User: /start
        Bot: 👋 Welcome to the Ethereum and Pulsechain token burn Monitoring Bot!
             [... help text ...]
    """
```

### `addwallet(update, context)` / `add(update, context)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py` / `burnAlertBot.py`

Handles wallet addition commands.

```python
def addwallet(update, context):  # burnBot.py, NewBurnAlertBot.py
def add(update, context):        # burnAlertBot.py
    """
    Handle /addwallet or /add command.
    
    Args:
        update: Telegram update object containing message
        context: Bot context with args=[blockchain, address]
        
    Validation:
        - Checks argument count (minimum 2)
        - Validates blockchain identifier
        - Validates address format with regex
        
    Example:
        User: /addwallet ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
        Bot: Added 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42 to the list of watched ETH wallets.
    """
```

### `addtoken(update, context)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Handles token addition commands.

```python
def addtoken(update, context):
    """
    Handle /addtoken command.
    
    Args:
        update: Telegram update object
        context: Bot context with args=[blockchain, token_address]
        
    Validation:
        - Checks argument count
        - Validates blockchain support
        - Validates token address format
        
    Example:
        User: /addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
        Bot: Added 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 to the list of watched ETH tokens.
    """
```

### `removewallet(update, context)` / `remove(update, context)`
**Module:** All modules

Handles wallet removal commands.

```python
def removewallet(update, context):  # burnBot.py, NewBurnAlertBot.py
def remove(update, context):        # burnAlertBot.py
    """
    Handle /removewallet or /remove command.
    
    Args:
        update: Telegram update object
        context: Bot context with args=[blockchain, address]
        
    Example:
        User: /removewallet ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
        Bot: Removed 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42 from the list of watched ETH wallets.
    """
```

### `removetoken(update, context)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Handles token removal commands.

```python
def removetoken(update, context):
    """
    Handle /removetoken command.
    
    Args:
        update: Telegram update object
        context: Bot context with args=[blockchain, token_address]
        
    Example:
        User: /removetoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
        Bot: Removed 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 from the list of watched ETH tokens.
    """
```

### `list_wallets(update, context)`
**Module:** All modules

Lists currently monitored wallets.

```python
def list_wallets(update, context):
    """
    Handle /listwallets or /list command.
    
    Args:
        update: Telegram update object
        context: Bot context object
        
    Response Format:
        The following wallets are currently being monitored
        
        Ethereum Wallets:
        1. 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42
        2. 0x000000000000000000000000000000000000dEaD
        
        Pulse Chain Wallets:
        1. 0x9cf59EaA24072bF0Fe33Aa7a097F0EA5b3CAD13d
        
    Example:
        User: /listwallets
        Bot: [Formatted list of all monitored wallets by blockchain]
    """
```

### `list_tokens(update, context)`
**Module:** `burnBot.py`, `NewBurnAlertBot.py`

Lists currently monitored tokens.

```python
def list_tokens(update, context):
    """
    Handle /listtokens command.
    
    Args:
        update: Telegram update object
        context: Bot context object
        
    Response:
        Formatted list of monitored tokens grouped by blockchain
        
    Example:
        User: /listtokens
        Bot: The following tokens are currently being monitored
             
             Ethereum tokens:
             1. 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
             2. 0x6B175474E89094C44Da98b954EedeAC495271d0F
    """
```

## Utility Functions

### Address Validation

```python
# Built-in validation in command handlers
import re

def validate_address(address, blockchain):
    """
    Validate wallet/token address format.
    
    Args:
        address (str): Address to validate
        blockchain (str): Target blockchain
        
    Returns:
        bool: True if address format is valid
        
    Example:
        >>> is_valid = re.match(r'^0x[a-fA-F0-9]{40}$', address)
        >>> print(f"Valid address: {is_valid is not None}")
    """
```

### Price Fetching

```python
# Internal price fetching logic
def fetch_crypto_prices():
    """
    Fetch current cryptocurrency prices from CoinGecko.
    
    Returns:
        dict: Price data for supported cryptocurrencies
        
    API Endpoint:
        https://api.coingecko.com/api/v3/simple/price
        
    Supported Tokens:
        - ethereum (ETH)
        - pulsechain (PLS)
        - binancecoin (BNB) - burnAlertBot.py only
        - chainlink (LINK) - burn bots only
        - dai (DAI) - burn bots only
        - usd-coin (USDC) - burn bots only
        - tether (USDT) - burn bots only
        
    Example Response:
        {
            'ethereum': {'usd': 2500.0},
            'pulsechain': {'usd': 0.0001},
            'chainlink': {'usd': 15.0}
        }
    """
```

## File I/O Functions

### State File Management

```python
# File operations used throughout modules
def load_watched_items(file_path):
    """
    Load watched items from text file.
    
    Args:
        file_path (str): Path to watched items file
        
    Returns:
        set: Set of watched items in "blockchain:address" format
        
    Example:
        >>> wallets = load_watched_items("watched_wallets.txt")
        >>> print(f"Monitoring {len(wallets)} wallets")
    """

def save_transaction_hashes(tx_hashes, file_path):
    """
    Save processed transaction hashes to JSON file.
    
    Args:
        tx_hashes (dict): Hash to block number mapping
        file_path (str): Path to JSON file
        
    Example:
        >>> hashes = {"0x123...": 12345}
        >>> save_transaction_hashes(hashes, "latest_tx_hashes.json")
    """

def update_last_run_time(timestamp, file_path):
    """
    Update last execution timestamp.
    
    Args:
        timestamp (int): Unix timestamp
        file_path (str): Path to timestamp file
        
    Example:
        >>> import time
        >>> update_last_run_time(int(time.time()), "last_run_time.txt")
    """
```

## Bot Setup Functions

### Telegram Bot Initialization

```python
from telegram.ext import Updater, CommandHandler

def setup_telegram_bot():
    """
    Initialize Telegram bot with command handlers.
    
    Returns:
        Updater: Configured Telegram bot updater
        
    Handlers Added:
        - /start - Show help
        - /addwallet - Add wallet to monitoring
        - /addtoken - Add token to monitoring (burn bots)
        - /removewallet - Remove wallet
        - /removetoken - Remove token (burn bots)
        - /listwallets - List monitored wallets
        - /listtokens - List monitored tokens (burn bots)
        
    Example:
        >>> updater = setup_telegram_bot()
        >>> updater.start_polling()
    """
```

## Constants and Configuration

### Blockchain Identifiers

```python
SUPPORTED_BLOCKCHAINS = {
    'eth': {
        'name': 'Ethereum',
        'api_base': 'https://api.etherscan.io/api',
        'explorer': 'https://etherscan.io',
        'native_token': 'ETH'
    },
    'pls': {
        'name': 'PulseChain', 
        'api_base': 'https://scan.pulsechain.com/api',
        'explorer': 'https://scan.pulsechain.com',
        'native_token': 'PLS'
    },
    'bnb': {  # burnAlertBot.py only
        'name': 'Binance Smart Chain',
        'api_base': 'https://api.bscscan.com/api', 
        'explorer': 'https://bscscan.com',
        'native_token': 'BNB'
    }
}
```

### API Endpoints

```python
# Blockchain APIs
ETHERSCAN_API = "https://api.etherscan.io/api"
BSCSCAN_API = "https://api.bscscan.com/api"
PULSECHAIN_API = "https://scan.pulsechain.com/api"

# Price API
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

# Telegram API
TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"
```

### Regular Expressions

```python
# Address validation patterns
ETH_ADDRESS_PATTERN = r'^0x[a-fA-F0-9]{40}$'
HASH_PATTERN = r'^0x[a-fA-F0-9]{64}$'

# File format patterns
WATCHED_ITEM_PATTERN = r'^(eth|pls|bnb):0x[a-fA-F0-9]{40}$'
```

## Error Codes and Messages

### Common Error Responses

```python
ERROR_MESSAGES = {
    'invalid_blockchain': "Invalid blockchain specified: {blockchain}",
    'invalid_address': "{address} is not a valid {blockchain} address.",
    'insufficient_args': "Please provide a blockchain and address.",
    'api_error': "Error fetching data from {api}: {error}",
    'file_error': "Error accessing file {file}: {error}",
    'network_error': "Network connection failed: {error}"
}
```

### HTTP Status Codes

```python
# Expected API response codes
SUCCESS_CODES = [200, 201]
RATE_LIMIT_CODE = 429
SERVER_ERROR_CODES = [500, 502, 503, 504]
CLIENT_ERROR_CODES = [400, 401, 403, 404]
```