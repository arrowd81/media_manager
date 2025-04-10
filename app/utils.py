from typing import Annotated

from fastapi import Depends

from database import session_maker


def _get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[session_maker, Depends(_get_db)]
