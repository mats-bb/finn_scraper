import requests as req
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

def load_from_json():
    with open('urls.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dict_list):
    with open('dict_list.json', 'w', encoding='utf-8') as f:
        json.dump(dict_list, f, indent=4, ensure_ascii=False)

def get_soup(url):
    resp = req.get(url)
    soup = bs(resp.content, "html.parser")

    return soup

def get_term_words(terms, soup):
    terms_dict = {}

    for string in terms:
        tags_list = []
        
        tag_info = soup.find("dt", string=string).find_next_siblings()
        for tag in tag_info:
            if tag.name == "dt":
                break
            else:
                tags_list.append(tag.text)

        tags_list = [word.replace(",", "") for word in tags_list]
            
        if len(tags_list) == 1:
            terms_dict[string] = str(tags_list[0])
        else:
            terms_dict[string] = tags_list

    return terms_dict

def get_info(urls):
    dict_list = []

    c = 0

    for url in urls[0:10]:
        soup = get_soup(url)
        terms = ["Arbeidsgiver", "Stillingstittel", "Ansettelsesform", "Sektor", "Bransje", "Stillingsfunksjon"]
        terms_dict = get_term_words(terms, soup)
        terms_dict["url"] = url
        terms_dict["date_added"] = datetime.today().date()
        dict_list.append(terms_dict)

    return dict_list

def run():
    urls = load_from_json()
    dict_list = get_info(urls)
    save_to_json(dict_list)

run()