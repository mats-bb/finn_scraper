import requests as req
import json
from bs4 import BeautifulSoup as bs
import pandas as pd

def load_from_json(dir_, filename):
    with open(fr'{dir_}\{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dir_, filename, data):
    with open(fr'{dir_}\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_from_csv(dir_, filename):
    with open(fr'{dir_}\{filename}.csv', 'r', encoding='utf-8') as f:
        return pd.read_csv(f)

def get_resp(url):
    return req.get(url)

def get_soup(resp):
    return bs(resp.content, "html.parser")
