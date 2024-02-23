from datetime import datetime
import os
import sys

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import get_resp, get_soup, load_from_json, save_to_json

# Constants
# Extracted files directory
EXTRACTED_DIR = r'extract\files'
# Info we want to get from the urls
TERMS = ["Arbeidsgiver", "Stillingstittel", "Ansettelsesform", "Sektor", "Bransje", "Stillingsfunksjon"]

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

    for url in urls:
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




# # To be obsoleted
# def get_term_words(terms, soup):
#     terms_dict = {}

#     for string in terms:
#         tags_list = []
        
#         try:
#             tag_info = soup.find("dt", string=string).find_next_siblings()
#         except:
#             tags_list.append("Missing")
#         else:

#             for tag in tag_info:
#                 if tag.name == "dt":
#                     break
#                 else:
#                     tags_list.append(tag.text)

#         if string == 'Stillingsfunksjon' or string == 'Bransje':
                    
#             if len(tags_list) == 1 and ',' in tags_list[0]:
#                 tags_list = tags_list[0].split(',')
                
#         tags_list = clean_words(tags_list)
                
#         if len(tags_list) == 1:
#             terms_dict[string] = str(tags_list[0])
#         else:
#             terms_dict[string] = tags_list

#     return terms_dict

# def get_info(urls):
#     dict_list = []

#     c = 0

#     for url in urls:
#         resp = get_resp(url)
#         soup = get_soup(resp)
#         terms = ["Arbeidsgiver", "Stillingstittel", "Ansettelsesform", "Sektor", "Bransje", "Stillingsfunksjon"]
#         terms_dict = get_term_words(terms, soup)
#         terms_dict["url"] = url
#         terms_dict["date_added"] = str(datetime.today().date())
#         dict_list.append(terms_dict)

#     print(len(dict_list))
#     return dict_list

# def run():
#     extracted_dir = r'extract\files'
#     urls = load_from_json(extracted_dir, 'urls')
#     dict_list = get_info(urls)
#     save_to_json(extracted_dir, 'dict_list', dict_list)

run()