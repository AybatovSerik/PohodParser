class Route:
    def __init__(self):
        self.url = None
        self.name = None
        self.region = None
        self.track = None
        self.distance = None
        self.level = None
        self.type = None
        self.duration = None
        self.group_size = None
        self.is_children = None
        self.short_description = None
        self.full_description = None
        self.price = None
        self.images = []
        self.guides = []

    def to_json(self):
        self.json_dict = dict()
        self.json_dict['url'] = self.url
        self.json_dict['name'] = self.name
        self.json_dict['region'] = self.region
        self.json_dict['track'] = self.track
        self.json_dict['distance'] = self.distance
        self.json_dict['level'] = self.level
        self.json_dict['type'] = self.type
        self.json_dict['duration'] = self.duration
        self.json_dict['group_size'] = self.group_size
        self.json_dict['is_children'] = self.is_children
        self.json_dict['short_description'] = self.short_description
        self.json_dict['full_description'] = self.full_description
        self.json_dict['price'] = self.price
        self.json_dict['images'] = self.images
        if len(self.guides) == 0:
            self.json_dict['guides'] = []
        else:
            self.json_dict['guides'] = [guide.to_json() for guide in self.guides]
        return self.json_dict
