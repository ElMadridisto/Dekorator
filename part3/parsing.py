import re
import time
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from logger_3 import *
def get_headers():
    headers = Headers(browser='random_browser', os='random_os').generate()
    return headers

def get_links():
    url = "https://spb.hh.ru/search/vacancy?text=python&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true&page=0"
    data = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(data.text, features='lxml')
    number_of_pages = int(soup.find('div', class_='bloko-gap bloko-gap_top').find('div', class_='pager').find_all('span', recursive=False)[-1].find('a', class_='bloko-button').text)
    list_vacancy = []
#В цикле вместо 3 должен стоять number_of_pages, но поиск по всем страницам с вакансиями тогда занимает очень много времени, поэтому для удобства поставл 3
    for page in range(3):#range(number_of_pages):
        url = f"https://spb.hh.ru/search/vacancy?text=python&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true&page={page}"
        data = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(data.text, features='lxml')
        links = soup.find_all('a', class_="serp-item__title")

        for l in links:
            link = l.get('href')
            data = requests.get(link, headers=get_headers())
            soup = BeautifulSoup(data.text, features='lxml')
            pattern = r'.*((D|d)jango).*((F|f)lask).*'
            run = soup.find(attrs={'data-qa': "vacancy-description"}).text
            #Иногда без паузы hh.ru просил вводить капчу, когда был поиск по всем страницам
            #time.sleep(2)
            if re.search(pattern, run):
                list_vacancy.append(get_resume(link))

            print(list_vacancy)
    return list_vacancy
@logger('main.log')
def get_resume(link):
    data = requests.get(link, headers=get_headers())
    soup = BeautifulSoup(data.text, features='lxml')
    name = soup.find(attrs={'data-qa' : 'vacancy-title'}).text
    salary = soup.find(attrs={'data-qa':'vacancy-salary'}).text

    try:
        city = soup.find(attrs={'data-qa':"vacancy-view-raw-address"}).text
    except AttributeError:
        city = soup.find(attrs={'data-qa':"vacancy-view-location"}).text
    resume = {'url': link, 'salary':salary, 'name':name, 'city':city}
    return resume


def get_json(list_vacancy):
    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(list_vacancy, v, ensure_ascii=False)

