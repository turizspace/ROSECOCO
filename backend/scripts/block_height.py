# root/backend/scripts/block_height_server.py
from flask import Flask, jsonify, send_from_directory
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

# Endpoint to get block height
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

# Endpoint to get blockchain information
@app.route('/blockchain_info')
def get_blockchain_info():
    try:
        payload = {
            "jsonrpc": "1.0",
            "id": "curltext",
            "method": "getblockchaininfo",
            "params": []
        }
        response = requests.post(RPC_URL, json=payload, auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD))
        response_json = response.json()
        if 'result' in response_json:
            logging.info("Blockchain Info: Successfully fetched")
            return jsonify(response_json['result'])
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Error fetching blockchain info: {error_message}")
            return jsonify({'error': error_message})
    except Exception as e:
        logging.error(f"Error fetching blockchain info: {e}")
        return jsonify({'error': str(e)})

# Endpoint to get mempool information
@app.route('/mempool_info')
def get_mempool_info():
    try:
        payload = {
            "jsonrpc": "1.0",
            "id": "curltext",
            "method": "getmempoolinfo",
            "params": []
        }
        response = requests.post(RPC_URL, json=payload, auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD))
        response_json = response.json()
        if 'result' in response_json:
            logging.info("Mempool Info: Successfully fetched")
            return jsonify(response_json['result'])
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Error fetching mempool info: {error_message}")
            return jsonify({'error': error_message})
    except Exception as e:
        logging.error(f"Error fetching mempool info: {e}")
        return jsonify({'error': str(e)})

# Endpoint to get mining information
@app.route('/mining_info')
def get_mining_info():
    try:
        payload = {
            "jsonrpc": "1.0",
            "id": "curltext",
            "method": "getmininginfo",
            "params": []
        }
        response = requests.post(RPC_URL, json=payload, auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD))
        response_json = response.json()
        if 'result' in response_json:
            logging.info("Mining Info: Successfully fetched")
            return jsonify(response_json['result'])
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Error fetching mining info: {error_message}")
            return jsonify({'error': error_message})
    except Exception as e:
        logging.error(f"Error fetching mining info: {e}")
        return jsonify({'error': str(e)})

# Endpoint to estimate smart fee
@app.route('/estimate_smart_fee/<int:blocks>')
def estimate_smart_fee(blocks):
    try:
        payload = {
            "jsonrpc": "1.0",
            "id": "curltext",
            "method": "estimatesmartfee",
            "params": [blocks]
        }
        response = requests.post(RPC_URL, json=payload, auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD))
        response_json = response.json()
        if 'result' in response_json:
            logging.info(f"Estimated Smart Fee for {blocks} blocks: Successfully fetched")
            return jsonify(response_json['result'])
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Error fetching estimated smart fee: {error_message}")
            return jsonify({'error': error_message})
    except Exception as e:
        logging.error(f"Error fetching estimated smart fee: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
