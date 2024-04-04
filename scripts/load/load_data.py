import pandas as pd
from sqlalchemy import create_engine

# Database connection
HOST_NAME = 'finn_final_db'
DATABASE = 'finn_final_db'
USER_NAME = 'admin'
PASSWORD = 'admin'
PORT_ID = 5432

TRANSFORMED_DIR = '/opt/airflow/data/transformed'

def load_from_csv(dir_, filename):
    """Load csv file from directory, return pandas dataframe."""
    with open(fr'{dir_}/{filename}.csv', 'r', encoding='utf-8') as f:
        return pd.read_csv(f)

def columns_to_lower(data):
    """Final touch, make all column names lowercase."""
    data.columns = data.columns.str.lower()

def run():
    """Load pandas dataframe into database."""
    data = load_from_csv(TRANSFORMED_DIR, 'transformed_list')
    columns_to_lower(data)
    engine = create_engine(f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST_NAME}:{PORT_ID}/{DATABASE}")
    data.to_sql('listing_info', engine, if_exists='append', index=False)

run()