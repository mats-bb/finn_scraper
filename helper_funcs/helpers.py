import requests as req
import json
from bs4 import BeautifulSoup as bs
import pandas as pd

def load_from_json(dir_, filename):
    """Load json file from directory."""
    with open(fr'{dir_}\{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dir_, filename, data):
    """Save json file to directory."""
    with open(fr'{dir_}\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_from_csv(dir_, filename):
    """Load csv file from directory."""
    with open(fr'{dir_}\{filename}.csv', 'r', encoding='utf-8') as f:
        return pd.read_csv(f)

def get_resp(url):
    """Get response from url."""
    return req.get(url)

def get_soup(resp):
    """Get soup object from response."""
    return bs(resp.content, "html.parser")
