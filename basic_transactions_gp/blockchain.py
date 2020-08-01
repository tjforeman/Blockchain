# Paste your version of blockchain.py from the client_mining_p
# folder here
# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='==========', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True).encode()

        # TODO: Hash this string using sha256
        hash = hashlib.sha256(block_string).hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     block_string = json.dumps(self.last_block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof +=1
    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:6] == "0" * 6
        # return True or False

    def new_transaction (self,sender, recipient, amount ):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def post_new_transaction():

    data = request.get_json()
    
    required = ['sender', 'recipient', 'amount']
    if not all(k in data for k in required):
        response = {'message': 'Missing Values'}
        return jsonify(response), 400

    blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])

    message = {
        'block_index':blockchain.last_block['index'],
        'block': blockchain.last_block
    }

    return jsonify(message), 200



@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
  

    if not data['proof'] and data['id']:
        return 'A proof and an ID are needed to attempt to mine', 400

    block = blockchain.last_block
    proof = data.get('proof')

    block_string = json.dumps(block, sort_keys=True)

    if blockchain.valid_proof(block_string ,proof ):
        
    # # Run the proof of work algorithm to get the next proof
    # # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(proof, previous_hash)

        # blockchain.new_transaction('0', data['id'], 1)
        response = {
        # TODO: Send a JSON response with the new block
        'block' : new_block,
        'message': 'New Block Forged'
        }

        return jsonify(response), 200

    else:
        response = {
            'message' : 'Sorry the proof provided did not match'
        }
        return jsonify(response), 400


@app.route('/chain', methods=['GET'])
@cross_origin()
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length' : len(blockchain.chain),
        'chain' : blockchain.chain,
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def return_last_block():

    last_block = blockchain.last_block

    response = {
        'last_block': last_block
    }

    return jsonify(response), 200



# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)