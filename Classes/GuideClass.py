class Guide:
    def __init__(self):
        self.name = None
        self.img = []
        self.phone = None
        self.email = None
        self.url = None

    def to_json(self):
        self.json_dict = dict()
        self.json_dict['name'] = self.name
        self.json_dict['img'] = self.img
        self.json_dict['phone'] = self.phone
        self.json_dict['email'] = self.email
        self.json_dict['url'] = self.url
        return self.json_dict