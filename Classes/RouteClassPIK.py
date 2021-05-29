from bs4 import BeautifulSoup
import re
from Classes.RouteClass import Route
from Classes.GuideClass import Guide
from Classes.HikeClass import Hike


def catch_exceptions(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args)
        except:
            print(f"{args[0].url} - problem in {func.__name__}")
    return inner_function



class RoutePIK(Route):
    @catch_exceptions
    def parse_name(self):
        return self.soup.find(attrs={'class': 'title name'}).text

    @catch_exceptions
    def parse_region(self):
        return self.soup.find(attrs={'itemprop': 'location'}).find(attrs={'itemprop': 'name'}).get('content')

    @catch_exceptions
    def parse_duration(self):
        duration_text = [col.text for col in self.main_route_info if 'Длительность' in col.text]
        return duration_text[0]

    @catch_exceptions
    def parse_distance(self):
        distance_text = [col.text for col in self.main_route_info if 'Длина' in col.text]
        return distance_text[0]

    @catch_exceptions
    def parse_level(self):
        level_text = [col.text for col in self.main_route_info if 'Сложность' in col.text]
        return level_text[0]

    @catch_exceptions
    def parse_group_size(self):
        group_size_text = [col.text for col in self.main_route_info if 'Размер группы' in col.text]
        return group_size_text[0]

    @catch_exceptions
    def parse_type(self):
        return [tag.text for tag in self.soup.find(attrs={'class': 'tags'}).find_all('a')]

    @catch_exceptions
    def parse_short_description(self):
        return self.soup.find('meta', attrs={'property': 'og:description'}).get('content')

    @catch_exceptions
    def parse_full_description(self):
        all_text = []
        days_tags = self.soup.find(attrs={'class': 'days'}).find_all(attrs={'class': re.compile('columns day')})
        for day_tag in days_tags:
            all_text += [tag.text for tag in day_tag.find_all('div') if tag.get('class')[0] not in ['photos', 'description']]
        return '\n'.join(all_text)

    @catch_exceptions
    def parse_img(self):
        gallery = self.soup.find(attrs={'class': 'gallery'}).find_all('a')
        images = [self.source + tag.get('href') for tag in gallery]
        mini_images = [tag.find('meta', attrs={'itemprop': 'contentUrl'}).get('content') for tag in gallery]
        return mini_images, images

    @catch_exceptions
    def parse_guides(self):
        guides_info = self.soup.find(attrs={'class': 'aside'}).find_all('a', attrs={'class': 'team-member'})
        for guide_soup in guides_info:
            try:
                guide = Guide()
                guide.img = guide_soup.find(attrs={'itemprop': 'contentUrl'}).get('content')
                guide.name = guide_soup.find(attrs={'class': 'name'}).text
                self.guides.append(guide)
            except:
                pass

    @catch_exceptions
    def parse_hikes(self):
        hikes = self.soup.find_all('span', attrs={'itemtype': 'http://schema.org/Event'})
        for hike_soup in hikes:
            try:
                hike = Hike()
                hike.group_size = self.group_size
                hike.is_full = False
                hike.date_start = hike_soup.find('meta', attrs={'itemprop': 'startDate'}).get('content')
                hike.date_end = hike_soup.find('meta', attrs={'itemprop': 'endDate'}).get('content')
                hike.price = hike_soup.find('span', attrs={'itemprop': 'price'}).get('content')
                hike.price_curr = hike_soup.find('span', attrs={'itemprop': 'priceCurrency'}).get('content')
                self.hikes.append(hike)
            except:
                pass

    def parse_page(self, url, session, headers):
        self.source = 'https://turclub-pik.ru'
        self.url = url
        self.page = session.get(self.url, headers=headers)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        self.main_route_info = self.soup.find(attrs={'class': 'info'}).find_all(attrs={'class': 'item'})

        self.name = self.parse_name()
        self.region = self.parse_region()
        self.distance = self.parse_distance()
        self.duration = self.parse_duration()
        self.level = self.parse_level()
        self.group_size = self.parse_group_size()
        self.type = self.parse_type()
        self.short_description = self.parse_short_description()
        self.full_description = self.parse_full_description()
        try:
            self.mini_images, self.images = self.parse_img()
        except:
            pass
        self.parse_guides()
        self.parse_hikes()


