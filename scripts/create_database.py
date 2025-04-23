from database import db_engine
from database import BaseDbClass


def create_db():
    from database.media import Media, MediaNames, MediaCategories  # noqa
    from database.user import User, UserMovie  # noqa

    BaseDbClass.metadata.create_all(db_engine)


if __name__ == '__main__':
    create_db()
