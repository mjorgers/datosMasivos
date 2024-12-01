from MongoDBHandler import MongoDBHandler
import time
import logging

if __name__ == "__main__":
    print("Hello from the scraper!", flush=True)

    # Instantiate the MongoDBHandler class
    db_handler = MongoDBHandler()

    # Set up logging
    logging.basicConfig(filename='scraper.log', level=logging.ERROR)

    print("Starting the scraper...", flush=True)
    while True:
        time.sleep(60)