# This is for deploying the new smart contract after a rebuild

import json
from web3 import Web3

with open("config.json") as config:
    config = json.load(config)

with open("../build/contracts/DANC.json") as contract_config:
    contract_config = json.load(contract_config)

web3 = Web3(Web3.HTTPProvider(config["http_provider"]))

test_account1_address = config["test_accounts"]["account1"]["address"]
test_account1_private_key = config["test_accounts"]["account1"]["key"]

contract = web3.eth.contract(bytecode=contract_config["bytecode"], abi=contract_config["abi"])
    
nonce = web3.eth.getTransactionCount(test_account1_address)
tx = contract.constructor(test_account1_address).buildTransaction({'nonce': nonce})

sign_tx = web3.eth.account.signTransaction(tx, test_account1_private_key)
tx_hash = web3.eth.sendRawTransaction(sign_tx.rawTransaction)
print(tx_hash)

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)