# Description: This is the main file for the scraper.
# It will scrape the data from the website and save it
# to the database.

from StockPriceFetcher import StockPriceFetcher
import time
import logging
# Instantiate the StockPriceFetcher class
stock_fetcher = StockPriceFetcher(['MKHO-MY', 'UVPOF', 'SOPS-MY'])

while 1:
    try:
        stock_prices_json = stock_fetcher.fetch_stock_prices()
        print(stock_prices_json)
        # TODO: Save the stock prices to the database
        time.sleep(3600)
    except Exception as e:
        # Log the error
        logging.error(f"An error occurred: {e}")