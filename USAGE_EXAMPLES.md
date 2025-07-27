# Usage Examples and Integration Guide

## Basic Setup and Configuration

### 1. Initial Configuration

```python
# Step 1: Configure API keys and bot token in your chosen module
# Example for burnBot.py

ETHERSCAN_API_KEY = 'UFCG3BXXNR58RSNCSFSRYWTNNTG3YW5G7B'
TELEGRAM_BOT_TOKEN = '6527224346:AAHP_gBPJ2_-qKF2j52ZjKXucahFeFNGpDE'
TELEGRAM_CHAT_ID = '@burnbotgroup'

# Step 2: Install dependencies
# pip install requests web3 python-telegram-bot

# Step 3: Run the bot
# python burnBot.py
```

### 2. File Structure Setup

```bash
# Your project directory should contain:
/blockchain-monitor/
├── burnBot.py              # Advanced burn monitoring
├── NewBurnAlertBot.py      # Enhanced burn alerts  
├── burnAlertBot.py         # Basic wallet monitoring
├── watched_wallets.txt     # Auto-created
├── watched_tokens.txt      # Auto-created (burn bots)
├── latest_tx_hashes.json   # Auto-created
├── last_run_time.txt       # Auto-created
└── tests/
    └── test_transactions.py
```

## Common Use Cases

### 1. Token Burn Monitoring

Monitor when tokens are sent to burn addresses (dead wallets).

```python
# Using burnBot.py or NewBurnAlertBot.py

# Step 1: Start the bot
python burnBot.py

# Step 2: Add burn addresses via Telegram
/addwallet ETH 0x000000000000000000000000000000000000dEaD
/addwallet PLS 0x000000000000000000000000000000000000dEaD

# Step 3: Add tokens to monitor
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  # USDC
/addtoken ETH 0x6B175474E89094C44Da98b954EedeAC495271d0F  # DAI
/addtoken PLS 0x6753560538ECa67617A9Ce605178F788bE7E524E  # PulseChain token

# Result: Bot will alert when any of these tokens are sent to burn addresses
```

**Example Alert:**
```
Token Burn transaction.
Blockchain: ETH
Burn Address: 0x000000000000000000000000000000000000dEaD
Burnt: 10,000 USDC
Worth: (~$10,000.00)
From: 0x742d35Cc6A...
[Transaction Hash Link]
```

### 2. Whale Wallet Monitoring

Track large wallet movements and transactions.

```python
# Monitor known whale wallets
/addwallet ETH 0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503  # Binance hot wallet
/addwallet ETH 0x8315177aB297bA92A06054cE80a67Ed4DBd7ed3a  # Bitfinex cold wallet
/addwallet ETH 0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42  # Whale wallet

# Monitor specific tokens on these wallets
/addtoken ETH 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  # USDC
/addtoken ETH 0xdAC17F958D2ee523a2206206994597C13D831ec7  # USDT
```

### 3. DeFi Protocol Monitoring

Monitor DeFi protocol treasuries and burn mechanisms.

```python
# Add DeFi protocol addresses
/addwallet ETH 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643  # Compound cDAI
/addwallet ETH 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7  # Curve 3pool
/addwallet ETH 0x5777d92f208679DB4b9778590Fa3CAB3AC9e2168  # Uniswap V3 USDC/ETH

# Monitor governance tokens
/addtoken ETH 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984  # UNI
/addtoken ETH 0xc00e94Cb662C3520282E6f5717214004A7f26888  # COMP
```

### 4. Project Treasury Monitoring

Track project funds and token movements.

```python
# Monitor project treasury addresses
/addwallet ETH 0x467194771dAe2967Aef3ECbEDD3Bf9a310C76C65  # Project treasury
/addwallet ETH 0x1715a3E4A142d8b698131108995174F37aEBA10D  # Marketing wallet

# Add project token
/addtoken ETH 0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE  # SHIB (example)
```

## Advanced Integration Examples

### 1. Custom Alert Processing

