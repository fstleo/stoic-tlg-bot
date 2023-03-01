import json


class User:

    user_id = ""
    time = "7:00"

    def __init__(self, user_id, time):
        self.user_id = user_id
        self.time = time

    def set_time(self, time):
        self.time = time

    def __iter__(self):
        yield from {
            "user_id": self.user_id,
            "time": self.time,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        user = User(json_dct['user_id'], json_dct['time'])
        return user
