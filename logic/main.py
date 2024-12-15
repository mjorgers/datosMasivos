import os, json
from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import ObjectId
from etl.ExternalDataHandler import ExternalDataHandler
from etl.DataWarehouseHandler import DataWarehouseHadler
from wrapper.CommodityPriceScraper import CommodityPriceScraper

app = Flask(__name__)
CORS(app)
externalData_handler = ExternalDataHandler()
datawarehouse_handler = DataWarehouseHadler()

if __name__ == "__main__":
    print("Starting the Logic...", flush=True)

    demo_json = open('demo.json')
    demo_data = json.load(demo_json)

    # Extract data from different sources and transform it
    externalData_handler.extract()
    transformed_data = externalData_handler.transform()

    # Save the data in the datawarehouse
    datawarehouse_handler.load_data(transformed_data)

    # Save the demo data in the datawarehouse
    demo_data = datawarehouse_handler.load_demo_data(demo_data)

    print("Finished the Logic...", flush=True)

@app.route('/')
def index():
    return 'API is working'

@app.route('/api/data', methods=['GET'])
def get_data():
    
    transformed_data = datawarehouse_handler.read_data()

    if transformed_data == None:
        return jsonify({'error': 'Failed to fetch the transfomed data'})

    return jsonify(transformed_data)

@app.route('/api/demodata', methods=['GET'])
def get_demo_data():
    
    demo_data = datawarehouse_handler.read_demo_data()

    if demo_data == None:
        return jsonify({'error': 'Failed to fetch the demo data'})

    return jsonify(demo_data)

@app.route('/api/stock_price', methods=['GET'])
def get_stock_price():
    stock_symbols = request.args.get('stock_symbols')
    if not stock_symbols:
        return jsonify({'error': 'stock_symbols parameter is required'})

    stock_symbols = stock_symbols.split(',')
    stock_price_fetcher = CommodityPriceScraper(stock_symbols)
    stock_prices = stock_price_fetcher.fetch_prices()

    if stock_prices == -1:
        return jsonify({'error': 'Failed to fetch stock prices'})

    return jsonify({'stock_prices': stock_prices})

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({'message': 'Pong!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')