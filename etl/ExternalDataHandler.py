import os
import pandas as pd
import requests

class ExternalDataHandler:

    def __init__(self):
        # Local Excel file with the list of Oil Mills
        self.excel_file = os.getenv('FILE_PATH')
        # National Anticorruption policy indicator.
        self.api_url = "https://datacatalogapi.worldbank.org/dexapps/efi/data?datasetId=BS.BTI&indicatorIds=BS.BTI.Q15.3&years=2024&countryCodes=BRA,MYS,PNG,IDN,KHM,CMR,COL,CRI,LBR,MLI,COD,DOM,ECU,GAB,GHA,GTM,HND,IND,LBR,MDG,MEX,MMR,NIC,NGA,PAN,PNG,PER,PHL,STP,SLE,SLB,LKA,THA,UGA,VEN"

    def extract(self):
        # Extract file data
        self.palm_oil_data = pd.read_excel(self.excel_file)
        # Extract API data
        response = requests.get(self.api_url)
        self.api_data = response.json()

    def transform(self):
        # Transform API data
        indicator_map = {
            "BS.BTI.Q15.3": "Anticorruption policy"
        }
        indicators = {
            entry["COUNTRY_CODE"]: {
                "name": indicator_map.get(entry["INDICATOR_ID"], "Unknown Indicator"),
                "value": entry["IND_VALUE"],
                "last_update": entry["CAL_YEAR"]
            } for entry in self.api_data["value"]
        }

        # Transform CSV data
        transformed_data = []
        for _, row in self.palm_oil_data.iterrows():
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

        return transformed_data
