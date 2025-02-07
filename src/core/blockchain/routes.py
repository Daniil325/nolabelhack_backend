from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from blockchain import Blockchain

router = APIRouter()

class VoteRequest(BaseModel):
    voter_id: str
    vote_id: str
    answer_id: str
    signature: str
    public_key: str

class NodeRequest(BaseModel):
    node: str

class VoteRequest(BaseModel):
    voter_id: str
    vote_id: str
    answer_id: str
    signature: str
    public_key: str

class NodeRequest(BaseModel):
    node: str

def create_router(blockchain: Blockchain):
    router = APIRouter()

    @router.post("/add_node")
    def add_node(request: NodeRequest):
        blockchain.add_node(request.node)
        return {"message": "Node added!", "nodes": list(blockchain.nodes)}

    @router.post("/add_vote")
    def add_vote(vote: VoteRequest):
        if blockchain.add_vote(vote.voter_id, vote.vote_id, vote.answer_id, vote.signature, vote.public_key):
            if len(blockchain.mempool) >= 5:
                previous_block = blockchain.chain[-1]
                proof = blockchain.proof_of_work(previous_block["proof"])
                previous_hash = blockchain.hash(previous_block)
                blockchain.create_block(proof, previous_hash)
                return {"message": "Vote added and block mined!"}
            return {"message": "Vote added!"}
        raise HTTPException(status_code=400, detail="Invalid signature")

    @router.get("/get_chain")
    def get_chain():
        return {"chain": blockchain.chain, "length": len(blockchain.chain)}

    @router.get("/mempool")
    def get_mempool():
        return {"mempool": blockchain.mempool}

    @router.get("/sync")
    def sync():
        if blockchain.sync_chain():
            return {"message": "Chain synchronized"}
        raise HTTPException(status_code=500, detail="Failed to synchronize chain")

    return router