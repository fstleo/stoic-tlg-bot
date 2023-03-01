import json

from EntityEncoder import EntityEncoder


class JsonListKeeper:

    def __init__(self, file_name):
        self.file = file_name

    def save(self, entities_list):
        with open(self.file, "w") as fp:
            json.dump(entities_list, fp, cls=EntityEncoder)

    def load(self):
        try:
            with open(self.file, "rb") as fp:
                entities = json.load(fp)
            return entities
        except:
            return dict()
