from json import JSONEncoder


class EntityEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
