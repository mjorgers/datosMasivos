import requests
from bs4 import BeautifulSoup
from datetime import datetime

class StockPriceFetcher:
    def __init__(self, stock_symbols):
        self.stock_symbols = stock_symbols
        self.url_template = 'https://www.cnbc.com/quotes/{symbol}'

    def fetch_stock_prices(self):
        stock_prices = []
        for symbol in self.stock_symbols:
            url = self.url_template.format(symbol=symbol)
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                stock_price_element = soup.find('span', class_='QuoteStrip-lastPrice')
                if stock_price_element:
                    stock_prices.append({
                        'symbol': symbol,
                        'price': stock_price_element.get_text(strip=True),
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                return -1

        return stock_prices