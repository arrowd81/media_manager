import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from database import BaseDbClass


class Seasons(enum.Enum):
    SPRING = 0
    SUMMER = 1
    FALL = 2
    WINTER = 3


class Media(BaseDbClass):
    __tablename__ = 'media'
    main_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    number_of_votes = Column(Integer, nullable=False)
    data_url = Column(String, nullable=False)
    number_of_episodes = Column(Integer, nullable=False)
    premiered_year = Column(Integer, nullable=False)
    premiered_season = Column(Enum(Seasons), nullable=False)
    source = Column(String, nullable=False)


class MediaNames(BaseDbClass):
    __tablename__ = 'media_name'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)


class MediaCategories(BaseDbClass):
    __tablename__ = 'media_categories'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)


class MediaProducers(BaseDbClass):
    __tablename__ = 'media_producers'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)


class MediaStudents(BaseDbClass):
    __tablename__ = 'media_students'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
