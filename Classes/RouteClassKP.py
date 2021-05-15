from bs4 import BeautifulSoup
import re
from Classes.RouteClass import Route
from Classes.GuideClass import Guide


def catch_exceptions(func):
    def inner_function(*args, **kwargs):
        try:
            return func(args[0])
        except:
            print(f"{args[0].url} - problem in {func.__name__}")
    return inner_function


class RouteKP(Route):
    @catch_exceptions
    def parse_name(self):
        return self.soup.find(attrs={'class' : 'main_top full_width'}).find().text

    @catch_exceptions
    def parse_region(self):
        return [col for col in self.main_route_info if 'Регион:' in col.text][0].text.replace('\n', '')

    @catch_exceptions
    def parse_track(self):
        return [col for col in self.main_route_info if 'Нитка:' in col.text][0].text.replace('\n', '')

    @catch_exceptions
    def parse_distance(self):
        return [col for col in self.main_route_info if 'Длина:' in col.text][0].text.replace('\n', '')

    @catch_exceptions
    def parse_duration(self):
        return [col for col in self.main_route_info if 'Длительность:' in col.text][0].text.replace('\n', '')

    @catch_exceptions
    def parse_group_size(self):
        return [col for col in self.main_route_info if 'Размер группы:' in col.text][0].text.replace('\n','')

    @catch_exceptions
    def parse_children(self):
        return [col for col in self.main_route_info if 'Участие с детьми:' in col.text][0].text.replace('\n', '')

    @catch_exceptions
    def parse_level(self):
        return [col for col in self.main_route_info if 'difficult' in str(col)][0].text.replace('\n', '')

    @catch_exceptions
    def parse_type(self):
        type_pattern_re = re.compile('.*>([\w\s]+)<.*')
        return  [re.search(type_pattern_re,col['title']).group(1)
                 for col in self.soup.find(attrs={'class':'route_icons'}).children]

    @catch_exceptions
    def parse_short_description(self):
        short_desc = self.soup.find(attrs={'id':'route-short-description-content'})
        return '\n'.join(map(lambda x: x.text, short_desc.find_all('p')))

    # @catch_exceptions
    def parse_guides(self):
        guides_list = self.soup.find_all(attrs={'class': re.compile(r'^route_coordinator$')})
        guide_object_list = []
        for guide_soup in guides_list:
            guide = Guide()
            guide.img = [guide_soup.find(attrs={'class': 'route_coordinator_left'}).find('img').attrs['src']]
            guide.name = guide_soup.find(attrs={'class': 'route_coordinator_name'}).text
            guide.url = guide_soup.find(attrs={'class': 'route_coordinator_name'}).get('href')
            if guide.url:
                guide.url = self.root_url + guide.url
            guide_object_list.append(guide)
        return guide_object_list


    def parse_page(self, url, session, headers):
        self.root_url = 'https://www.vpoxod.ru'
        self.url = url
        self.page = session.get(self.url, headers=headers)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')

        self.name = self.parse_name()
        self.main_route_info = self.soup.find(attrs={'class':'route_top_center'}).find_all('li')
        self.region = self.parse_region()
        self.track = self.parse_track()
        self.distance = self.parse_distance()
        self.duration = self.parse_duration()
        self.group_size = self.parse_group_size()
        self.is_children = self.parse_children()
        self.level = self.parse_level()
        self.type = self.parse_type()
        self.short_description = self.parse_short_description()
        self.guides = self.parse_guides()
