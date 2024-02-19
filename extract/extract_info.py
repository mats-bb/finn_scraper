from datetime import datetime
import os
import sys

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import get_resp, get_soup, load_from_json, save_to_json

def get_term_words(terms, soup):
    terms_dict = {}

    for string in terms:
        tags_list = []
        try:
            tag_info = soup.find("dt", string=string).find_next_siblings()
        except:
            # print(tags_list)
            terms_dict[string] = "Missing"
            # print("Tag didnt exist, adding default.")
        else:

            for tag in tag_info:
                if tag.name == "dt":
                    break
                else:
                    tags_list.append(tag.text)

        if string == 'Stillingsfunksjon' or string == 'Bransje':
                    
            if len(tags_list) > 1:
                # tags_list = [word.replace(",", "") for word in tags_list]
                tags_list = [word.rstrip(',') for word in tags_list]

            elif len(tags_list) == 1 and ',' in tags_list[0]:
                tags_list = tags_list[0].split(',')
                tags_list = list(filter(None, tags_list))
                tags_list = [word.rstrip(',') for word in tags_list]
                
        if len(tags_list) == 1:
            terms_dict[string] = str(tags_list[0])
        else:
            terms_dict[string] = tags_list

    # for key, val in terms_dict.items():
    #     if len(val) == 0:
    #         terms_dict[key] = "None"

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