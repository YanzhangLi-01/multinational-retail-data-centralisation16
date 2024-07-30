from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Use appropriate config files for RDS and local databases
    rds_connector = DatabaseConnector(config_file='db_creds_rds.yaml')
    local_connector = DatabaseConnector(config_file='db_creds_local.yaml')
    rds_engine = rds_connector.init_db_engine()

    data_extractor = DataExtractor()
    data_cleaning = DataCleaning()

    tables = rds_connector.list_db_tables(rds_engine)
    print("Tables in the AWS RDS database:", tables)

    # Extract, clean, and upload user data
    user_data_df = data_extractor.read_rds_table(rds_connector, 'legacy_users')
    cleaned_user_data_df = data_cleaning.clean_user_data(user_data_df)
    local_connector.upload_to_db(cleaned_user_data_df, 'dim_users')
    print("User data cleaned and uploaded to local PostgreSQL successfully.")

    # Extract, clean, and upload card data
    pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
    card_data_df = data_extractor.retrieve_pdf_data(pdf_link)
    cleaned_card_data_df = data_cleaning.clean_card_data(card_data_df)
    local_connector.upload_to_db(cleaned_card_data_df, 'dim_card_details')
    print("Card data cleaned and uploaded to local PostgreSQL successfully.")

    # Extract, clean, and upload store data
    api_key = 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'
    headers = {'x-api-key': api_key}
    number_of_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
    store_details_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'

    number_of_stores = data_extractor.list_number_of_stores(number_of_stores_endpoint, headers)
    print(f"Number of stores: {number_of_stores}")

    store_data_df = data_extractor.retrieve_stores_data(store_details_endpoint, headers)
    cleaned_store_data_df = data_cleaning.clean_store_data(store_data_df)
    local_connector.upload_to_db(cleaned_store_data_df, 'dim_store_details')
    print("Store data cleaned and uploaded to local PostgreSQL successfully.")

#    # Extract, clean, and upload product data
#    s3_address = 's3://data-handling-public/products.csv'
#    product_data_df = data_extractor.extract_from_s3(s3_address)
#    product_data_df = data_cleaning.convert_product_weights(product_data_df)
#    cleaned_product_data_df = data_cleaning.clean_products_data(product_data_df)
#    local_connector.upload_to_db(cleaned_product_data_df, 'dim_products')
#    print("Product data cleaned and uploaded to local PostgreSQL successfully.")
#
#    # Extract, clean, and upload orders data
#    orders_table_name = 'orders_table'
#    orders_data_df = data_extractor.read_rds_table(rds_connector, orders_table_name)
#    cleaned_orders_data_df = data_cleaning.clean_orders_data(orders_data_df)
#    local_connector.upload_to_db(cleaned_orders_data_df, 'orders_table')
#    print("Orders data cleaned and uploaded to local PostgreSQL successfully.")
#
#    # Extract, clean, and upload date details data
#    json_url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
#    date_details_df = data_extractor.extract_json_from_s3(json_url)
#    cleaned_date_details_df = data_cleaning.clean_date_details_data(date_details_df)
#    local_connector.upload_to_db(cleaned_date_details_df, 'dim_date_times')
#    print("Date details data cleaned and uploaded to local PostgreSQL successfully.")

if __name__ == "__main__":
    main()
