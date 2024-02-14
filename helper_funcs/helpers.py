import requests as req
import json
from bs4 import BeautifulSoup as bs

def load_from_json(filename):
    with open(f'{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dir_, filename, data):
    with open(f'{dir_}\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_resp(url):
    return req.get(url)

def get_soup(resp):
    return bs(resp.content, "html.parser")
