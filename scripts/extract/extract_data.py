from datetime import datetime
import requests as req
import json
from bs4 import BeautifulSoup as bs

# Constants
# Extracted files directory
EXTRACTED_DIR = '/opt/airflow/data/extracted'
# Info we want to get from the urls
TERMS = ["Arbeidsgiver", "Stillingstittel", "Ansettelsesform", "Sektor", "Bransje", "Stillingsfunksjon"]

def get_resp(url):
    """Get response from url."""
    return req.get(url)

def get_soup(resp):
    """Get soup object from response."""
    return bs(resp.content, "html.parser")

def load_from_json(dir_, filename):
    """Load json file from directory."""
    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dir_, filename, data):
    """Save json file to directory."""
    with open(fr'{dir_}/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clean_words(list_):
    """Remove unwanted punctuation and whitespace."""
    list_ = [word.rstrip(',') for word in list_]
    list_ = [word.strip() for word in list_]

    return list_

def add_info(terms_dict, url):
    """Add url and date_added info to terms_dict."""
    terms_dict["url"] = url
    terms_dict["date_added"] = str(datetime.today().date())

def get_tags_list(term, soup):
    """Extract relevant term tags from html object(soup)."""
    tags_list = []

    try:
        tag_info = soup.find("dt", string=term).find_next_siblings()
    except:
        tags_list.append("Missing")
    else:
        for tag in tag_info:
            if tag.name == "dt":
                break
            else:
                tags_list.append(tag.text)

    return tags_list

def process_special_terms(term, tags_list):
    """Check special conditions, split tags_list if true."""
    if term in ["Stillingsfunksjon", "Bransje"]:
        if len(tags_list) == 1 and ',' in tags_list[0]:
            tags_list = tags_list[0].split(',')

    return tags_list

def assign_tags_to_dict(terms_dict, term, tags_list):
    """Assign tags to term."""
    if len(tags_list) == 1:
        terms_dict[term] = str(tags_list[0])
    else:
        terms_dict[term] = tags_list

def extract_url_info(urls, terms):
    """Run extraction for every url."""
    dict_list = []

    for url in urls[:10]:
        terms_dict = {}

        resp = get_resp(url)
        soup = get_soup(resp)
        
        for term in terms:
            tags_list = get_tags_list(term, soup)
            tags_list = process_special_terms(term, tags_list)
            clean_tags_list = clean_words(tags_list)
            assign_tags_to_dict(terms_dict, term, clean_tags_list)
            add_info(terms_dict, url)

        dict_list.append(terms_dict)

    return dict_list

def run():
    """Run."""
    urls = load_from_json(EXTRACTED_DIR, 'urls')
    dict_list = extract_url_info(urls, TERMS)
    save_to_json(EXTRACTED_DIR, 'terms_dict', dict_list)

run()