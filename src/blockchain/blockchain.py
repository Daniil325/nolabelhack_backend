from flask import Flask, jsonify, request
import datetime
import hashlib
import json
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': []  # Здесь будут храниться данные о голосовании
        }
        self.chain.append(block)
        return block

    def add_vote(self, user_id, vote_id, vote_answer_id):
        self.chain[-1]['data'].append({'voter_id': user_id, 'vote': vote_id, 'answer_id': vote_answer_id})

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_node(self, address):
        self.nodes.add(address)

    def sync_chains(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            (f'http://{node}/get_chain')
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] !=    '0000':
                return False

            previous_block = block
            block_index += 1

        return True

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.chain[-1]
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'A block is MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'data': block['data']
    }

    return jsonify(response), 200

@app.route('/add_vote', methods=['POST'])
def add_vote():
    values = request.get_json()
    required = ['user_id', 'vote_id', 'vote_answer_id']

    if not all(k in values for k in required):
        return 'Missing values', 400

    blockchain.add_vote(values['user_id'], values['vote_id'], values['vote_answer_id'])
    response = {'message': 'Vote will be added to the next block'}
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/add_node', methods=['POST'])
def add_node():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/sync', methods=['GET'])
def sync():
    if blockchain.sync_chains():
        response = {'message': 'The chain has been synchronized with the longest chain'}
    else:
        response = {'message': 'The chain is already up to date'}

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)