import json
from web3 import Web3

with open("config.json") as config:
    config = json.load(config)

with open("../build/contracts/DANC.json") as contract_config:
    contract_config = json.load(contract_config)

# Connect to ethereum node specified in config file
web3 = Web3(Web3.HTTPProvider(config["http_provider"]))
# Get the deployed DANC erc20 ethereum contract
contract = web3.eth.contract(address=config["contract_address"], abi=contract_config["abi"])

def send_transaction(tx, key):
    """
    :description: Use the sender's private key to sign transaction and send to network
    :param tx: Transaction to be sent
    :param key: Sender's Etherem private key
    :return: Transaction hash. This can be used to look up the transaction in the blockchain.
    """
    sign_tx = web3.eth.account.signTransaction(tx, key)
    tx_hash = web3.eth.sendRawTransaction(sign_tx.rawTransaction)
    return tx_hash


def transfer(senderAddress, senderPrivateKey, receiverAddress, amount):
    """
    :description: Transfer DANC tokens from sender wallet to receiver wallet
    :param senderAddress: Sender's ethereum address
    :param senderPrivateKey: Sender's etherem private key
    :param receiverAddress: Receiver's etherem address
    :param amount: Amount of DANC tokens to send
    :return: transaction hash. This can be used to look up the transaction in the blockchain.
    """
    # get the nonce of the sender's ethereum account
    nonce = web3.eth.getTransactionCount(senderAddress)

    # build the transaction to be sent to the network
    tx = contract.functions.transfer(receiverAddress, amount).buildTransaction({'nonce': nonce,'from': senderAddress})

    tx_hash = send_transaction(tx, senderPrivateKey)
    return tx_hash
