# Cryptocurrency Wallet

# Imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()
from bip44 import Wallet
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

# Wallet functionality


def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


def send_transaction(w3, account, to, wage):
    value = w3.toWei(wage, 'ether')

    block = w3.eth.get_block('latest')
    if 'baseFeePerGas' in block:
        base_fee = int(block['baseFeePerGas'], 16)
    else:
        base_fee = w3.toWei(1, 'gwei')

    priority_fee = w3.toWei(2, 'gwei')
    max_fee = base_fee + priority_fee
    
    gas_estimate = w3.eth.estimateGas({
        'to': to, 'from': account.address, 'value': value
    })

    transaction = {
        'type': '0x2',
        'chainId': w3.eth.chain_id,
        'from': account.address,
        'to': to,
        'value': value,
        'gas': gas_estimate,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': priority_fee,
        'nonce': w3.eth.getTransactionCount(account.address)
    }
    # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(transaction)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