```python
# Extend the notification system for custom processing
import json
from burnBot import send_telegram_notification

def custom_burn_alert(tx_data):
    """
    Custom processing for burn alerts with additional logic.
    """
    value = float(tx_data['value']) / 10**18
    
    # Only alert for burns > $1000
    if tx_data['usd_value'] > 1000:
        # Custom message format
        message = f"🔥 MAJOR BURN ALERT 🔥\n"
        
        # Send enhanced notification
        response = send_telegram_notification(
            message=message,
            value=value,
            usd_value=tx_data['usd_value'],
            tx_hash=tx_data['hash'],
            blockchain=tx_data['blockchain'],
            w_from=tx_data['from'],
            w_to=tx_data['to'],
            token_symbol=tx_data['tokenSymbol']
        )
        
        # Log to custom database
        log_burn_event(tx_data)
        
    return response

def log_burn_event(tx_data):
    """
    Log burn event to external system.
    """
    burn_log = {
        'timestamp': tx_data['timeStamp'],
        'blockchain': tx_data['blockchain'],
        'token': tx_data['tokenSymbol'],
        'amount': tx_data['value'],
        'usd_value': tx_data['usd_value'],
        'tx_hash': tx_data['hash']
    }
    
    # Save to database or send to analytics service
    with open('burn_events.json', 'a') as f:
        f.write(json.dumps(burn_log) + '\n')
```

### 2. Multi-Blockchain Price Monitoring

```python
# Extended price monitoring for multiple tokens
import requests

def get_extended_prices():
    """
    Fetch prices for additional tokens beyond the default set.
    """
    extended_url = (
        'https://api.coingecko.com/api/v3/simple/price?'
        'ids=ethereum,pulsechain,chainlink,dai,usd-coin,tether,'
        'uniswap,compound-governance-token,aave,maker&vs_currencies=usd'
    )
    
    response = requests.get(extended_url)
    return response.json()

def calculate_burn_impact(token_symbol, burn_amount, total_supply):
    """
    Calculate the impact of a burn on token supply.
    """
    burn_percentage = (burn_amount / total_supply) * 100
    
    if burn_percentage > 0.1:  # More than 0.1% of supply burned
        return f"🚨 SIGNIFICANT BURN: {burn_percentage:.2f}% of total supply!"
    elif burn_percentage > 0.01:  # More than 0.01% of supply burned
        return f"⚠️ Notable burn: {burn_percentage:.4f}% of supply"
    else:
        return f"Minor burn: {burn_percentage:.6f}% of supply"
```

### 3. Historical Data Analysis

```python
# Analyze historical burn data
import json
from datetime import datetime, timedelta

def analyze_burn_patterns():
    """
    Analyze burn patterns from historical data.
    """
    with open('burn_events.json', 'r') as f:
        burn_events = [json.loads(line) for line in f]
    
    # Group by token
    token_burns = {}
    for event in burn_events:
        token = event['token']
        if token not in token_burns:
            token_burns[token] = []
        token_burns[token].append(event)
    
    # Calculate statistics
    for token, burns in token_burns.items():
        total_burned = sum(float(burn['amount']) for burn in burns)
        total_usd = sum(burn['usd_value'] for burn in burns)
        avg_burn = total_burned / len(burns) if burns else 0
        
        print(f"{token}: {len(burns)} burns, {total_burned:.2f} tokens (${total_usd:.2f})")
        print(f"  Average burn: {avg_burn:.2f} tokens")

def get_burn_frequency(token_symbol, days=30):
    """
    Calculate burn frequency for a specific token.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    with open('burn_events.json', 'r') as f:
        recent_burns = []
        for line in f:
            event = json.loads(line)
            event_date = datetime.fromtimestamp(int(event['timestamp']))
            
            if (event['token'] == token_symbol and 
                event_date > cutoff_date):
                recent_burns.append(event)
    
    return len(recent_burns), sum(b['usd_value'] for b in recent_burns)
```

## Programmatic Usage Examples

### 1. Direct Function Usage

