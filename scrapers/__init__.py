class Scraper:
    @classmethod
    def find_link(cls, name):
        raise NotImplemented

    @staticmethod
    def get_site_id_from_link(link):
        raise NotImplemented

    @classmethod
    def get_data(cls, site_id):
        raise NotImplemented

    def save_to_database(self):
        raise NotImplemented
