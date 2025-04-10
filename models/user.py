from sqlalchemy import Column, String, Integer, ForeignKey, Numeric

from models import BaseDbClass


class User(BaseDbClass):
    __tablename__ = 'user'
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class UserMovie(BaseDbClass):
    __tablename__ = 'user_movie'
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
    score = Column(Numeric(3, 1))
