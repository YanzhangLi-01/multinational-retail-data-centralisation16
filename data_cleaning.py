import pandas as pd
import numpy as np

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
        # Drop rows with any NULL values
        df = df.dropna(subset=['opening_date'])
        
        # Correct the 'store_type' values
        df['store_type'] = df['store_type'].replace('eeAmerica', 'America')
        df['store_type'] = df['store_type'].replace('eeEurope', 'Europe')
        
        # Function to parse different date formats
        def parse_date(date_str):
            date_formats = ['%d/%m/%Y', '%B %Y %d', '%Y %B %d']
            for fmt in date_formats:
                try:
                    return pd.to_datetime(date_str, format=fmt, errors='coerce')
                except ValueError:
                    continue
            return np.nan
        
        # Convert 'opening_date' to datetime using the custom parsing function
        df['opening_date'] = df['opening_date'].apply(parse_date)

        # Drop rows with any NULL values after date parsing
        df = df.dropna(subset=['opening_date'])

        # Format the 'opening_date' to 'YYYY/M/D'
        df['opening_date'] = df['opening_date'].dt.strftime('%Y/%-m/%-d')

        return df
    
    def convert_product_weights(self, df):
        def convert_weight(weight):
            if isinstance(weight, str):
                weight = weight.lower()
                if 'kg' in weight:
                    return float(weight.replace('kg', '').strip())
                elif 'g' in weight:
                    return float(weight.replace('g', '').strip()) / 1000
                elif 'ml' in weight:
                    return float(weight.replace('ml', '').strip()) / 1000
                elif 'l' in weight:
                    return float(weight.replace('l', '').strip())
                else:
                    return None
            else:
                return None  # or raise an error if needed, or handle differently
            
        df['weight'] = df['weight'].apply(convert_weight)
        return df
    
    def clean_products_data(self, df):
        df = df.dropna(subset=['weight'])
        df = df[df['weight'] > 0]
        return df
    
    def clean_orders_data(self, df):
        columns_to_drop = ['first_name', 'last_name', '1']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        df.columns = [col.strip().lower() for col in df.columns]  # Normalize column names
        return df
    
    def clean_date_details_data(self, df):
        df = df.dropna()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
        df = df.dropna(subset=['time'])
        return df

