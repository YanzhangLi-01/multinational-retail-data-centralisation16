import yaml
from sqlalchemy import create_engine, text

class DatabaseConnector:
    def __init__(self, config_file):
        self.credentials = self.read_db_creds(config_file)

    def read_db_creds(self, config_file):
        with open(config_file, 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    def init_db_engine(self):
        creds = self.credentials
        engine = create_engine(
            f"postgresql://{creds['USER']}:{creds['PASSWORD']}@{creds['HOST']}:{creds['PORT']}/{creds['DATABASE']}"
        )
        return engine

    def list_db_tables(self, engine):
        query = text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        with engine.connect() as connection:
            result = connection.execute(query)
            tables = result.fetchall()
        return [table[0] for table in tables]

    def upload_to_db(self, df, table_name):
        engine = self.init_db_engine()
    
        if df is not None:
            df.to_sql(table_name, engine, if_exists='replace', index=False)
        else:
            print("Error: DataFrame is None, cannot upload to the database.")

