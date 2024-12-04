from ExternalDataHandler import ExternalDataHandler
from DataWarehouseHandler import DataWarehouseHadler
import time
import logging

if __name__ == "__main__":
    print("Starting the ETL...", flush=True)

    externalData_handler = ExternalDataHandler()
    datawarehouse_handler = DataWarehouseHadler()

    # Extract data from different sources and transform it
    externalData_handler.extract()
    transformed_data = externalData_handler.transform()

    # Save the data in the datawarehouse
    datawarehouse_handler.load_data(transformed_data)

    print("Finished the ETL...", flush=True)