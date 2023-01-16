from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus


class SupermarketSite:

    def __init__(self, food_item_searched, supermarket_site_url):
        self.__searched_url = supermarket_site_url.format(quote_plus(food_item_searched))
        html_content = requests.get(self.__searched_url).text
        self.soup = BeautifulSoup(html_content, 'lxml')

    @property
    def searched_url(self):
        return self.__searched_url