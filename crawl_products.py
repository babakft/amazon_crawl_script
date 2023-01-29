import requests
from bs4 import BeautifulSoup
from config import BASE_LINK_AMAZON, HEADER, PRODUCT_ATTR, STORAGE_TYPE
from parser import SearchParser
from storage import FileStorage, MongoStorage
from abc import ABC, abstractmethod


class CrawlBase(ABC):

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, headers=HEADER).content
        except requests.HTTPError as error:
            print("tha amazon reject the request")

        return response

    @abstractmethod
    def start(self, storing=True):
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
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == "mongo":
            return MongoStorage()
        else:
            return FileStorage()

    def start(self, storing=True):
        page = self.page_number
        print(f"start crawling for {self.search_text} page: {page}")

        search_result = self.get(self.link.format(self.search_text, page))
        soup = BeautifulSoup(search_result, "lxml")

        each_product = soup.find_all("div", attrs={"class": PRODUCT_ATTR["section"]})

        for product in each_product:
            result = self.parser.parse(product)

            print(result['title'])

            if storing:
                self.store(result)

        return result

    def store(self, data):
        self.storage.store(data, self.search_text, self.page_number)


if __name__ == "__main__":
    search = CrawlSearch("ps4", "20")
    search.start()
