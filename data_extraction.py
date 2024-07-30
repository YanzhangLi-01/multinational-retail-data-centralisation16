import pandas as pd
import tabula
import requests
import boto3
from io import StringIO
import json

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

    def retrieve_stores_data(self, store_endpoint, headers):
        store_data = []
        for store_number in range(1, 451):
            response = requests.get(store_endpoint.format(store_number=store_number), headers=headers)
            if response.status_code == 200:
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
        s3 = boto3.client('s3')
        bucket_name = s3_url.split('/')[2]
        file_key = '/'.join(s3_url.split('/')[3:])
        
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = json.loads(obj['Body'].read().decode('utf-8'))
        
        df = pd.json_normalize(data)
        return df