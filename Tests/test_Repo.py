from unittest import TestCase
from Repo import Repo
from unittest.mock import MagicMock
from User import User

class TestRepo(TestCase):

    def setUp(self):
        self.list_source = MagicMock()
        self.list_source.load.return_value = []
        self.repo = Repo(self.list_source)

    def test_load_called(self):
        self.list_source.load.assert_called()

    def test_get_all(self):
        self.list_source.load.return_value = [5, 12, 22]
        self.repo = Repo(self.list_source)
        self.assertEqual(3, len(self.repo.get_all()))

    def test_add(self):
        self.repo.add(User(1))
        self.assertEqual(1, len(self.repo.get_all()))
        self.list_source.save.assert_called()

    def test_delete(self):
        self.repo.add(User(1))
        self.list_source.save.assert_called()
        self.repo.delete(1)
        self.list_source.save.assert_called()
        self.assertEqual(0, len(self.repo.get_all()))
