import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from config import anime_list_proxy
from database.media import Seasons
from scrapers import Scraper
from utils.request_utils import safe_request


@dataclass
class AnimeListData:
    name: str = None
    score: float = None
    number_of_votes: int = None
    eng_name: str = None
    genres: list[str] = field(default_factory=list)
    number_of_episodes: int = None
    premiered_season: Seasons = None
    premiered_year: int = None
    producers: list[str] = field(default_factory=list)
    studios: list[str] = field(default_factory=list)
    source: str = None

    def assert_complete(self):
        assert (
                self.name
                and self.score
                and self.number_of_votes
                and self.genres
                and self.number_of_episodes
                and self.premiered_season
                and self.premiered_year
                and self.producers
                and self.studios
                and self.source
        )


class AnimeListScraper(Scraper):
    seasons_map = {"Spring": Seasons.SPRING, "Summer": Seasons.SUMMER, "Fall": Seasons.FALL, "Winter": Seasons.WINTER}

    @classmethod
    def find_link(cls, name: str, confirm=False):
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

        info_list = soup.find_all('div', class_='spaceit_pad')
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
                        data.premiered_season, data.premiered_year = info.find('a').text.split()
                    case 'Producers':
                        producers = info.find_all('a')
                        for i in producers:
                            data.producers.append(i.text)
                    case 'Studios':
                        studios = info.find_all('a')
                        for i in studios:
                            data.studios.append(i.text)
                    case 'Source':
                        data.source = info.find('a').text.strip()
        data.assert_complete()
        return data


if __name__ == '__main__':
    link = AnimeListScraper.find_link("Frieren beond")
    out = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(link))
    print(out)
