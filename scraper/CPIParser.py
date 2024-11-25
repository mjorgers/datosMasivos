import pandas as pd
import json

class CPIParser:
    def __init__(self, file_path):
        self.economy_iso3 = None
        self.indicator_id = None
        self.filtered_df = None
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.json = None

    def filter_data(self, economy_iso3, indicator_id='TI.CPI.Score'):
        self.economy_iso3 = economy_iso3
        self.indicator_id = indicator_id

        self.filtered_df = self.df[(self.df['Economy ISO3'] == economy_iso3) & (self.df['Indicator ID'] == indicator_id)]

        if self.filtered_df.empty:
            print(f"No data found for Economy ISO3: {economy_iso3} and Indicator ID: {indicator_id}")
        else:
            self.get_json()

    def get_json(self):
        years = [str(year) for year in range(2012, 2024)]
        data = {year: float(self.filtered_df[year].values[0]) for year in years}
        self.json = json.dumps(data, indent=4)

