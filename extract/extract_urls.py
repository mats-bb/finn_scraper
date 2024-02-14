import requests as req
from bs4 import BeautifulSoup as bs
import json

base_url = fr"https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&published=1"

def save_to_json(urls):
    with open('urls.json', 'w') as f:
        json.dump(urls, f, indent=4)

def get_first_page(base_url):
    urls = []

    resp = req.get(base_url)
    if resp.status_code == 200:
        soup = bs(resp.content, "html.parser")
        classes = soup.find_all(class_='sf-search-ad-link link link--dark hover:no-underline')
        for class_ in classes:
            urls.append(class_['href'])

    return urls

def get_conseq_pages(first_page_url, urls):
    page_num = 2

    while True:
    
        resp = req.get(fr"{first_page_url}" + "&page=" + str(page_num))

        if resp.status_code == 200:
            soup = bs(resp.content, "html.parser")
            classes = soup.find_all(class_='sf-search-ad-link link link--dark hover:no-underline')

            for class_ in classes:
                urls.append(class_['href'])

            page_num += 1
                
        else:
            break

    return urls

def run():
    urls = get_first_page(base_url)
    urls2 = get_conseq_pages(base_url, urls)
    save_to_json(urls2)

a = run()
