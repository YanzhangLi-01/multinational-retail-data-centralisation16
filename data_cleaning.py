import pandas as pd
import numpy as np
import re
import uuid

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

    def clean_card_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Remove rows with NULL values
        cleaned_df = df.dropna()

        # Ensure 'date_payment_confirmed' column is in datetime format
        cleaned_df['date_payment_confirmed'] = pd.to_datetime(cleaned_df['date_payment_confirmed'], errors='coerce')

        # Drop rows where 'date_payment_confirmed' could not be converted
        cleaned_df = cleaned_df.dropna(subset=['date_payment_confirmed'])

        # Optionally, format the 'date_payment_confirmed' column to a specific date format, e.g., 'YYYY-MM-DD'
        cleaned_df['date_payment_confirmed'] = cleaned_df['date_payment_confirmed'].dt.strftime('%Y-%m-%d')

        return cleaned_df
    
    def clean_store_data(self, df):
        # Drop rows with any NULL values in 'opening_date'
        df = df.dropna(subset=['opening_date'])
        
        # Correct the 'continent' values
        df['continent'] = df['continent'].replace({'eeAmerica': 'America', 'eeEurope': 'Europe'})

        # Drop columns with any NULL values
        df = df.dropna(axis=1, how='any')
        
        # Define a function to parse different date formats
        def parse_date(date_str):
            if pd.isna(date_str):
                return np.nan
            
            date_formats = ['%Y-%m-%d', '%B %Y %d', '%Y %B %d']
            
            for fmt in date_formats:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except ValueError:
                    continue
            
            return np.nan
        
        # Convert 'opening_date' to datetime using the custom parsing function
        df['opening_date'] = df['opening_date'].apply(parse_date)

        # Remove rows with any NaN values in 'opening_date' after parsing
        df = df.dropna(subset=['opening_date'])

        # Remove the time part from 'opening_date'
        df['opening_date'] = df['opening_date'].dt.date

        # Clean 'staff_numbers' to ensure it contains only numeric values
        df['staff_numbers'] = df['staff_numbers'].apply(lambda x: np.nan if not str(x).isdigit() else x)
        
        # Drop rows with any NaN values in 'staff_numbers' after cleaning
        df = df.dropna(subset=['staff_numbers'])
        
        # Convert 'staff_numbers' to integers
        df['staff_numbers'] = df['staff_numbers'].astype(int)

        # Define a function to identify nonsensical strings
        def is_nonsense(value):
            if isinstance(value, str):
                # Define a regex pattern for nonsensical strings
                pattern = r'^[A-Z0-9]{8,}$' 
                return bool(re.match(pattern, value))
            return False
        
        # Drop rows containing nonsensical strings
        nonsensical_mask = df.applymap(is_nonsense)
        df = df[~nonsensical_mask.any(axis=1)]

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

    def clean_orders_data(self, df):
        columns_to_drop = ['first_name', 'last_name', '1']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        df.columns = [col.strip().lower() for col in df.columns]  # Normalize column names
        return df
    
    def clean_date_details_data(self, df):
        # Regular expression pattern for validating UUIDs
        uuid_pattern = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        )

        # Function to check if a string is a valid UUID
        def is_valid_uuid(uuid_str):
            return bool(uuid_pattern.match(uuid_str))

        # Filter out rows where 'date_uuid' column has invalid UUIDs
        df = df[df['date_uuid'].apply(is_valid_uuid)]

        return df