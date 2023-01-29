import json

import requests
from bs4 import BeautifulSoup
from config import BASE_LINK_AMAZON, HEADER, PRODUCT_ATTR, STORAGE_TYPE
from parser import SearchParser
from storage import FileStorage, MongoStorage


def get(link):
    try:
        return requests.get(link, headers=HEADER).content
    except requests.HTTPError as error:
        print(error)


class CrawlSearch:

    def __init__(self, search_text, page_number):
        self.search_text = search_text
        self.link = BASE_LINK_AMAZON
        self.parser = SearchParser()
        self.page_number = page_number
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == "mongo":
            print("x")
            return MongoStorage()
        else:
            print("y")
            return FileStorage()

    def start(self, storing=True):
        page = self.page_number
        crawl = True
        while crawl:

            if page == "20":
                break
            print(page)

            search_result = get(self.link.format(self.search_text, page))
            soup = BeautifulSoup(search_result, "lxml")

            each_product = soup.find_all("div", attrs={"class": PRODUCT_ATTR["section"]})
            crawl = bool(len(each_product) != 0)

            for product in each_product:
                result = self.parser.parse(product)
                if storing:
                    print(self.storage)
                    self.storage.store(result)

            page = str(int(page) + 1)

        return result


if __name__ == "__main__":
    search = CrawlSearch("ps4", "19")
    print(search.start())
