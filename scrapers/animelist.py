import re

from bs4 import BeautifulSoup

from scrapers import Scraper
from utils.request_utils import safe_request

from config import anime_list_proxy


class AnimeListScraper(Scraper):
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
        info_list = soup.find_all('div', class_='spaceit_pad')
        out = {'name': soup.find('h1', class_='title-name h1_bold_none').text,
               'eng_name': '',
               'score': float(soup.find('div', class_='fl-l score').text),
               'Genres': []}
        for info in info_list:
            title = info.find('span', class_='dark_text')
            if title is not None and title.text[:-1] in ['English', 'Genres', 'Genre']:
                names = info.find_all('a')
                if names:
                    for i in names:
                        out['Genres'].append(i.text)
                else:
                    out['eng_name'] = info.text.strip()[info.text.find(':') + 1:]
        return out



if __name__ == '__main__':
    link = AnimeListScraper.find_link("Frieren beond")
    print(AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(link)))
