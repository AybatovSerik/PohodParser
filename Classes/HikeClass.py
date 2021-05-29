class Hike:
    def __init__(self):
        self.price = None
        self.date_start = None
        self.date_end = None
        self.group_size = None
        self.is_full = None
        self.json_dict = dict()

    def to_json(self):
        self.json_dict['price'] = self.price
        self.json_dict['date_start'] = self.date_start
        self.json_dict['date_end'] = self.date_end
        self.json_dict['group_size'] = self.group_size
        self.json_dict['is_full'] = self.is_full
        return self.json_dict
