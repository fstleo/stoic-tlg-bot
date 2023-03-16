import datetime
import unittest
from unittest.mock import MagicMock, Mock, patch

from RepoExceptions import NotFoundError
from StoicApp import StoicApp
from User import User


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.timers_keeper = MagicMock()
        self.users = MagicMock()
        self.picture_provider = MagicMock()

    def test_app_init_existing_users_send_scheduled(self):
        first_user = User(1, "12:00")
        second_user = User(2, "14:00")
        self.users.get_all.return_value = [first_user, second_user]
        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.timers_keeper.add.assert_any_call(first_user.chat_id, first_user.send_time, self.app.send_today(first_user.chat_id))
        self.timers_keeper.add.assert_any_call(second_user.chat_id, second_user.send_time, self.app.send_today(second_user.chat_id))

    def test_subscribe_new_user_added_to_list(self):
        user_id = 1
        time = "3:00"
        self.users.get_by_chat_id.return_value = None
        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.subscribe(user_id, time)
        user, = self.users.add.call_args.args
        self.assertEqual(user_id, user.chat_id)
        self.assertEqual(time, user.send_time)

    def test_subscribe_new_user_adds_timer(self):
        self.users.get_by_chat_id.return_value = None
        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        new_time = "3:00"
        user_id = 1

        self.app.subscribe(user_id, new_time)

        self.timers_keeper.add.assert_any_call(user_id, new_time, self.app.send_today(user_id))

    def test_subscribe_new_user_observers_notified(self):
        self.users.get_by_chat_id.return_value = None
        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        subscription_observer = MagicMock()
        self.app.add_observer(subscription_observer)
        new_time = "3:00"
        user_id = 1

        self.app.subscribe(user_id, new_time)

        subscription_observer.subscribed.assert_called_once_with(user_id, new_time, False)

    def test_subscribe_existing_user_sets_user_time(self):
        user_id = 1
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user
        new_time = "5:00"

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.subscribe(user_id, new_time)

        self.assertEqual(new_time, user.send_time)

    def test_subscribe_existing_user_deletes_old_timer_adds_new_one(self):
        user_id = 1
        new_time = "5:00"
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.subscribe(user_id, new_time)

        self.timers_keeper.delete.assert_any_call(user.chat_id)
        self.timers_keeper.add.assert_any_call(user.chat_id, new_time, self.app.send_today(user.chat_id))

    def test_subscribe_existing_user_updates_user(self):
        user_id = 1
        new_time = "5:00"
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.subscribe(user_id, new_time)

        set_timer_user, = self.users.update.call_args.args
        self.assertEqual(user, set_timer_user)

    def test_subscribe_existing_user_observers_notified(self):
        user_id = 1
        new_time = "5:00"
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        subscription_observer = MagicMock()
        self.app.add_observer(subscription_observer)

        self.app.subscribe(user_id, new_time)

        subscription_observer.subscribed.assert_called_once_with(user_id, new_time, True)

    def test_unsubscribe_existing_user_removed_from_list(self):
        user_id = 1
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.unsubscribe(user_id)

        deleted_user, = self.users.delete.call_args.args
        self.assertEqual(user, deleted_user)

    def test_unsubscribe_existing_user_timer_deleted(self):
        user_id = 1
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        self.app.unsubscribe(user_id)

        self.timers_keeper.delete.assert_any_call(user.chat_id)

    def test_unsubscribe_existing_user_observers_notified(self):
        user_id = 1
        user = User(user_id, "3:00")
        self.users.get_by_chat_id.return_value = user

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        subscription_observer = MagicMock()
        self.app.add_observer(subscription_observer)

        self.app.unsubscribe(user_id)

        subscription_observer.unsubscribed.assert_called_once_with(user_id, True)

    def test_unsubscribe_non_existing_user_observers_notified(self):
        user_id = 1
        self.users.get_by_chat_id.side_effect = Mock(side_effect=NotFoundError('User not found'))

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        subscription_observer = MagicMock()
        self.app.add_observer(subscription_observer)

        self.app.unsubscribe(user_id)

        subscription_observer.unsubscribed.assert_called_once_with(user_id, False)

    def test_send_today(self):
        now_is_like = datetime.datetime(2023, 5, 1)
        with patch('StoicApp.datetime') as mock_date:
            mock_date.now.return_value = now_is_like
        user_id = 1

        self.app = StoicApp(self.timers_keeper, self.users, self.picture_provider)
        subscription_observer = MagicMock()
        self.app.add_observer(subscription_observer)
        self.app.send_today(user_id)

        subscription_observer.send_today.assert_called_once_with(user_id, self.picture_provider.get(now_is_like))

    "SELECT * FROM spaces WHERE LOCATE('|', name) > 0;"

if __name__ == '__main__':
    unittest.main()
