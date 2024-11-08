import requests
from bs4 import BeautifulSoup
import json


class StockPriceFetcher:
    def __init__(self, stock_symbols):
        self.stock_symbols = stock_symbols
        self.url_template = 'https://www.cnbc.com/quotes/{symbol}'

    def fetch_stock_prices(self):
        stock_prices = {}
        for symbol in self.stock_symbols:
            url = self.url_template.format(symbol=symbol)
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                stock_price_element = soup.find('span', class_='QuoteStrip-lastPrice')
                if stock_price_element:
                    stock_prices[symbol] = stock_price_element.get_text(strip=True)
                else:
                    stock_prices[symbol] = f"Could not find the stock price element for {symbol}."
            else:
                stock_prices[
                    symbol] = f"Failed to retrieve the webpage for {symbol}. Status code: {response.status_code}"

        return json.dumps(stock_prices, indent=4)


stock_fetcher = StockPriceFetcher(['MKHO-MY', 'UVPOF', 'SOPS-MY'])
stock_prices_json = stock_fetcher.fetch_stock_prices()
print(stock_prices_json)

"""
Right now it's only doing a single request and then it stops, but it should be able to run as a daemon updating the prices whenever it's called.
"""