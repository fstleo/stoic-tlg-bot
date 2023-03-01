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
        def send():
            self.send_today(user.user_id)

        self.timers_keeper.add(user.user_id, user.time, send)

    def subscribe(self, user_id, time):
        try:
            user = User(user_id, time)
            self.users.add(user)
            self.add_timer(user)
        except:
            user = self.users.get(user_id)
            user.set_time(time)
            self.users.update(user)
        finally:
            for observer in self.observers:
                observer.subscribed(user_id, time, True)

    def unsubscribe(self, user_id):
        try:
            self.users.delete(user_id)
            self.timers_keeper.delete(user_id)
            for observer in self.observers:
                observer.unsubscribed(user_id, True)
        except:
            for observer in self.observers:
                observer.unsubscribed(user_id, False)

