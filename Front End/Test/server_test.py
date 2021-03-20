import json
import time

from web3.auto import w3
from solc import compile_source

hash_of_123 = "0x64e604787cbf194841e7b68d7cd28786f6c9a0a3ab9f8b0a0e87cb4387ab0107"
signature_of_123_restaurant_1 = "0xfe3bf72b36651612160de3bc80bd846434563ac09562935a25bfa2227025931c071134dcb395f519f17a0e2165044d8b425ff7559633290ebcd2323b1f698d1f1b"
signature_of_123_restaurant_2 = "0xd5a964f9c960de2916635d894f1da5833c659dd340bf7d9c10773fbad4d272b516fc0cc321884c8c4eb849ab5f61a44624ffd3247ebaa3eea1de4d5ab984ce7f1b"


def make_new_contract():
    tx_hash = Competition.constructor().transact({'from':owner_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])

# Creates one competition from restaurant 1 and one competition from restaurant 2
def test_add_restaurant_to_competition(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(tx_receipt)
    tx_hash = contract.functions.add_restaurant_to_competition("Eat alone", 60).transact({'from':restaurant2_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(tx_receipt)
    print("Added one competition for two restaurants successfully")

# Tries to add same restaurant in the competition twice
def test_add_same_restaurant_to_competition(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(tx_receipt)
    try: # the string does not matter that it is the same, it fails because the restaurant address is the same
        tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to add two competitions from the same restaurant")

# Adds two customers to the same competition
def test_add_2_customers_to_competition(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(tx_receipt)
    tx_hash = contract.functions.add_customer_to_competition("Tom", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer2_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(tx_receipt)
    print("Added two customers to same competition")

# Tries to add customer that is already a restaurant running a competition
def test_add_customer_that_is_restaurant(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':restaurant1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to add customer with address of a restaurant that already has competition ongoing")

# Make expiration happen after 0 seconds(i.e. instantly) so that customer will fail to join
def test_add_customer_after_expiration(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 0).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to add customer after expiration")

# Test against replay attack - adding a customer twice in the same competition
def test_add_customer_twice(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to add customer twice in the same competition")

# Try to add customer in competitino of restaurant 1 from signature of restaurant 2
def test_signature_verification_fail(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_2).transact({'from':customer1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to add customer with signature from someone else")

# Winner is the only participant
def test_get_winner_with_one_participant(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 2).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    time.sleep(2) # So that expiration will pass
    tx_hash = contract.functions.get_winner(restaurant1_account).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert(contract.functions.show_winner(restaurant1_account).call() == customer1_account)  # winner is the only participant
    print("The winner was the only participant in the competition")

# Winner is one of the two participants in the competition
def test_get_winner_with_two_participants(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 2).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("Tom", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer2_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    time.sleep(2) # So that expiration will pass
    tx_hash = contract.functions.get_winner(restaurant1_account).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert((contract.functions.show_winner(restaurant1_account).call() == customer1_account) or (contract.functions.show_winner(restaurant1_account).call() == customer2_account))  # winner is one of the two customers
    print("The winner was one of the two participants in the competition")

# Fails to get a winner before the expiration has passed
def test_get_winner_before_expiration(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 60).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.get_winner(restaurant1_account).transact({'from':restaurant1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to call find a winner before expiration has passed")

# Fails to get a winner when there is already a winner
def test_get_winner_when_already_winner(contract):
    tx_hash = contract.functions.add_restaurant_to_competition("Eat together", 2).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = contract.functions.add_customer_to_competition("George", restaurant1_account, hash_of_123, signature_of_123_restaurant_1).transact({'from':customer1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    time.sleep(2)
    tx_hash = contract.functions.get_winner(restaurant1_account).transact({'from':restaurant1_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    try:
        tx_hash = contract.functions.get_winner(restaurant1_account).transact({'from':restaurant1_account})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print("Failed to try to get a winner after a winner was already found")


def get_gas_for_verify(contract):
    print(contract.functions.recover(hash_of_123, signature_of_123_restaurant_1).estimateGas({'from':customer1_account}) * 1000000000)

def run_all_tests():
    contract = make_new_contract()
    #print("Gas price: " + str(w3.eth.gasPrice))
    test_add_restaurant_to_competition(contract)
    contract = make_new_contract()
    test_add_same_restaurant_to_competition(contract)
    contract = make_new_contract()
    test_add_2_customers_to_competition(contract)
    contract = make_new_contract()
    test_add_customer_that_is_restaurant(contract)
    contract = make_new_contract()
    test_add_customer_after_expiration(contract)
    contract = make_new_contract()
    test_add_customer_twice(contract)
    contract = make_new_contract()
    test_signature_verification_fail(contract)
    contract = make_new_contract()
    test_get_winner_with_one_participant(contract)
    contract = make_new_contract()
    test_get_winner_with_two_participants(contract)
    contract = make_new_contract()
    test_get_winner_before_expiration(contract)
    contract = make_new_contract()
    test_get_winner_when_already_winner(contract)
    # contract = make_new_contract()
    # get_gas_for_verify(contract)
    print("All tests pass!")

contract_source_code = None
contract_source_code_file = 'contract_test.sol'

with open(contract_source_code_file, 'r') as file:
    contract_source_code = file.read()

contract_compiled = compile_source(contract_source_code)
contract_interface = contract_compiled['<stdin>:Competition']
Competition = w3.eth.contract(abi=contract_interface['abi'],
                          bytecode=contract_interface['bin'])

owner_account = w3.eth.accounts[0]
restaurant1_account = w3.eth.accounts[1]
restaurant2_account = w3.eth.accounts[2]
customer1_account = w3.eth.accounts[3]
customer2_account = w3.eth.accounts[4]

run_all_tests()
