import json
from web3 import Web3
from pathlib import Path

base_path = Path(__file__).parent

with open(str(base_path) + "/eth-config.json") as config:
    config = json.load(config)

web3 = Web3(Web3.HTTPProvider(config["http_provider"]))
contract = web3.eth.contract(address=config["contract_address"], abi=config["contract"]["abi"])

def generate_eth_account():
    account = web3.eth.account.create()
    return { "address": account._address, "publicKey": account._private_key }

# use origin private key to sign transaction and send to the network
def send_transaction(tx, key):
    sign_tx = web3.eth.account.signTransaction(tx, private_key1)
    tx_hash = web3.eth.sendRawTransaction(sign_tx.rawTransaction)
    return tx_hash

# transfer DANC tokens from origin to destination address
def transfer(origin, origin_key, destination, amount):
    nonce = web3.eth.getTransactionCount(origin)
    tx = contract.functions.transfer(destination, amount).buildTransaction({'nonce': nonce,'from': origin})
    tx_hash = send_transaction(tx, origin_key)
    return tx_hash

print(generate_eth_account())