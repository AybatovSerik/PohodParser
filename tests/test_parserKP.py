from Classes.RouteClassKP import RouteKP
import requests
from bs4 import BeautifulSoup
import re

session = requests.session()
headers = {
    'authority': 'www.kith.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}


test_page = 'https://www.vpoxod.ru/route/nw/Viborg_monrepo_kayak#content-top'
route_object = RouteKP()
route_object.parse_page(test_page, session, headers)

print(route_object.to_json()['full_description'])
print(route_object.guides)
print(route_object.to_json()['guides'])
print(route_object.to_json()['hikes'])