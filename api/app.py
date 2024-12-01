from flask import Flask, jsonify, request
from flask_cors import CORS

from StockPriceFetcher import StockPriceFetcher

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API is working'

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'Not implemented'})

@app.route('/api/stock_price', methods=['GET'])
def get_stock_price():
    stock_symbols = request.args.get('stock_symbols')
    if not stock_symbols:
        return jsonify({'error': 'stock_symbols parameter is required'})

    stock_symbols = stock_symbols.split(',')
    stock_price_fetcher = StockPriceFetcher(stock_symbols)
    stock_prices = stock_price_fetcher.fetch_stock_prices()

    if stock_prices == -1:
        return jsonify({'error': 'Failed to fetch stock prices'})

    return jsonify({'stock_prices': stock_prices})

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({'message': 'Pong!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')