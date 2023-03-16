from sqlalchemy.types import Time
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(String(9), unique=True)
    send_time = Column(Time)

    def __init__(self, chat_id, send_time):
        self.chat_id = chat_id
        self.send_time = send_time

    def set_time(self, send_time):
        self.send_time = send_time
