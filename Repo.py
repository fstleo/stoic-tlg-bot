from User import User


class Repo:

    entity_list = {}

    def __init__(self, list_source):
        self.list_keeper = list_source
        jsons = list_source.load()
        for key in jsons.keys():
            json = jsons[key]
            self.entity_list[key] = User(json["user_id"], json["time"])

    def get_all(self):
        return self.entity_list.values()

    def add(self, entity):
        if entity.user_id not in self.entity_list.keys():
            self.entity_list[entity.user_id] = entity
            self.save()
        else:
            raise Exception

    def delete(self, user_id):
        if user_id in self.entity_list:
            self.entity_list.pop(user_id)
            self.save()

    def get(self, user_id):
        return self.entity_list[user_id]

    def update(self, user):
        self.entity_list[user.user_id] = user
        self.save()

    def save(self):
        self.list_keeper.save(self.entity_list)

    def load_entity_list(self):
        return self.list_keeper.load()
