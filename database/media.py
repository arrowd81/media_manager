from sqlalchemy import Column, String, Integer, ForeignKey

from database import BaseDbClass


class Media(BaseDbClass):
    __tablename__ = 'media'
    main_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    data_url = Column(String, nullable=False)


class MediaNames(BaseDbClass):
    __tablename__ = 'media_name'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)


class MediaCategories(BaseDbClass):
    __tablename__ = 'media_categories'
    name = Column(String, nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
