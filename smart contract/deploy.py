import json
from web3 import Web3, HTTPProvider
import sys
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import random
import hashlib
from operator import itemgetter

# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------

# contract details
contract_path = './truffle/build/contracts/oceanCoin.json'

# open compiled file and get abi & bytecode
truffleFile = json.load(open(contract_path))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# setup web3 instance using ganache
ganache_url = "http://127.0.0.1:8545"
w3 = Web3(HTTPProvider(ganache_url))
if w3.isConnected():
    print("Web3 Connected")
else:
    sys.exit("Couldn't connect to the blockchain via web3")
# set default account
w3.eth.defaultAccount = w3.eth.accounts[0]

# instanciate contract
OceanCoin = w3.eth.contract(abi=abi, bytecode=bytecode)
# deploy contract (call constructor)
tx_hash = OceanCoin.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract deployed at address: {} and block: {}"
      .format(tx_receipt.contractAddress, w3.eth.blockNumber))
contractAddress = tx_receipt.contractAddress

print(contractAddress)

# contract interface
#oceanCoin = w3.eth.contract(address=contractAddress, abi=abi)
