import datetime
import hashlib
import json
import os
import pickle
import logging
import requests
from ecdsa import VerifyingKey, NIST256p

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Blockchain:
    DIFFICULTY = 5
    FILE_NAME = "blockchain.pkl"

    def __init__(self):
        self.chain = []
        self.mempool = []
        self.nodes = set()
        self.load_chain()
        if not self.chain:
            self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.mempool[:],
        }
        self.mempool.clear()
        self.chain.append(block)
        self.save_chain()
        logger.info(f"Block created: {block}")
        return block

    def add_vote(self, voter_id, vote_id, answer_id, signature, public_key):
        if not self.verify_signature(voter_id, vote_id, answer_id, signature, public_key):
            logger.warning(f"Invalid signature for vote: {voter_id}, {vote_id}, {answer_id}")
            return False
        self.mempool.append({
            "voter_id": voter_id,
            "vote_id": vote_id,
            "answer_id": answer_id,
            "signature": signature,
            "public_key": public_key
        })
        logger.info(f"Vote added to mempool: {voter_id}, {vote_id}, {answer_id}")
        return True

    def proof_of_work(self, previous_proof):
        new_proof = 0
        while True:
            hash_operation = hashlib.sha256(f"{new_proof}{previous_proof}".encode()).hexdigest()
            if hash_operation.startswith("0" * self.DIFFICULTY):
                return new_proof
            new_proof += 1

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def validate_chain(self, chain):
        previous_block = chain[0]
        for block in chain[1:]:
            if block["previous_hash"] != self.hash(previous_block):
                logger.warning(f"Invalid previous hash in block: {block}")
                return False
            previous_block = block
        return True

    def add_node(self, address):
        self.nodes.add(address)
        logger.info(f"Node added: {address}")

    def save_chain(self):
        try:
            with open(self.FILE_NAME, "wb") as f:
                pickle.dump(self.chain, f)
            logger.info("Blockchain saved successfully")
        except Exception as e:
            logger.error(f"Ошибка сохранения блокчейна: {e}")

    def load_chain(self):
        if os.path.exists(self.FILE_NAME):
            try:
                with open(self.FILE_NAME, "rb") as f:
                    self.chain = pickle.load(f)
                logger.info("Blockchain loaded successfully")
            except Exception as e:
                logger.error(f"Ошибка загрузки блокчейна: {e}")

    def verify_signature(self, voter_id, vote_id, answer_id, signature, public_key):
        message = f"{voter_id}{vote_id}{answer_id}".encode()
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST256p)
            return vk.verify(bytes.fromhex(signature), message, hashfunc=hashlib.sha256)
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False

    def sync_chain(self):
        try:
            for node in self.nodes:
                try:
                    response = requests.get(f"http://{node}/get_chain")
                    if response.status_code == 200:
                        new_chain = response.json()["chain"]
                        if len(new_chain) > len(self.chain) and self.validate_chain(new_chain):
                            self.chain = new_chain
                            self.save_chain()
                            logger.info(f"Chain synchronized with node: {node}")
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Failed to sync with node {node}: {e}")
                    continue
            return True
        except Exception as e:
            logger.error(f"Error during synchronization: {e}")
            return False