import requests
import Classes
from bs4 import BeautifulSoup
import datetime
from parser_config import session, headers


def define_last_num_of_routes(session, headers):
    start_url = "https://www.vpoxod.ru/route?per-page=48&page=500"
    start_response = session.get(start_url, headers=headers)
    print(start_response.status_code)
    start_soup = BeautifulSoup(start_response.text, 'html.parser')
    last_page_num = int(start_soup.find(attrs={'class':'pagination'}).find(attrs={'class':'active disabled'}).text)
    return last_page_num


def take_routes_urls(route_pages_num,session,headers):
    route_url = "https://www.vpoxod.ru"
    routes_list = []
    for page_num in range(1,route_pages_num+1):
        page_url = f"https://www.vpoxod.ru/route?per-page=48&page={page_num}"
        print(f'Page {page_num}: {page_url}')
        page_response = session.get(page_url, headers=headers)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        page_routes_list = page_soup.find_all(attrs={'class': 'main_page_hike_title'})
        page_routes_list = [(route_url+route.find()['href']) for route in page_routes_list]
        routes_list += page_routes_list

    return routes_list


def main():
    route_url = "https://www.vpoxod.ru"
    time = datetime.datetime.today().strftime('%Y%m%d_%H%M')
    filepath = f"../data/kp_parsed_routes_{time}.txt"
    print(f"Start Parsing {route_url}")
    print(f"Now {datetime.datetime.today().strftime('%Y-%m-%d : %H-%M-%S')}")

    route_pages_num = define_last_num_of_routes(session, headers)
    print(f'Num of routes lists {route_pages_num}')
    routes_urls = take_routes_urls(route_pages_num, session, headers)
    # routes_urls = take_routes_urls(1, session, headers)
    print(f"Num of routes {len(routes_urls)}")

    with open(filepath, 'w', encoding='utf-8') as f:
        for (num, url) in enumerate(routes_urls):
            if num % 100 == 0:
                print(f"Route num - {num}")
            route_object = Classes.RouteClassKP.RouteKP()
            route_object.parse_page(url, session, headers)
            f.write(str(route_object.to_json()) + '\n')


if __name__ == '__main__':
    main()
