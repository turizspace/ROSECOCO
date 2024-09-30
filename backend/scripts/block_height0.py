# root/backend/scripts/block_height_server.py
from flask import Flask, jsonify, send_from_directory, make_response
from flask_cors import CORS
from requests.auth import HTTPBasicAuth
import requests
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
RPC_USER = 'matrpc'
RPC_PASSWORD = 'sniffblockheight'
RPC_PORT = 5173
RPC_URL = f'http://127.0.0.1:{RPC_PORT}/'

# Setup logging
logging.basicConfig(filename='block_height.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/block_height')
def get_block_height():
    try:
        payload = {
            "jsonrpc": "1.0",
            "id": "curltext",
            "method": "getblockcount",
            "params": []
        }
        response = requests.post(RPC_URL, json=payload, auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD))
        response_json = response.json()
        if 'result' in response_json:
            block_height = response_json['result']
            logging.info(f"Block Height: {block_height}")
            return jsonify({'block_height': block_height})
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Error fetching block height: {error_message}")
            return jsonify({'error': error_message})
    except Exception as e:
        logging.error(f"Error fetching block height: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
