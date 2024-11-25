# Description: This is the main file for the scraper.
# It will scrape the data from the website and save it
# to the database.

from StockPriceFetcher import StockPriceFetcher
from MongoDBHandler import MongoDBHandler
import time
import logging

if __name__ == "__main__":
    print("Hello from the scraper!", flush=True)

    # Instantiate the StockPriceFetcher class
    stock_fetcher = StockPriceFetcher(['MKHO-MY', 'UVPOF', 'SOPS-MY'])

    # Instantiate the MongoDBHandler class
    db_handler = MongoDBHandler(collection_name='stockprices')

    # Set up logging
    logging.basicConfig(filename='scraper.log', level=logging.ERROR)

    print("Starting the scraper...", flush=True)
    while True:
        stock_prices = stock_fetcher.fetch_stock_prices()
        if stock_prices == -1:
            logging.error("An error occurred while fetching stock prices")
        else:
            print(stock_prices)

            print("Stock prices fetched successfully. Saving to the database...", flush=True)
            for stock_price in stock_prices:
                db_handler.write_stock_price(stock_price)

        time.sleep(60)