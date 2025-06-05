import os
import traceback

import requests

from config import anime_list_proxy
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


def get_anime_data(anime_name):
    anime_link = None
    while True:
        if not anime_link:
            anime_link = AnimeListScraper.find_link(anime_name)
        try:
            media_data = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(anime_link))
        except Exception as e:
            anime_link = input(
                f"Error getting data for {anime_name}, link:{anime_link}\n"
                f"Error:{e}\n"
                f"{traceback.format_exc()}\n"
                f"enter new anime link or nothing to retry: ")
            if not anime_link:
                continue
        else:
            return anime_link, media_data


def download_image(anime_name: str, url: str):
    name = anime_name.replace("/", "\\").replace("?", "") + url[url.rfind('.'):]
    image_path = "frontend/pictures/" + name
    if os.path.exists(image_path):
        return name  # todo: check and update the file
        # raise FileExistsError(f"file {name} already exists")
    while True:
        try:
            response = requests.get(url, proxies=anime_list_proxy)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            image_url = input(f"could not download image with error: {e} (enter image url or nothing to retry)")
            if image_url:
                url = image_url
            else:
                continue
        else:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return name


def main(location):
    data = scan_dir(location)
    for d in data:
        if db_session.query(Media).where(Media.location == d['path']).first() is not None:
            continue
        anime_link, media_data = get_anime_data(d["name"])
        main_name = media_data.eng_name or media_data.name
        image_path = download_image(main_name, media_data.image_url)
        media = Media(
            main_name=main_name,
            data_url=anime_link,
            location=d['path'],
            rating=media_data.score,
            number_of_votes=media_data.number_of_votes,
            number_of_episodes=media_data.number_of_episodes,
            premiered_year=media_data.premiered_year,
            premiered_season=media_data.premiered_season,
            source=media_data.source,
            image_path=image_path
        )
        media.save()
        if media_data.eng_name:
            MediaNames(name=media_data.name, media_id=media.id).save()
        for genre in media_data.genres:
            MediaCategories(name=genre, media_id=media.id).save()
        db_session.commit()


if __name__ == '__main__':
    main('/run/media/arrow/New Volume/[01] Everyone/[02] Amine/[02] Serial')
