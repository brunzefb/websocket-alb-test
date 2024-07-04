import asyncio
from flask import Flask, jsonify
import websockets
import threading

WEB_SOCKET_PORT = 80
HEALTH_CHECK_PORT = 8080

app = Flask(__name__)

# Define a health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200


async def handle_websocket(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            response = f"Received: {message}"
            await websocket.send(response)
    except websockets.ConnectionClosed:
        pass

def start_flask_app():
    app.run(host='0.0.0.0', port=HEALTH_CHECK_PORT)

def start_websocket_server():
    start_server = websockets.serve(handle_websocket, "0.0.0.0", WEB_SOCKET_PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    start_websocket_server()