```python
# Import functions directly (not recommended for production)
import sys
sys.path.append('.')

from burnBot import (
    get_wallet_transactions, 
    add_wallet, 
    send_telegram_notification
)

# Get transaction history programmatically
def check_wallet_activity(wallet_address, blockchain='eth'):
    """
    Check recent activity for a wallet.
    """
    # For burn bots, you need to specify a token address too
    token_address = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'  # USDC
    
    transactions = get_wallet_transactions(
        wallet_address=wallet_address,
        token_address=token_address,
        blockchain=blockchain
    )
    
    print(f"Found {len(transactions)} transactions for {wallet_address}")
    
    # Process recent transactions
    for tx in transactions[:5]:  # Last 5 transactions
        value = float(tx['value']) / 10**18
        print(f"  {tx['hash'][:10]}... - {value:.2f} {tx['tokenSymbol']}")
    
    return transactions

# Add multiple wallets programmatically
def bulk_add_wallets(wallet_list, blockchain='eth'):
    """
    Add multiple wallets to monitoring.
    """
    for wallet in wallet_list:
        try:
            add_wallet(wallet, blockchain)
            print(f"✅ Added {wallet}")
        except Exception as e:
            print(f"❌ Failed to add {wallet}: {e}")

# Example usage
if __name__ == "__main__":
    # Check activity
    check_wallet_activity('0x000000000000000000000000000000000000dEaD')
    
    # Bulk add burn addresses
    burn_addresses = [
        '0x000000000000000000000000000000000000dEaD',
        '0x0000000000000000000000000000000000000001',
        '0x0000000000000000000000000000000000000002'
    ]
    bulk_add_wallets(burn_addresses, 'eth')
```

### 2. Web API Integration

```python
# Create a simple web API for monitoring data
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/monitored-wallets')
def get_monitored_wallets():
    """
    API endpoint to get currently monitored wallets.
    """
    with open('watched_wallets.txt', 'r') as f:
        wallets = [line.strip().split(':') for line in f.readlines()]
    
    result = {}
    for blockchain, address in wallets:
        if blockchain not in result:
            result[blockchain] = []
        result[blockchain].append(address)
    
    return jsonify(result)

@app.route('/api/recent-burns')
def get_recent_burns():
    """
    API endpoint to get recent burn events.
    """
    try:
        with open('burn_events.json', 'r') as f:
            burns = [json.loads(line) for line in f.readlines()[-10:]]
        return jsonify(burns)
    except FileNotFoundError:
        return jsonify([])

@app.route('/api/burn-stats')
def get_burn_stats():
    """
    API endpoint for burn statistics.
    """
    try:
        with open('burn_events.json', 'r') as f:
            burns = [json.loads(line) for line in f.readlines()]
        
        total_burns = len(burns)
        total_usd = sum(burn['usd_value'] for burn in burns)
        
        # Group by token
        token_stats = {}
        for burn in burns:
            token = burn['token']
            if token not in token_stats:
                token_stats[token] = {'count': 0, 'total_usd': 0}
            token_stats[token]['count'] += 1
            token_stats[token]['total_usd'] += burn['usd_value']
        
        return jsonify({
            'total_burns': total_burns,
            'total_value_usd': total_usd,
            'by_token': token_stats
        })
    except FileNotFoundError:
        return jsonify({'error': 'No burn data available'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. Database Integration

```python
# Integrate with SQLite database
import sqlite3
import json
from datetime import datetime

