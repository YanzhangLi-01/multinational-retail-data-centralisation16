import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self, df):
        # Drop rows with any NULL values
        df = df.dropna()
    
        # Convert data columns and drop rows with any error values
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df = df.dropna(subset=['date_of_birth'])
    
        # Remove time part, keeping only the date
        df['date_of_birth'] = df['date_of_birth'].dt.date

        return df

    def clean_card_data(self, df):
        # Remove rows with NULL values
        df = df.dropna()
        
        return df
    
    def clean_store_data(self, df):
        # Drop rows with any NULL values in 'opening_date'
        df = df.dropna(subset=['opening_date'])
        
        # Correct the 'store_type' values
        df['store_type'] = df['store_type'].replace({'eeAmerica': 'America', 'eeEurope': 'Europe'})

        # Drop columns with any NULL values
        df = df.dropna(axis=1, how='any')
        
        # Define a function to identify nonsensical strings
        def is_nonsense(value):
            if isinstance(value, str):
                # Define a regex pattern for nonsensical strings (adjust as needed)
                pattern = r'^[A-Z0-9]{8,}$' 
                return bool(re.match(pattern, value))
            return False
        
        # Drop rows containing nonsensical strings
        nonsensical_mask = df.applymap(is_nonsense)
        df = df[~nonsensical_mask.any(axis=1)]

        # Convert 'opening_date' to datetime, coerce errors to NaT (Not a Time)
    #    df['opening_date'] = pd.to_datetime(df['opening_date'], format='%B %Y %d') #date_formats = ['%d/%m/%Y', '%B %Y %d', '%Y %B %d']

        return df
    
    def convert_product_weights(self, df):
        def convert_weight(weight):
            if isinstance(weight, str):
                weight = weight.lower().strip()

                # Handle cases like '12 x 100'
                if ' x ' in weight:
                    parts = weight.split(' x ')
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        total_weight = int(parts[0]) * int(parts[1])
                        return total_weight / 1000  # assuming the weight is in grams

                # Remove units and convert to kg
                for unit in ['kg', 'g', 'ml', 'l']:
                    if unit in weight:
                        number = weight.replace(unit, '').strip()
                        try:
                            value = float(number)
                            if unit == 'kg' or unit == 'l':
                                return value
                            else:  # 'g' or 'ml'
                                return value / 1000
                        except ValueError:
                            return None
            return None

        df['weight'] = df['weight'].apply(convert_weight)

        # Remove any rows with NULL values in the weight column
        df = df.dropna(subset=['weight'])

        return df
    
#    def clean_products_data(self, df):
#        df = df.dropna(subset=['weight'])
#        df = df[df['weight'] > 0]
#        return df
    
    def clean_orders_data(self, df):
        columns_to_drop = ['first_name', 'last_name', '1']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        df.columns = [col.strip().lower() for col in df.columns]  # Normalize column names
        return df
    
    def clean_date_details_data(self, df):
        df = df.dropna()
#        df['date'] = pd.to_datetime(df['date'], errors='coerce')
#        df = df.dropna(subset=['date'])
#        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
#        df = df.dropna(subset=['time'])
        return df

