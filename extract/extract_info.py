from datetime import datetime
import os
import sys

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import get_resp, get_soup, load_from_json, save_to_json

def clean_words(list_):
    """Remove unwanted punctuation and whitespace."""
    list_ = [word.rstrip(',') for word in list_]
    list_ = [word.strip() for word in list_]

    return list_

def add_info(terms_dict, url):
    terms_dict["url"] = url
    terms_dict["date_added"] = str(datetime.today().date())

def get_tags_list(term, soup):
    tags_list = []
    try:
        tag_info = soup.find("dt", string=term).find_next_siblings()
    except ValueError:
        tags_list.append("Missing")
    else:
        for tag in tag_info:
            if tag.name == "dt":
                break
            else:
                tags_list.append(tag.text)

    return tags_list

def process_special_terms(term, tags_list):
    if term in ("Stillingsfunksjon", "Bransje"):
        if len(tags_list) == 1 and ',' in tags_list[0]:
                tags_list = tags_list[0].split(',')

    return tags_list

def assign_term_to_dict(terms_dict, term, tags_list):
    if len(tags_list) == 1:
        terms_dict[term] = str(tags_list[0])
    else:
        terms_dict[term] = tags_list

    return terms_dict

def extract_url_info(urls):
    dict_list = []

    for url in urls:
        pass

def get_term_words(terms, soup):
    terms_dict = {}

    for string in terms:
        tags_list = []
        
        try:
            tag_info = soup.find("dt", string=string).find_next_siblings()
        except:
            tags_list.append("Missing")
        else:

            for tag in tag_info:
                if tag.name == "dt":
                    break
                else:
                    tags_list.append(tag.text)

        if string == 'Stillingsfunksjon' or string == 'Bransje':
                    
            if len(tags_list) == 1 and ',' in tags_list[0]:
                tags_list = tags_list[0].split(',')
                
        tags_list = clean_words(tags_list)
                
        if len(tags_list) == 1:
            terms_dict[string] = str(tags_list[0])
        else:
            terms_dict[string] = tags_list

    return terms_dict

def get_info(urls):
    dict_list = []

    c = 0

    for url in urls:
        resp = get_resp(url)
        soup = get_soup(resp)
        terms = ["Arbeidsgiver", "Stillingstittel", "Ansettelsesform", "Sektor", "Bransje", "Stillingsfunksjon"]
        terms_dict = get_term_words(terms, soup)
        terms_dict["url"] = url
        terms_dict["date_added"] = str(datetime.today().date())
        dict_list.append(terms_dict)

    print(len(dict_list))
    return dict_list

def run():
    extracted_dir = r'extract\files'
    urls = load_from_json(extracted_dir, 'urls')
    dict_list = get_info(urls)
    save_to_json(extracted_dir, 'dict_list', dict_list)

run()