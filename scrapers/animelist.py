import re

from bs4 import BeautifulSoup

from config import anime_list_proxy
from scrapers import Scraper
from utils.request_utils import safe_request


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
        score_tag = soup.find('div', class_='fl-l score')
        out = {
            'name': soup.find('h1', class_='title-name h1_bold_none').text,
            'score': float(score_tag.text),
            'number_of_votes': int(re.sub(r'\D', '', score_tag['data-user'])),
            'eng_name': '',
            'Genres': [],
            'Episodes': None,
            'Premiered': '',
            'Producers': [],
            'Studios': [],
        }

        info_list = soup.find_all('div', class_='spaceit_pad')
        for info in info_list:
            title = info.find('span', class_='dark_text')
            if title is not None:
                match title.text[:-1]:
                    case 'English':
                        out['eng_name'] = info.text.strip()[info.text.find(':') + 1:]
                    case 'Genres' | 'Genre':
                        names = info.find_all('a')
                        for i in names:
                            out['Genres'].append(i.text)
                    case 'Episodes':
                        out['Episodes'] = int(info.text[info.text.find(':') + 1:].strip())
                    case 'Premiered':
                        out['Premiered'] = info.find('a').text
                    case 'Producers':
                        producers = info.find_all('a')
                        for i in producers:
                            out['Producers'].append(i.text)
                    case 'Studios':
                        studios = info.find_all('a')
                        for i in studios:
                            out['Studios'].append(i.text)
                    case 'Source':
                        out['Source'] = info.find('a').text.strip()

        return out


if __name__ == '__main__':
    link = AnimeListScraper.find_link("Frieren beond")
    out = AnimeListScraper.get_data(AnimeListScraper.get_site_id_from_link(link))
    print(out)
