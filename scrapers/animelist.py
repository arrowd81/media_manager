import re
import traceback
from dataclasses import dataclass, field, fields
from datetime import datetime

from bs4 import BeautifulSoup

from config import anime_list_proxy
from database.media import Seasons
from scrapers import Scraper
from utils.date_utils import get_season_from_date
from utils.request_utils import safe_request


@dataclass
class AnimeListData:
    name: str = None
    score: float = None
    number_of_votes: int = None
    eng_name: str = ''
    genres: list[str] = field(default_factory=list)
    number_of_episodes: int = None
    premiered_season: Seasons = None
    premiered_year: int = None
    producers: list[str] = field(default_factory=list)
    studios: list[str] = field(default_factory=list)
    source: str = None
    image_url: str = None

    def check_and_complete(self):
        for f in fields(self):
            if getattr(self, f.name) is None:
                value = input(f"unable to find {f.name} enter the value you want to enter (or nothing to set None):")
                if value:
                    if f.type == list[str]:
                        getattr(self, f.name).append(value)
                    elif f.type == Seasons:
                        setattr(self, f.name, Seasons(int(value)))
                    else:
                        setattr(self, f.name, f.type(value))


class AnimeListScraper(Scraper):
    seasons_map = {"Spring": Seasons.SPRING, "Summer": Seasons.SUMMER, "Fall": Seasons.FALL, "Winter": Seasons.WINTER}

    @classmethod
    def find_link(cls, name: str, confirm=False):
        while True:
            try:
                response = safe_request('get', 'https://myanimelist.net/search/all?q=' + name, proxies=anime_list_proxy)
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', class_='hoverinfo_trigger fw-b fl-l')
                for link in links:
                    link_ = link.get('href')
                    if confirm:
                        answer = input(f"found link {link_} for {name} correct? [Y/n] ")
                        if answer != 'n':
                            continue
                    print(f"found link {link_} for {name}")
                    return link_
                return input(f"couldn't find animelist link for {name} enter the animelist link: ")
            except Exception as e:
                new_link = input(
                    f"Error getting data for {name}\nError:{e}\n{traceback.format_exc()}\nenter new anime link"
                    f"or nothing to retry: ")
                if new_link:
                    return new_link

    @classmethod
    def get_site_id_from_link(cls, link):
        return re.search(r'/anime/(\d+)', link).group(1)

    @classmethod
    def get_data(cls, site_id: str):
        response = safe_request('get', 'https://myanimelist.net/anime/' + site_id, proxies=anime_list_proxy)
        soup = BeautifulSoup(response.content, 'html.parser')
        score_tag = soup.find('div', class_='fl-l score')
        data = AnimeListData(
            name=soup.find('h1', class_='title-name h1_bold_none').text,
            score=float(score_tag.text),
            number_of_votes=int(re.sub(r'\D', '', score_tag['data-user'])),
        )
        data.image_url = soup.find('img', alt=data.name)['data-src']

        info_list = soup.find_all('div', class_='spaceit_pad')
        aired = None
        for info in info_list:
            title = info.find('span', class_='dark_text')
            if title is not None:
                match title.text[:-1]:
                    case 'English':
                        data.eng_name = info.text.strip()[info.text.find(':') + 1:]
                    case 'Genres' | 'Genre':
                        names = info.find_all('a')
                        for i in names:
                            data.genres.append(i.text)
                    case 'Episodes':
                        data.number_of_episodes = int(info.text[info.text.find(':') + 1:].strip())
                    case 'Premiered':
                        premiered_season, data.premiered_year = info.find('a').text.split()
                        data.premiered_season = cls.seasons_map[premiered_season]
                    case 'Producers':
                        producers = info.find_all('a')
                        for i in producers:
                            data.producers.append(i.text)
                    case 'Studios':
                        studios = info.find_all('a')
                        for i in studios:
                            data.studios.append(i.text)
                    case 'Source':
                        data.source = info.text.strip()[info.text.find(':') + 1:].strip()
                    case 'Aired':
                        aired = info.text.strip()[info.text.find(':') + 1:].strip()
        if (not data.premiered_season or not data.premiered_year) and aired:
            try:
                from_date_string = aired.split(" to ")[0]
                start_date = datetime.strptime(from_date_string, "%b %d, %Y")
                data.premiered_year = start_date.year
                data.premiered_season = get_season_from_date(start_date)
            except Exception as e:
                print(f"couldn't get premiered year from {aired}: {e}")
            else:
                print(f"found premiered year and season from {aired}: "
                      f"{data.premiered_year}, {data.premiered_season.name}")
        data.check_and_complete()
        return data


if __name__ == '__main__':
    link = AnimeListScraper.find_link("Frieren beond")
    out = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(link))
    print(out)
