import requests
from bs4 import BeautifulSoup
from config import BASE_LINK_AMAZON, project_config, HEADER
from parser import SearchParser
from storage import FileStorage, MongoStorage, CsvStorage
from abc import ABC, abstractmethod

PRODUCT_ATTR = {"section": "s-card-container s-overflow-hidden aok-relative"
                           " puis-include-content-margin puis s-latency-cf-section s-card-border"}


class CrawlBase(ABC):

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, headers=HEADER).content
        except requests.HTTPError or requests.ConnectionError:
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

        if project_config["STORING"] is True:
            self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if project_config["STORAGE_TYPE"] == "mongodb":
            return MongoStorage()
        elif project_config["STORAGE_TYPE"] == "csv":
            return CsvStorage()
        else:
            return FileStorage()

    def start(self):
        page = self.page_number
        print(f"start crawling for {self.search_text} page: {page} \n")

        search_result = self.get(self.link.format(self.search_text, page))

        """Separating the products that are shown in search result"""
        soup = BeautifulSoup(search_result, "lxml")
        each_product = soup.find_all("div", attrs={"class": PRODUCT_ATTR["section"]})
        for product in each_product:

            result = self.parser.parse(product)

            if project_config["STORING"]:
                self.store(result)
                print(f"{result['title']}\n")
            else:
                print(f"{result}\n")

    def store(self, data):
        self.storage.store(data, self.search_text, self.page_number)
