from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'API is working'

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'Not implemented'})

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({'message': 'Pong!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')