import requests
from bs4 import BeautifulSoup
from config import BASE_LINK_AMAZON, PROJECT_CONFIG, HEADER
from parser import SearchParser
from storage import FileStorage, MongoStorage, CsvStorage, RedisStorage
from abc import ABC, abstractmethod

PRODUCT_ATTR = {"section": "s-card-container s-overflow-hidden aok-relative"
                           " puis-include-content-margin puis s-latency-cf-section s-card-border"}


class CrawlBase(ABC):

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, headers=HEADER).content
        except requests.HTTPError or requests.exceptions.ConnectionError:
            print("Amazon rejects the request for crawling")
            exit()
        except requests.exceptions.ProxyError:
            print("Please deactive your vpn or proxy ")
            exit()

        return response

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass


class CrawlSearch(CrawlBase):

    def __init__(self, search_text, page_number):
        self.search_text = search_text
        self.link = BASE_LINK_AMAZON
        self.parser = SearchParser()
        self.page_number = page_number

        if PROJECT_CONFIG["STORING"] is True:
            self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():

        DATA_STORAGE = {
            "mongodb": MongoStorage(),
            "csv": CsvStorage(),
            "file": FileStorage(),
            "redis": RedisStorage()
        }
        return DATA_STORAGE[PROJECT_CONFIG['STORAGE_TYPE']]

    def start(self):
        page = self.page_number
        print(f"start crawling for {self.search_text} page: {page} \n")

        search_result = self.get(self.link.format(self.search_text, page))

        """Separating the products that are shown in search result"""
        soup = BeautifulSoup(search_result, "lxml")
        each_product = soup.find_all("div", attrs={"class": PRODUCT_ATTR["section"]})
        for product in each_product:
            result = self.parser.parse(product)

            if PROJECT_CONFIG["STORING"]:
                self.store(result)
                print(f"{result['title']}\n")
            else:
                print(f"{result}\n")

    def store(self, data):
        self.storage.store(data, self.search_text, self.page_number)
