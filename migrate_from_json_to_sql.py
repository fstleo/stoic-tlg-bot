import json
from datetime import datetime

from SQLRepo import SQLRepo
from User import User


def migrate(file_name, repo):
    with open(file_name, "rb") as fp:
        entities = json.load(fp)
    for key in entities.keys():
        user_entry = entities[key]
        print(user_entry)
        time = datetime.strptime(user_entry["time"], '%H:%M').time()
        try:
            repo.add(User(user_entry["user_id"], time));
        except:
            print("Can't add user ", user_entry)


if __name__ == '__main__':
    migrate("users.json", SQLRepo("users.db", "users"))
