from flask import Blueprint, jsonify, request
from blockchain import Blockchain
import logging


blockchain = Blockchain()
logger = logging.getLogger(__name__)

bp = Blueprint('blockchain', __name__)

@bp.route('/mine_block', methods=['GET'])
def mine_block():
    try:
        previous_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(previous_block['proof'])
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        logger.info(f"Block mined: {block}")
        return jsonify({'message': 'Block mined!', 'block': block}), 200
    except Exception as e:
        logger.error(f"Error mining block: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/add_vote', methods=['POST'])
def add_vote():
    try:
        data = request.get_json()
        required = ['voter_id', 'vote_id', 'answer_id', 'signature', 'public_key']
        if not all(k in data for k in required):
            return jsonify({'message': 'Missing fields'}), 400

        if blockchain.add_vote(data['voter_id'], data['vote_id'], data['answer_id'], data['signature'],
                               data['public_key']):
            logger.info(f"Vote added: {data}")
            return jsonify({'message': 'Vote added!'}), 201
        return jsonify({'message': 'Invalid signature'}), 400
    except Exception as e:
        logger.error(f"Error adding vote: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/get_chain', methods=['GET'])
def get_chain():
    try:
        return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200
    except Exception as e:
        logger.error(f"Error retrieving chain: {e}")
        return jsonify({'message': 'Internal server error'}), 500


@bp.route('/add_node', methods=['POST'])
def add_node():
    try:
        data = request.get_json()
        if 'node' not in data:
            return jsonify({'message': 'No node provided'}), 400

        blockchain.add_node(data['node'])
        logger.info(f"Node added: {data['node']}")
        return jsonify({'message': 'Node added!', 'nodes': list(blockchain.nodes)}), 201
    except Exception as e:
        logger.error(f"Error adding node: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/sync', methods=['GET'])
def sync():
    if blockchain.sync_chain():
        return jsonify({'message': 'Chain synchronized'}), 200
    return jsonify({'message': 'Failed to synchronize chain'}), 500