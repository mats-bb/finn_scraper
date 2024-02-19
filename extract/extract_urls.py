import sys
import os

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import get_resp, get_soup, save_to_json

base_url = "https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&published=1"

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
    extracted_dir = r'extract\files'
    save_to_json(extracted_dir, 'urls', urls)

a = run()