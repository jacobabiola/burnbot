import requests
import json
import time
import os.path
import re
from web3 import Web3

# Update the following variables with your own Etherscan and Telegram group ID keys and Telegram bot token
ETHERSCAN_API_KEY = '...B'  

TELEGRAM_BOT_TOKEN = '...'
TELEGRAM_CHAT_ID = '@..'




# Define some helper functions
def get_wallet_transactions(wallet_address, token_address, blockchain):
    if blockchain == 'eth':
        url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token_address}&address={wallet_address}&sort=desc&apikey={ETHERSCAN_API_KEY}'
    
    elif blockchain == 'pls':
        url = f'https://scan.pulsechain.com/api?module=account&action=tokentx&contractaddress={token_address}&address={wallet_address}'
    else:
        raise ValueError('Invalid blockchain specified')

    response = requests.get(url)
    data = json.loads(response.text)

    result = data.get('result', [])
    if not isinstance(result, list):
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error fetching transactions for {wallet_address} with {token_address} on {blockchain.upper()} blockchain: {data}")
        return []

    return result


def send_telegram_notification(message, value, usd_value, tx_hash, blockchain, w_from, w_to,token_symbol):
    kisa = w_from[:12] + '...' + w_from[-3:]
    lisa = w_to[:12] + '...' + w_to[-3:]
    if blockchain == 'eth':
        from_wallet = f'<a href="https://etherscan.io/address/{w_from}">{kisa}</a>'
        to = f'<a href="https://etherscan.io/address/{w_to}">{lisa}</a>'
        etherscan_link = f'<a href="https://etherscan.io/tx/{tx_hash}">Tx hash</a>'
        token= 'ETH'
   
    elif blockchain == 'pls':
        value = int(value)
        value = "{:,}".format(value)
        from_wallet = f'<a href="https://scan.pulsechain.com/address/{w_from}">{kisa}</a>'
        to = f'<a href="https://scan.pulsechain.com/address/{w_to}">{lisa}</a>'
        etherscan_link = f'<a href="https://scan.pulsechain.com/tx/{tx_hash}">Tx hash</a>'
        token = 'PLS'
    else:
        raise ValueError('Invalid blockchain specified')


    ausd_value = "{:,.2f}".format(usd_value)

    message = f'Token Burn transaction. \n' \
              f'Blockchain: {blockchain.upper()} \n' \
              f'Burn Address: {to} \n' \
              f'Burnt: {value} {token_symbol} \n' \
              f'Worth: (~${ausd_value})  \n' \
              f'From: {from_wallet} \n' \
              f'{etherscan_link}'


    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': f'{TELEGRAM_CHAT_ID}',
               'text': f'{message}',
               'disable_web_page_preview': True,
               'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    print(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Telegram notification sent with message: {message}.")
    return response