class BurnDatabase:
    def __init__(self, db_path='burns.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Initialize database schema.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS burn_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                blockchain TEXT NOT NULL,
                token_symbol TEXT NOT NULL,
                amount REAL NOT NULL,
                usd_value REAL NOT NULL,
                tx_hash TEXT UNIQUE NOT NULL,
                from_address TEXT NOT NULL,
                to_address TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_burn(self, tx_data):
        """
        Log a burn event to database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO burn_events 
                (timestamp, blockchain, token_symbol, amount, usd_value, 
                 tx_hash, from_address, to_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tx_data['timestamp'],
                tx_data['blockchain'],
                tx_data['tokenSymbol'],
                float(tx_data['value']) / 10**18,
                tx_data['usd_value'],
                tx_data['hash'],
                tx_data['from'],
                tx_data['to']
            ))
            conn.commit()
            print(f"✅ Logged burn: {tx_data['hash']}")
        except sqlite3.IntegrityError:
            print(f"⚠️ Burn already exists: {tx_data['hash']}")
        finally:
            conn.close()
    
    def get_recent_burns(self, limit=10):
        """
        Get recent burn events.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM burn_events 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        burns = cursor.fetchall()
        conn.close()
        
        return burns
    
    def get_token_stats(self, token_symbol):
        """
        Get statistics for a specific token.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as burn_count,
                SUM(amount) as total_burned,
                SUM(usd_value) as total_usd_value,
                AVG(amount) as avg_burn_amount,
                MIN(timestamp) as first_burn,
                MAX(timestamp) as last_burn
            FROM burn_events 
            WHERE token_symbol = ?
        ''', (token_symbol,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'token': token_symbol,
            'burn_count': stats[0],
            'total_burned': stats[1],
            'total_usd_value': stats[2],
            'avg_burn_amount': stats[3],
            'first_burn': stats[4],
            'last_burn': stats[5]
        }

# Usage example
db = BurnDatabase()

# Example burn event
burn_event = {
    'timestamp': '1640995200',
    'blockchain': 'eth',
    'tokenSymbol': 'USDC',
    'value': '1000000000000000000000',  # 1000 USDC in wei
    'usd_value': 1000.0,
    'hash': '0x123456789abcdef',
    'from': '0xsender...',
    'to': '0x000000000000000000000000000000000000dEaD'
}

db.log_burn(burn_event)
stats = db.get_token_stats('USDC')
print(f"USDC burns: {stats}")
```

## Testing and Validation

### 1. Unit Testing

```python
# Enhanced unit testing
import unittest
from unittest.mock import patch, MagicMock
import json

class TestBurnBot(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_wallet_transactions_success(self, mock_get):
        """
        Test successful transaction fetching.
        """
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': [
                {
                    'hash': '0x123',
                    'from': '0xabc',
                    'to': '0xdef',
                    'value': '1000000000000000000',
                    'timeStamp': '1640995200',
                    'blockNumber': '13916165',
                    'tokenSymbol': 'USDC'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Import function dynamically to avoid execution
        from burnBot import get_wallet_transactions
        
        # Test function
        result = get_wallet_transactions(
            '0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42',
            '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
            'eth'
        )
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['hash'], '0x123')
    
    def test_address_validation(self):
        """
        Test address validation regex.
        """
        import re
        
        valid_addresses = [
            '0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42',
            '0x000000000000000000000000000000000000dEaD',
            '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
        ]
        
        invalid_addresses = [
            '742d35Cc6AB4B6b52D654654654654654654Cc6Af42',  # Missing 0x
            '0x742d35Cc6AB4B6b52D654654654654654654Cc6A',    # Too short
            '0x742d35Cc6AB4B6b52D654654654654654654Cc6Af424', # Too long
            '0xGGGG35Cc6AB4B6b52D654654654654654654Cc6Af42'   # Invalid chars
        ]
        
        pattern = r'^0x[a-fA-F0-9]{40}$'
        
        for addr in valid_addresses:
            self.assertTrue(re.match(pattern, addr), f"Should be valid: {addr}")
        
        for addr in invalid_addresses:
            self.assertFalse(re.match(pattern, addr), f"Should be invalid: {addr}")
    
    @patch('builtins.open', create=True)
    def test_file_operations(self, mock_open):
        """
        Test file read/write operations.
        """
        from burnBot import add_wallet
        
        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Test adding wallet
        add_wallet('0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42', 'eth')
        
        # Verify file was opened in append mode
        mock_open.assert_called_with('watched_wallets.txt', 'a')
        mock_file.write.assert_called_with('eth:0x742d35Cc6AB4B6b52D654654654654654654Cc6Af42\n')

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Testing

```python
# Integration test with real APIs (use sparingly)
import requests
import time

def test_api_connectivity():
    """
    Test connectivity to external APIs.
    """
    print("Testing API connectivity...")
    
    # Test Etherscan API
    try:
        etherscan_url = "https://api.etherscan.io/api?module=stats&action=ethsupply&apikey=YourAPIKey"
        response = requests.get(etherscan_url, timeout=10)
        print(f"✅ Etherscan API: {response.status_code}")
    except Exception as e:
        print(f"❌ Etherscan API: {e}")
    
    # Test CoinGecko API
    try:
        coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(coingecko_url, timeout=10)
        print(f"✅ CoinGecko API: {response.status_code}")
        print(f"   ETH Price: ${response.json()['ethereum']['usd']}")
    except Exception as e:
        print(f"❌ CoinGecko API: {e}")
    
    # Test Telegram Bot API (if token configured)
    # Note: This sends a test message
    try:
        bot_token = "YOUR_BOT_TOKEN"
        chat_id = "YOUR_CHAT_ID" 
        telegram_url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(telegram_url, timeout=10)
        print(f"✅ Telegram Bot API: {response.status_code}")
    except Exception as e:
        print(f"❌ Telegram Bot API: {e}")

if __name__ == "__main__":
    test_api_connectivity()
```

## Performance Optimization Examples

### 1. Concurrent API Calls

```python
# Optimize API calls with concurrent requests
import asyncio
import aiohttp
import time

async def fetch_transactions_async(session, wallet_address, token_address, blockchain):
    """
    Asynchronous transaction fetching.
    """
    if blockchain == 'eth':
        url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token_address}&address={wallet_address}&sort=desc&apikey={ETHERSCAN_API_KEY}'
    elif blockchain == 'pls':
        url = f'https://scan.pulsechain.com/api?module=account&action=tokentx&contractaddress={token_address}&address={wallet_address}'
    
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data.get('result', [])
    except Exception as e:
        print(f"Error fetching {wallet_address}: {e}")
        return []

async def monitor_wallets_async():
    """
    Async version of wallet monitoring for better performance.
    """
    # Load watched items
    with open('watched_wallets.txt', 'r') as f:
        watched_wallets = set(f.read().splitlines())
    with open('watched_tokens.txt', 'r') as f:
        watched_tokens = set(f.read().splitlines())
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # Create tasks for all wallet-token combinations
        for wallet in watched_wallets:
            wallet_blockchain, wallet_address = wallet.split(':')
            for token in watched_tokens:
                token_blockchain, token_address = token.split(':')
                if token_blockchain == wallet_blockchain:
                    task = fetch_transactions_async(
                        session, wallet_address, token_address, wallet_blockchain
                    )
                    tasks.append((task, wallet_address, token_address, wallet_blockchain))
        
        # Execute all tasks concurrently
        print(f"Fetching data for {len(tasks)} wallet-token pairs...")
        start_time = time.time()
        
        for task, wallet_addr, token_addr, blockchain in tasks:
            transactions = await task
            # Process transactions here
            print(f"Wallet {wallet_addr[:10]}...: {len(transactions)} transactions")
        
        elapsed = time.time() - start_time
        print(f"Completed in {elapsed:.2f} seconds")

# Run async monitoring
if __name__ == "__main__":
    asyncio.run(monitor_wallets_async())
```

### 2. Caching and Rate Limiting

```python
# Implement caching and rate limiting
import time
from functools import wraps
import pickle
import os

class RateLimiter:
    def __init__(self, max_calls_per_second=5):
        self.max_calls = max_calls_per_second
        self.calls = []
    
    def wait_if_needed(self):
        now = time.time()
        # Remove calls older than 1 second
        self.calls = [call_time for call_time in self.calls if now - call_time < 1]
        
        if len(self.calls) >= self.max_calls:
            sleep_time = 1 - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(now)

class TransactionCache:
    def __init__(self, cache_file='tx_cache.pkl', ttl=300):  # 5 minute TTL
        self.cache_file = cache_file
        self.ttl = ttl
        self.cache = self.load_cache()
    
    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, time.time())
        self.save_cache()

# Rate limiter instances
etherscan_limiter = RateLimiter(5)  # 5 calls per second
coingecko_limiter = RateLimiter(10)  # 10 calls per second

# Cache instance
tx_cache = TransactionCache()

def rate_limited_request(limiter):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limited_request(etherscan_limiter)
def cached_get_wallet_transactions(wallet_address, token_address, blockchain):
    """
    Cached and rate-limited version of get_wallet_transactions.
    """
    cache_key = f"{blockchain}:{wallet_address}:{token_address}"
    
    # Check cache first
    cached_result = tx_cache.get(cache_key)
    if cached_result is not None:
        print(f"Cache hit for {wallet_address[:10]}...")
        return cached_result
    
    # Fetch from API
    print(f"Fetching from API: {wallet_address[:10]}...")
    result = get_wallet_transactions(wallet_address, token_address, blockchain)
    
    # Cache result
    tx_cache.set(cache_key, result)
    
    return result
```

This comprehensive documentation provides:

1. **Complete API documentation** with all public functions, parameters, and examples
2. **Detailed function reference** with code signatures and usage patterns  
3. **Practical usage examples** covering common scenarios like burn monitoring, whale tracking, and DeFi protocol monitoring
4. **Advanced integration examples** showing custom alert processing, web API creation, and database integration
5. **Testing frameworks** with unit tests and integration tests
6. **Performance optimization** techniques including async operations and caching

The documentation covers all three main modules (`burnBot.py`, `NewBurnAlertBot.py`, and `burnAlertBot.py`) and provides both beginner-friendly examples and advanced integration patterns for developers who want to extend the functionality.