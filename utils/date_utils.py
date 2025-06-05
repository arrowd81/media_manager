import datetime

from cachetools.func import ttl_cache

from database.media import Seasons


def get_season_from_date(date: datetime.date):
    match date.month:
        case 3 | 4 | 5:
            return Seasons.SPRING
        case 6 | 7 | 8:
            return Seasons.SUMMER
        case 9 | 10 | 11:
            return Seasons.FALL
        case _:
            return Seasons.WINTER


@ttl_cache(ttl=24 * 60 * 60)
def get_current_season():
    return get_season_from_date(datetime.date.today())
