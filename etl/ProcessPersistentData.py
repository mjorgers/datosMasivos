import pandas as pd
import requests, chardet, json
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['palmoildatabase']
collection = db['transformed_data']

# Load Excel data
excel_file = "/Users/carlos.salinas.gancedo/Documents/UC3M/Projects/aceitePalmaPanelDatosMasivos/data-files/PalmOil-UML-Oct-2024.xlsx"
palm_oil_data = pd.read_excel(excel_file)

# Fetch API data
api_url = "https://datacatalogapi.worldbank.org/dexapps/efi/data?datasetId=BS.BTI&indicatorIds=BS.BTI.Q15.3&years=2024&countryCodes=BRA,MYS,PNG,IDN,KHM,CMR,COL,CRI,LBR,MLI,COD,DOM,ECU,GAB,GHA,GTM,HND,IND,LBR,MDG,MEX,MMR,NIC,NGA,PAN,PNG,PER,PHL,STP,SLE,SLB,LKA,THA,UGA,VEN"
response = requests.get(api_url)
api_data = response.json()

# Transform API data
indicator_map = {
    "BS.BTI.Q15.3": "Anticorruption policy"
}
indicators = {
    entry["COUNTRY_CODE"]: {
        "name": indicator_map.get(entry["INDICATOR_ID"], "Unknown Indicator"),
        "value": entry["IND_VALUE"],
        "last_update": entry["CAL_YEAR"]
    } for entry in api_data["value"]
}

# Transform CSV data
transformed_data = []
for _, row in palm_oil_data.iterrows():
    country_code = row['ISO']
    country_name = row['Country']
    oil_mill_data = {
        "mill": row['Mill Name'],
        "parent_company": row['Parent Company'],
        "group": row['Group Name'],
        "RSPO_type": f"{row['RSPO Type']}",
        "RSPO_date": f"{row['Date RSPO Certification Status']}"[:10],
        "confidence_level": row['Confidence level'],
        "providence": row['Province'],
        "district": row['District'],
        "coordinates": {
            "latitude": row['Latitude'],
            "longitude": row['Longitude']
        }
    }
    
    # Find or create entry for the country
    country_entry = next((item for item in transformed_data if item["country_code"] == country_code), None)
    if not country_entry:
        country_entry = {
            "country_code": country_code,
            "country_name": country_name,
            "indicators": [indicators.get(country_code, {})],
            "oil_mills": []
        }
        transformed_data.append(country_entry)
    
    # Append oil mill data
    country_entry["oil_mills"].append(oil_mill_data)

# Save transformed data to MongoDB
# collection.insert_many(transformed_data)
# File path to save the JSON file
file_path = "palm_oil_project.json"

# Write the JSON data to the file
with open(file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=4)  # 'indent' makes the file readable

print(f"JSON data saved to {file_path}")

print(f"Data successfully saved to MongoDB in the 'palmoildatabase' database.")