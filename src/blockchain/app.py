from flask import Flask
import threading
import time
from routes import bp
from blockchain import Blockchain

app = Flask(__name__)
app.register_blueprint(bp)

blockchain = Blockchain()

if __name__ == '__main__':
    threading.Thread(target=lambda: [time.sleep(10), blockchain.sync_chain()], daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