def monitor_wallets():
    watched_wallets = set()
    file_path = "watched_wallets.txt"
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    watched_tokens = set()
    file_path = "watched_tokens.txt"
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    latest_tx_hashes = {}
    latest_tx_hashes_path = "latest_tx_hashes.json"
    if os.path.exists(latest_tx_hashes_path):
        with open(latest_tx_hashes_path, "r") as f:
            latest_tx_hashes = json.load(f)

    last_run_time = 0
    last_run_time_path = "last_run_time.txt"
    if os.path.exists(last_run_time_path):
        with open(last_run_time_path, "r") as f:
            last_run_time = int(f.read())

    while True:
        try:
            # Fetch current token prices from CoinGecko API
            eth_usd_price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum%2Cpulsechain%2Cchainlink%2Cdai%2Cusd-coin%2Ctether&vs_currencies=usd'
            response = requests.get(eth_usd_price_url)
            data = json.loads(response.text)
            eth_usd_price = data['ethereum']['usd']
           
            pls_usd_price = data['pulsechain']['usd']
            link_usd_price = data['chainlink']['usd']
            dai_usd_price = data['dai']['usd']
            usdc_usd_price = data['usd-coin']['usd']
            usdt_usd_price = data['tether']['usd']


            # Read from file
            with open("watched_wallets.txt", 'r') as f:
                watched_wallets = set(f.read().splitlines())
            # Read from file
            with open("watched_tokens.txt", 'r') as f:
                watched_tokens = set(f.read().splitlines())

            for wallet in watched_wallets:
                blockchain, wallet_address = wallet.split(':')
            for token in watched_tokens:
                blockchain, token_address = token.split(':')
                transactions = get_wallet_transactions(wallet_address, token_address, blockchain)

                for tx in transactions:
                    if blockchain == 'pls':
                        tx_hash = tx['blockHash']
                    else:
                        tx_hash = tx['hash']
                    tx_time = int(tx['timeStamp'])
                    if blockchain == 'eth':
                        price = eth_usd_price
                        token = 'ETH'
                    elif blockchain == "eth":
                        price = dai_usd_price
                        token = 'DAI'
                    elif blockchain == "eth":
                        price = link_usd_price
                        token = 'LINK'
                    elif blockchain == "eth":
                        price = usdc_usd_price
                        token = 'USDC'
                    elif blockchain == "eth":
                        price = usdt_usd_price
                        token = 'USDT'
                 
                    elif blockchain == "pls":
                        price = pls_usd_price
                        token = 'PLS'
                 
                    else:
                        raise ValueError('Invalid blockchain specified')
                        
                    if tx_hash not in latest_tx_hashes and tx_time > last_run_time:
                        if tx['to'].lower() == wallet_address.lower():
                            value = float(tx['value']) / 10 ** 18  # Convert from wei to ETH or BNB
                            usd_value = value * price  # Calculate value in USD
                            message = f'🚨 Incoming transaction detected on {wallet_address}'
                            send_telegram_notification(message, value, usd_value, tx['hash'], blockchain,tx['from'],tx['to'], tx['tokenSymbol'])
                            latest_tx_hashes[tx_hash] = int(tx['blockNumber'])

                        elif tx['from'].lower() == token_address.lower():
                            value = float(tx['value']) / 10 ** 18  # Convert from wei to ETH or BNB
                            usd_value = value * price  # Calculate value in USD
                            message = f'🚨 Outgoing transaction detected on {token_address}'
                            send_telegram_notification(message, value, usd_value, tx['hash'], blockchain,tx['from'],tx['to'], tx['tokenSymbol'])
                            latest_tx_hashes[tx_hash] = int(tx['blockNumber'])


                  


            # Save latest_tx_hashes to file
            with open(latest_tx_hashes_path, "w") as f:
                json.dump(latest_tx_hashes, f)

            # Update last_run_time
            last_run_time = int(time.time())
            with open(last_run_time_path, "w") as f:
                f.write(str(last_run_time))

            # Sleep for 1 minute
            time.sleep(60)
        except Exception as e:
            print(f'An error occurred: {e}')
            # Sleep for 10 seconds before trying again
            time.sleep(10)


def add_wallet(wallet_address, blockchain):
    file_path = "watched_wallets.txt"
    with open(file_path, 'a') as f:
        f.write(f'{blockchain}:{wallet_address}\n')


def remove_wallet(wallet_address, blockchain):
    file_path = "watched_wallets.txt"
    temp_file_path = "temp.txt"
    with open(file_path, 'r') as f, open(temp_file_path, 'w') as temp_f:
        for line in f:
            if line.strip() != f'{blockchain}:{wallet_address}':
                temp_f.write(line)
    os.replace(temp_file_path, file_path)

def add_token(token_address, blockchain):
    file_path = "watched_tokens.txt"
    with open(file_path, 'a') as f:
        f.write(f'{blockchain}:{token_address}\n')


def remove_token(token_address, blockchain):
    file_path = "watched_tokens.txt"
    temp_file_path = "temp.txt"
    with open(file_path, 'r') as f, open(temp_file_path, 'w') as temp_f:
        for line in f:
            if line.strip() != f'{blockchain}:{token_address}':
                temp_f.write(line)
    os.replace(temp_file_path, file_path)


