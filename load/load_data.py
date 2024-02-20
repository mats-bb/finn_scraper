import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import load_from_csv

# Constants
TRANSFORMED_DIR = r'transform\files'

# Connection URL
url_object = URL.create(
    drivername='postgresql',
    username='postgres',
    password='Morradi123',
    host='localhost',
    port=5432,
    database='finn_scraper'
)

def columns_to_lower(data):
    """Final touch, make all column names lowercase."""
    data.columns = data.columns.str.lower()

def run():
    """Run the loading process."""
    data = load_from_csv(TRANSFORMED_DIR, 'transformed_list')
    columns_to_lower(data)
    engine = create_engine(url_object)
    data.to_sql('listing_info', engine, if_exists='append', index=False)

run()