import os
import sys

from sqlalchemy import create_engine

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import load_from_csv
    
data = load_from_csv(r'transform\files', 'transformed_list')
data.columns = data.columns.str.lower()

engine = create_engine('postgresql://postgres:Morradi123@localhost/finn_scraper')

data.to_sql('listing_info', engine, if_exists='append', index=False)