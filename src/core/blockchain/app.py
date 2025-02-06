from fastapi import FastAPI
import threading
import time
from routes import router
import os
from blockchain import Blockchain
import requests
import uvicorn

app = FastAPI()
app.include_router(router)

blockchain = Blockchain()

def init_nodes():
    node_name = os.getenv("NODE_NAME", "")
    known_nodes = {
        "node1": "5000",
        "node2": "5000",
        "node3": "5000",
    }

    if node_name in known_nodes:
        del known_nodes[node_name]

    for node, port in known_nodes.items():
        url = f"http://{node}:{port}/add_node"  # Используем имя сервиса
        print(f"Пытаюсь подключиться к: {url}")

        try:
            response = requests.post(url, json={"node": f"{node}:{port}"})
            if response.status_code == 200:
                print(f"Узел {node} успешно добавлен")
            else:
                print(f"Не удалось добавить узел {node}, код статуса: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Не удалось подключиться к узлу {node} по адресу {url}, ошибка: {e}")


@app.on_event("startup")
def startup_event():
    time.sleep(5)
    threading.Thread(target=lambda: [time.sleep(10), blockchain.sync_chain()], daemon=True).start()
    threading.Thread(target=init_nodes, daemon=True).start()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
