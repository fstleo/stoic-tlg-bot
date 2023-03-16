import sqlite3

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from RepoExceptions import AlreadyCreatedError, NotFoundError
from User import User


class SQLRepo:

    def __init__(self, db_path):
        engine = create_engine("sqlite:///{}".format(db_path), echo=True)
        self.session = sessionmaker(bind=engine)()

    def get_all(self):
        return self.session.query(User).all()

    def add(self, entity):
        try:
            self.session.add(entity)
            self.session.commit()
        except:
            raise AlreadyCreatedError()

    def delete(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
        except:
            raise NotFoundError()

    def get_by_chat_id(self, required_chat_id):
        try:
            return self.session.query(User).filter_by(chat_id=required_chat_id).first()
        except:
            raise NotFoundError()

    def get(self, entity_id):
        try:
            return self.session.get(User, entity_id)
        except:
            raise NotFoundError()

    def update(self, entity):
        self.session.commit()

