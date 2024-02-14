import requests as req
from bs4 import BeautifulSoup as bs
import json
import sys

# sys.path.append(rf'C:\Users\matsk\Desktop\Projects\finn_scraper\helper_funcs')
from ..helper_funcs.helpers import get_soup

base_url = "https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&published=1"
extracted_dir = r'extract\files'

def get_first_page(base_url):
    urls = []

    resp = get_resp(base_url)
    if resp.status_code == 200:
        soup = get_soup(resp)
        classes = soup.find_all(class_='sf-search-ad-link link link--dark hover:no-underline')
        for class_ in classes:
            urls.append(class_['href'])

    return urls

def get_conseq_pages(base_url, urls):
    page_num = 2

    while True:
    
        resp = get_resp(fr"{base_url}" + "&page=" + str(page_num))

        if resp.status_code == 200:
            soup = get_soup(resp)
            classes = soup.find_all(class_='sf-search-ad-link link link--dark hover:no-underline')

            for class_ in classes:
                urls.append(class_['href'])

            page_num += 1
                
        else:
            break

    return urls

def run():
    first_page_urls = get_first_page(base_url)
    urls = get_conseq_pages(base_url, first_page_urls)
    save_to_json(extracted_dir, 'urls', urls)

a = run()