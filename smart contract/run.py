import json
from web3 import Web3, HTTPProvider
import sys

# setup web3 instance using ganache
ganache_url = "http://127.0.0.1:8545"
w3 = Web3(HTTPProvider(ganache_url))
if w3.isConnected():
    print("Web3 Connected")
else:
    sys.exit("Couldn't connect to the blockchain via web3")
# set default account
w3.eth.defaultAccount = w3.eth.accounts[0]

# contract details
contract_path = './truffle/build/contracts/oceanCoin.json'
contract_address = '0x224BbB49A2c9b432A6806Ab3177Ee1b859129bE6'

# open compiled file and get abi & bytecode
truffleFile = json.load(open(contract_path))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# contract interface
oceanCoin = w3.eth.contract(address=contract_address, abi=abi)
