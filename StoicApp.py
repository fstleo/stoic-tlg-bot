from datetime import datetime

from User import User


class StoicApp:

    observers = []

    def __init__(self, timers_keeper, users, picture_provider):
        self.timers_keeper = timers_keeper
        self.users = users
        self.picture_provider = picture_provider
        for user in users.get_all():
            self.add_timer(user)

    def add_observer(self, observer):
        self.observers.append(observer)

    def send_today(self, user_id):
        current_day = datetime.now()
        for observer in self.observers:
            observer.send_today(user_id, self.picture_provider.get(current_day))

    def add_timer(self, user):
        self.timers_keeper.add(user.chat_id, user.send_time, self.send_today(user.chat_id))

    def subscribe(self, chat_id, time):
        try:
            user = self.users.get_by_chat_id(chat_id)
            user.set_time(time)
            self.users.update(user)
            self.timers_keeper.delete(user.chat_id)
            self.add_timer(user)
            for observer in self.observers:
                observer.subscribed(chat_id, time, True)
        except:
            user = User(chat_id, time)
            self.users.add(user)
            self.add_timer(user)
            for observer in self.observers:
                observer.subscribed(chat_id, time, False)

    def unsubscribe(self, chat_id):
        try:
            user = self.users.get_by_chat_id(chat_id)
            self.users.delete(user)
            print(chat_id, " unsubscribed")
            self.timers_keeper.delete(chat_id)
            for observer in self.observers:
                observer.unsubscribed(chat_id, True)
        except:
            print(chat_id, " already unsubscribed")
            for observer in self.observers:
                observer.unsubscribed(chat_id, False)

