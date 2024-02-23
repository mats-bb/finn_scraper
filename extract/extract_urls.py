import sys
import os

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import get_resp, get_soup, save_to_json

# Constants
# First page of Finn.no, jobber, oslo, nye i dag
BASE_URL = "https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&published=1"
# Extracted files directory
EXTRACTED_DIR = r'extract\files'

def get_classes(soup, class_name):
    """Returns a list of classes from soup object."""
    classes = soup.find_all(class_=class_name)

    return classes

def get_first_page(base_url):
    """Returns a list of urls from the first page of Finn.no, jobber, oslo, nye i dag."""
    urls = []

    resp = get_resp(base_url)

    if resp.status_code == 200:
        soup = get_soup(resp)
        classes = get_classes(soup, 'sf-search-ad-link link link--dark hover:no-underline')

        for class_ in classes:
            urls.append(class_['href'])

    return urls

def get_consec_pages(base_url, urls):
    """Returns a list of urls from the consecutive pages of Finn.no, jobber, oslo, nye i dag."""
    page_num = 2

    while True:
    
        resp = get_resp(fr"{base_url}" + "&page=" + str(page_num))

        if resp.status_code == 200:
            soup = get_soup(resp)
            classes = get_classes(soup, 'sf-search-ad-link link link--dark hover:no-underline')

            for class_ in classes:
                urls.append(class_['href'])

            page_num += 1
                
        else:
            break

    return urls

def run():
    """Run the url extraction process."""
    first_page_urls = get_first_page(BASE_URL)
    all_urls = get_consec_pages(BASE_URL, first_page_urls)
    save_to_json(EXTRACTED_DIR, 'urls', all_urls)

run()