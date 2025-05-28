import os

from database import db_session
from database.media import Media, MediaNames, MediaCategories
from scrapers.animelist import AnimeListScraper


def scan_dir(location):
    data_found = []
    with os.scandir(location) as itemlist:
        for item in itemlist:
            if not item.name.startswith('#'):
                data_found.append({"name": item.name, "path": item.path})
    return data_found


def main(location):
    data = scan_dir(location)
    for d in data:
        if db_session.query(Media).where(Media.location == d['path']).first() is not None:
            continue
        try:
            anime_link = AnimeListScraper.find_link(d["name"])
            media_data = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(anime_link))
        except Exception as e:
            anime_link = input(f"Error getting data for {d['name']}\nError:{e}\nenter new anime link: ")
            media_data = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(anime_link))
        media = Media(
            main_name=media_data.eng_name or media_data.name,
            data_url=anime_link,
            location=d['path'],
            rating=media_data.score,
            number_of_votes=media_data.number_of_votes,
            number_of_episodes=media_data.number_of_episodes,
        )
        media.save()
        if media_data.eng_name:
            MediaNames(name=media_data.name, media_id=media.id).save()
        for genre in media_data.genres:
            MediaCategories(name=genre, media_id=media.id).save()
        db_session.commit()


if __name__ == '__main__':
    main('/run/media/arrow/New Volume/[01] Everyone/[02] Amine/[02] Serial')
