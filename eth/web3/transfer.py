import json
from web3 import Web3

with open("config.json") as config:
    config = json.load(config)

with open("../build/contracts/DANC.json") as contract_config:
    contract_config = json.load(contract_config)

# test accounts. Using ropsten test network for testing
add1 = config["test_accounts"]["account1"]["address"]
add2 = config["test_accounts"]["account2"]["address"]
private_key1 = config["test_accounts"]["account1"]["key"]

web3 = Web3(Web3.HTTPProvider(config["http_provider"]))

contract = web3.eth.contract(address=config["contract_address"], abi=contract_config["abi"])

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

# transfer(add1, private_key1, add2, 1)
# print(contract.functions.balanceOf(add1).call())