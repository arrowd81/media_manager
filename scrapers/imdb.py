import re

from bs4 import BeautifulSoup

from scrapers import Scraper
from utils.request_utils import safe_request


class ImdbScraper(Scraper):
    req_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36'}

    @classmethod
    def find_link(cls, name: str, confirm=False):
        response = safe_request('get', f'https://www.imdb.com/find/?q={name}&exact=true', headers=cls.req_headers)
        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find_all('li',
                               class_='ipc-metadata-list-summary-item '
                                      'ipc-metadata-list-summary-item--click '
                                      'find-result-item find-title-result')
        for item in result:
            link = item.find('a', class_='ipc-metadata-list-summary-item__t')
            if link.text == name:
                return link.get('href')
        with open("./this.html", 'w') as file:
            file.write(response.text)
        return input(f"couldn't find imdb link for {name} enter the imdb link: ")

    @classmethod
    def get_site_id_from_link(cls, link):
        return re.search(r'/title/tt(\d+)', link).group(1)

    @classmethod
    def get_data(cls, site_id):
        response = safe_request('get', 'https://www.imdb.com/title/tt' + site_id, headers=cls.req_headers)
        soup = BeautifulSoup(response.content, "html.parser")
        rating = float(soup.find('div', {"data-testid": 'hero-rating-bar__aggregate-rating__score'}).text.split('/')[0])
        genres = soup.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
        out = {'Genres': [], 'rating': rating}
        print('and genres are :')
        for item in genres:
            out['Genres'].append(item.find('span', class_='ipc-chip__text').text)
        return out


if __name__ == '__main__':
    link = ImdbScraper.find_link("The Batman")
    print(ImdbScraper.get_data(ImdbScraper.get_site_id_from_link(link)))
