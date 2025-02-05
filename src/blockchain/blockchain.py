from flask import Flask, jsonify, request
import datetime
import hashlib
import json
import requests
import pickle
import os
import threading
import time
from ecdsa import SigningKey, VerifyingKey, NIST256p


class Blockchain:
    DIFFICULTY = 5  # Количество нулей в начале хэша
    FILE_NAME = 'blockchain.pkl'

    def __init__(self):
        self.chain = []
        self.mempool = []  # Неподтвержденные транзакции
        self.nodes = set()
        self.load_chain()
        if not self.chain:
            self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.utcnow()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.mempool[:],
        }
        self.mempool.clear()
        self.chain.append(block)
        self.save_chain()
        return block

    def add_vote(self, voter_id, vote_id, answer_id, signature, public_key):
        if not self.verify_signature(voter_id, vote_id, answer_id, signature, public_key):
            return False
        self.mempool.append({
            'voter_id': voter_id,
            'vote_id': vote_id,
            'answer_id': answer_id,
            'signature': signature,
            'public_key': public_key
        })
        return True

    def proof_of_work(self, previous_proof):
        new_proof = 0
        while True:
            hash_operation = hashlib.sha256(f'{new_proof}{previous_proof}'.encode()).hexdigest()
            if hash_operation[:self.DIFFICULTY] == '0' * self.DIFFICULTY:
                return new_proof
            new_proof += 1

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def validate_chain(self, chain):
        previous_block = chain[0]
        for block in chain[1:]:
            if block['previous_hash'] != self.hash(previous_block):
                return False
            if not block['proof'] or not self.proof_of_work(block['proof'] - 1):
                return False
            previous_block = block
        return True

    def sync_chain(self):
        for node in self.nodes:
            try:
                response = requests.get(f'http://{node}/get_chain')
                if response.status_code == 200:
                    new_chain = response.json()['chain']
                    if len(new_chain) > len(self.chain) and self.validate_chain(new_chain):
                        self.chain = new_chain
                        self.save_chain()
            except requests.exceptions.RequestException:
                continue

    def add_node(self, address):
        self.nodes.add(address)

    def save_chain(self):
        with open(self.FILE_NAME, 'wb') as f:
            pickle.dump(self.chain, f)

    def load_chain(self):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, 'rb') as f:
                self.chain = pickle.load(f)

    def verify_signature(self, voter_id, vote_id, answer_id, signature, public_key):
        message = f'{voter_id}{vote_id}{answer_id}'.encode()
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST256p)
            return vk.verify(bytes.fromhex(signature), message)
        except:
            return False


app = Flask(__name__)
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    return jsonify({'message': 'Block mined!', 'block': block}), 200


@app.route('/add_vote', methods=['POST'])
def add_vote():
    data = request.get_json()
    required = ['voter_id', 'vote_id', 'answer_id', 'signature', 'public_key']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
    if blockchain.add_vote(data['voter_id'], data['vote_id'], data['answer_id'], data['signature'], data['public_key']):
        return jsonify({'message': 'Vote added!'}), 201
    return jsonify({'message': 'Invalid signature'}), 400


@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200


@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    if 'node' not in data:
        return jsonify({'message': 'No node provided'}), 400
    blockchain.add_node(data['node'])
    return jsonify({'message': 'Node added!', 'nodes': list(blockchain.nodes)}), 201


@app.route('/sync', methods=['GET'])
def sync():
    blockchain.sync_chain()
    return jsonify({'message': 'Chain synchronized'}), 200


if __name__ == '__main__':
    threading.Thread(target=lambda: [time.sleep(10), blockchain.sync_chain()], daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
