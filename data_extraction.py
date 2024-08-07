import pandas as pd
import tabula
import requests
import boto3
from io import StringIO
import json
from urllib.parse import urlparse

class DataExtractor:
    def __init__(self):
        pass

    def read_rds_table(self, db_connector, table_name):
        engine = db_connector.init_db_engine()
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df

    def retrieve_pdf_data(self, pdf_link):
        dfs = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df

    def list_number_of_stores(self, endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()['number_stores']
        else:
            response.raise_for_status()

    def retrieve_stores_data(self, store_endpoint, headers, num_stores):
        store_data = []
        for store_number in range(1, num_stores):
            response = requests.get(store_endpoint.format(store_number=store_number), headers=headers)
            if response.status_code == 200:
                #print(response.json())
                store_data.append(response.json())
            else:
                response.raise_for_status()
        
        return pd.DataFrame(store_data)

    def extract_from_s3(self, s3_address):
        # Parse the S3 address
        bucket = s3_address.split('/')[2]
        key = '/'.join(s3_address.split('/')[3:])
        
        # Initialize boto3 client
        s3 = boto3.client('s3')
        
        # Get the object from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Convert to DataFrame
        df = pd.read_csv(StringIO(content))
        
        return df

    def extract_json_from_s3(self, s3_url):
        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Parse the S3 URL
        parsed_url = urlparse(s3_url)
        bucket_name = parsed_url.netloc.split('.')[0]
        file_key = parsed_url.path.lstrip('/')

        # Get the object from S3
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        json_content = obj['Body'].read().decode('utf-8')
        
        # Directly use json_content if it's already a dictionary
        try:
            # Attempt to convert JSON string to dictionary
            data = json.loads(json_content)
        except json.JSONDecodeError:
            # If json_content is already a dictionary, use it directly
            data = json_content
        
        # Check if data is a dictionary
        if not isinstance(data, dict):
            raise TypeError("The fetched data is not in the expected dictionary format.")
        
        # Check if the JSON data has the expected keys
        expected_keys = ['timestamp', 'month', 'year', 'day', 'time_period', 'date_uuid']
        if not all(k in data for k in expected_keys):
            raise ValueError("JSON data is missing one or more required keys.")
        
        # Convert the JSON data to a pandas DataFrame
        # Transpose the JSON data to match the format
        df = pd.DataFrame({key: pd.Series(value) for key, value in data.items()})
        
        # Reset index to ensure a numeric index
        df.reset_index(drop=True, inplace=True)

        return df
