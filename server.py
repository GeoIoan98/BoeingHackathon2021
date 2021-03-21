import json
from web3 import Web3, HTTPProvider
import sys
from flask import Flask, render_template


# ----- Connect to smart contract -----

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
contract_path = './SmartContract/truffle/build/contracts/oceanCoin.json'
fp=open('./SmartContract/address.dat', 'r')
contract_address = fp.read()
fp.close()
print("Contract Address: ", contract_address)

# open compiled file and get abi & bytecode
truffleFile = json.load(open(contract_path))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# contract interface
oceanCoin = w3.eth.contract(address=contract_address, abi=abi)

# add auction 0
tx_hash = oceanCoin.functions.startAuction(100).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# add auction 1
tx_hash = oceanCoin.functions.startAuction(100).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)


# ----- Set up server -----

app = Flask(__name__, static_folder='FrontEnd/static', template_folder='FrontEnd/templates')

@app.route('/')
@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/organisation')
def hello():
    return render_template('organisation.html', contract_address = oceanCoin.address.lower(), contractABI = json.dumps(abi))

@app.route('/volunteer')
def testing():
    return render_template('volunteer.html', contract_address = oceanCoin.address.lower(), contractABI = json.dumps(abi))

@app.route('/store')
def store():
    return render_template('store.html', contract_address = oceanCoin.address.lower(), contractABI = json.dumps(abi))

@app.route('/leaderboard')
def leader():
    return render_template('leaderboard.html', contract_address = oceanCoin.address.lower(), contractABI = json.dumps(abi))

if __name__ == '__main__':
    app.run()
