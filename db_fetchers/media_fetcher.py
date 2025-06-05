from datetime import date

from sqlalchemy import select, or_, and_
from sqlalchemy.orm.session import Session

from database.media import Media, Seasons
from utils.date_utils import get_current_season


class MediaFetcherDB:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @staticmethod
    def _latest_anime(stmt):
        current_season = get_current_season()
        current_year = date.today().year
        seasons_last_year = 3 - current_season.value
        return stmt.where(
            or_(
                and_(
                    Media.premiered_year == current_year,
                    Media.premiered_season.in_([Seasons(i) for i in range(current_season.value, -1, -1)])
                ),
                and_(
                    Media.premiered_year == current_year - 1,
                    Media.premiered_season.in_([Seasons(3 - i) for i in range(seasons_last_year)])
                )
            )
        )

    def get_new_top_media(self):
        stmt = self._latest_anime(select(Media))
        top_new = self.db_session.execute(stmt.order_by(Media.rating)).scalars().all()
        if len(top_new) <= 20:
            new_count = 20 - len(top_new)
            top_new += self.db_session.execute(
                select(Media).order_by(Media.rating).limit(new_count)
            ).scalars().all()
        return top_new
