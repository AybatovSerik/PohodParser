import requests
import Classes
from bs4 import BeautifulSoup
import datetime
from parser_config import session, headers


def take_routes_urls(session, headers):
    routes_url = "https://turclub-pik.ru/search/?page=2000&sorting=date&limit=20&routes_limit=20"
    routes_page = session.get(routes_url, headers=headers)
    routes_soup = BeautifulSoup(routes_page.text, 'html.parser')
    routes_tags = [tag for tag in routes_soup.find(attrs={'class': 'columns is-multiline mb-6'}).children]
    return [tag.find(attrs={'itemprop': 'url'}).get('href') for tag in routes_tags]


def main():
    route_url = "https://turclub-pik.ru"
    time = datetime.datetime.today().strftime('%Y%m%d_%H%M')
    filepath = f"../data/pik_parsed_routes_{time}.txt"
    print(f"Start Parsing {route_url}")
    print(f"Now {datetime.datetime.today().strftime('%Y-%m-%d : %H-%M-%S')}")

    routes_urls = take_routes_urls(session, headers)
    print(f"Num of routes {len(routes_urls)}")

    with open(filepath, 'w', encoding='utf-8') as f:
        for (num, url) in enumerate(routes_urls):
            if num % 100 == 0:
                print(f"Route num - {num}")
            route_object = Classes.RouteClassPIK.RoutePIK()
            route_object.parse_page(route_url+url, session, headers)
            f.write(str(route_object.to_json()) + '\n')


if __name__ == '__main__':
    main()
