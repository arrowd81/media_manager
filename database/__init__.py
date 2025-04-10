from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import RDBMS_URL

db_engine = create_engine(RDBMS_URL)
session_maker = sessionmaker(db_engine)
db_session = session_maker()
Base = declarative_base()


class BaseDbClass(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    def save(self, session: Session = db_session):
        session.add(self)
        session.flush()
        session.refresh(self)