# Define the command handlers for the Telegram bot
def start(update, context):
    message = """
👋 Welcome to the Ethereum and Pulsechain token burn Monitoring Bot!

Use /addwallet <blockchain> <wallet_address> to add a new wallet to monitor.
Use /addtoken <blockchain> <token_address> to add a new token to monitor.

Example: /addwallet ETH 0x123456789abcdef
Example: /addtoken ETH 0x123456789abcdef

Example: /addwallet PLS 0x123456789abcdef
Example: /addtoken PLS 0x123456789abcdef

Use /removewallet <blockchain> <wallet_address> to stop monitoring a wallet.
Use /removetoken <blockchain> <token_address> to stop monitoring a token.

Example: /removewallet ETH 0x123456789abcdef
Example: /removetoken ETH 0x123456789abcdef


Use /listwallets <blockchain> to list all wallets being monitored for a specific blockchain.
Use /listtokens <blockchain> to list all tokens being monitored for a specific blockchain.

Example: /listwallets ETH or just /listwallet
Example: /listtokens ETH or just /listtoken
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def addwallet(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please provide a blockchain and wallet address to add.")
        return

    blockchain = context.args[0].lower()
    wallet_address = context.args[1]

    # Check if the wallet address is in the correct format for the specified blockchain
    if blockchain == 'eth':
        if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet_address):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{wallet_address} is not a valid Ethereum wallet address.")
            return
   

    elif blockchain == 'pls':
        if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet_address):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{wallet_address} is not a valid PulseChain wallet address.")
            return
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Invalid blockchain specified: {blockchain}")
        return

    add_wallet(wallet_address, blockchain)
    message = f'Added {wallet_address} to the list of watched {blockchain.upper()} wallets.'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)




def removewallet(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please provide a blockchain and wallet address to remove.\nUsage: /remove ETH 0x123456789abcdef")
        return
    blockchain = context.args[0].lower()
    wallet_address = context.args[1]
    remove_wallet(wallet_address, blockchain)
    message = f'Removed {wallet_address} from the list of watched {blockchain.upper()} wallets.'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def addtoken(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please provide a blockchain and token address to add.")
        return

    blockchain = context.args[0].lower()
    token_address = context.args[1]

    # Check if the wallet address is in the correct format for the specified blockchain
    if blockchain == 'eth':
        if not re.match(r'^0x[a-fA-F0-9]{40}$', token_address):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{token_address} is not a valid Ethereum token address.")
            return
   

    elif blockchain == 'pls':
        if not re.match(r'^0x[a-fA-F0-9]{40}$', token_address):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{token_address} is not a valid PulseChain token address.")
            return
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Invalid blockchain specified: {blockchain}")
        return

    add_token(token_address, blockchain)
    message = f'Added {token_address} to the list of watched {blockchain.upper()} tokens.'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)




def removetoken(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please provide a blockchain and token address to remove.\nUsage: /remove ETH 0x123456789abcdef")
        return
    blockchain = context.args[0].lower()
    token_address = context.args[1]
    remove_token(token_address, blockchain)
    message = f'Removed {token_address} from the list of watched {blockchain.upper()} tokens.'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)



def list_wallets(update, context):
    with open("watched_wallets.txt", "r") as f:
        wallets = [line.strip() for line in f.readlines()]
    if wallets:
        eth_wallets = []
        bnb_wallets = []
        pulsechain_wallets = []
        for wallet in wallets:
            blockchain, wallet_address = wallet.split(':')
            if blockchain == 'eth':
                eth_wallets.append(wallet_address)
            
            elif blockchain == 'pls':
                pulsechain_wallets.append(wallet_address)

        message = "The following wallets are currently being monitored\n"
        message += "\n"
        if eth_wallets:
            message += "Ethereum Wallets:\n"
            for i, wallet in enumerate(eth_wallets):
                message += f"{i + 1}. {wallet}\n"
            message += "\n"
   
        if pulsechain_wallets:
            message += "Pulse Chain Wallets:\n"
            for i, wallet in enumerate(pulsechain_wallets):
                message += f"{i + 1}. {wallet}\n"
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        message = "There are no wallets currently being monitored."
        context.bot.send_message(chat_id=update.message.chat_id, text=message)


def list_tokens(update, context):
    with open("watched_tokens.txt", "r") as f:
        tokens = [line.strip() for line in f.readlines()]
    if tokens:
        eth_tokens = []
        bnb_tokens = []
        pulsechain_tokens = []
        for token in tokens:
            blockchain, token_address = token.split(':')
            if blockchain == 'eth':
                eth_tokens.append(token_address)
            
            elif blockchain == 'pls':
                pulsechain_tokens.append(token_address)

        message = "The following tokens are currently being monitored\n"
        message += "\n"
        if eth_tokens:
            message += "Ethereum tokens:\n"
            for i, token in enumerate(eth_tokens):
                message += f"{i + 1}. {token}\n"
            message += "\n"
   
        if pulsechain_tokens:
            message += "Pulse Chain Tokens:\n"
            for i, token in enumerate(pulsechain_tokens):
                message += f"{i + 1}. {token}\n"
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        message = "There are no tokens currently being monitored."
        context.bot.send_message(chat_id=update.message.chat_id, text=message)


# Set up the Telegram bot
from telegram.ext import Updater, CommandHandler

updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the command handlers
start_handler = CommandHandler('start', start)
addwallet_handler = CommandHandler('addwallet', addwallet)
addtoken_handler = CommandHandler('addtoken', addtoken)
removewallet_handler = CommandHandler('removewallet', removewallet)
removetoken_handler = CommandHandler('removetoken', removetoken)
listwallet_handler = CommandHandler('listwallets', list_wallets)
listtoken_handler = CommandHandler('listtokens', list_tokens)

# Add the command handlers to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(addwallet_handler)
dispatcher.add_handler(addtoken_handler)
dispatcher.add_handler(removewallet_handler)
dispatcher.add_handler(removetoken_handler)
dispatcher.add_handler(listwallet_handler)
dispatcher.add_handler(listtoken_handler)

updater.start_polling()
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Telegram bot started.")

print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Monitoring wallets...")
monitor_wallets()