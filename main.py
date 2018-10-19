#!/usr/bin/python

from hashlib import sha256
import json

def compute_hash(texto):
    block_string = json.dumps(texto, sort_keys=True)
    return sha256(block_string.encode()).hexdigest()

def proof_of_work(block):
    """
    We add some difficulty to hash calculation setting a requirement :
    hash must start with '000', so we recalculate it changing 'nonce'
    value until requirement is fulfilled
    :param block:
    :return: computed_hash
    """

    computed_hash = compute_hash(block)
    while not computed_hash.startswith('0' * 2):    #2 is nonce difficulty
        block['nonce'] += 1
        computed_hash = compute_hash(block)
    return computed_hash

def generate_block(transactions, chain=[]):
    """
    A new block (including transactions) is generated and appended to blockchain

    :param transactions:
    :param chain:
    :return: updated chain
    """
    if chain == []:
        new_block = {'contents': {'id': 0, 'nonce': 0, 'previoushash': '0', 'transactions': transactions}, 'blockhash': ''}
    else:
        last_block = chain[-1]
        last_id = chain[-1]['contents']['id']
        previous_hash = chain[-1]['blockhash']
        new_block = {'contents': {'id': last_id + 1, 'nonce': 0, 'previoushash': previous_hash, 'transactions': transactions}, 'blockhash': ''}

    new_block['blockhash'] = proof_of_work(new_block['contents'])
    chain.append(new_block)
    return chain

def check_chain(chain):
    """
    Checks block's hash recalculating it.
    previous_hash also must be the same as the former blockhash.
    If both requirements are fulfilled chain is considered valid.

    :param chain:
    :return:
    """
    previous_hash = '0'
    for node in chain:
        hash = proof_of_work(node['contents'])
        if hash != node['blockhash']:
            print ("Hash error in block : ", node)
            return
        if previous_hash != node['contents']['previoushash']:
            print("Previoushash in block : ", node)
            return
        previous_hash = hash

    print("Chain is OK!")

# Some Lorem ipsum transactions that will be stored in a list.
transaction0 = {'id': 0, 'text': 'Lorem ipsum dolor sit amet'}
transaction1 = {'id': 1, 'text': 'consectetur adipiscing elit'}

transactions = []

transactions.append(transaction0)
transactions.append(transaction1)

chain = generate_block(transactions)

transaction2 = {'id': 0, 'text': 'Aenean id accumsan sapien'}
transaction3 = {'id': 1, 'text': 'Praesent tristique venenatis pretium'}

transactions = []
transactions.append(transaction2)
transactions.append(transaction3)

chain = generate_block(transactions, chain)

# If I try to tamper the chain changing 'Lorem' to 'lorem' in the text of the first transaction in block #1
# the chain validation will fail.
# chain = [{'contents': {'id': 0, 'nonce': 201, 'previoushash': '0', 'transactions': [{'id': 0, 'text': 'lorem ipsum dolor sit amet'}, {'id': 1, 'text': 'consectetur adipiscing elit'}]}, 'blockhash': '008c307c38b3bb07a3e6eced51af24bf4ec27a3c170f1ed9f92274401e0bbafe'}, {'contents': {'id': 1, 'nonce': 25, 'previoushash': '008c307c38b3bb07a3e6eced51af24bf4ec27a3c170f1ed9f92274401e0bbafe', 'transactions': [{'id': 0, 'text': 'Aenean id accumsan sapien'}, {'id': 1, 'text': 'Praesent tristique venenatis pretium'}]}, 'blockhash': '00286a1d3814c93a7eada7233c1c8ae6b10d980a1c7418199ed2c34025f44c5e'}]

check_chain(chain)