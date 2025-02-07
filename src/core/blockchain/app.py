import os
import threading
import time

import uvicorn
from fastapi import FastAPI

from blockchain import Blockchain, logger
from routes import create_router

app = FastAPI()
blockchain = Blockchain()
router = create_router(blockchain)

app.include_router(router)



def init_nodes():
    time.sleep(5)
    known_nodes_env = os.getenv("KNOWN_NODES", "")
    known_nodes = set(known_nodes_env.split(",")) if known_nodes_env else set()
    logger.info(f"Known nodes: {known_nodes}")

    for node in known_nodes:
        blockchain.add_node(node)

@app.on_event("startup")
def startup_event():
    threading.Thread(target=init_nodes, daemon=True).start()
    threading.Thread(target=auto_sync, daemon=True).start()


def auto_sync():
    while True:
        blockchain.sync_chain()
        time.sleep(10)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
