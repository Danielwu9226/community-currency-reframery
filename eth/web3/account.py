import json
from web3 import Web3
with open("config.json") as config:
    config = json.load(config)

web3 = Web3(Web3.HTTPProvider(config["http_provider"]))

def create_eth_account():
    account = web3.eth.account.create()
    return { "address": account._address, "publicKey": account._private_key }