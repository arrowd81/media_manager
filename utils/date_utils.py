from datetime import date

from cachetools.func import ttl_cache

from database.media import Seasons


@ttl_cache(ttl=24 * 60 * 60)
def get_current_season():
    match date.today().month:
        case 3 | 4 | 5:
            return Seasons.SPRING
        case 6 | 7 | 8:
            return Seasons.SUMMER
        case 9 | 10 | 11:
            return Seasons.FALL
        case _:
            return Seasons.WINTER
