import requests
from bs4 import BeautifulSoup
from config import BASE_LINK_AMAZON, HEADER, PRODUCT_ATTR
from parser import SearchParser


def get(link):
    try:
        return requests.get(link, headers=HEADER).content
    except requests.HTTPError as error:
        print(error)


class CrawlSearch:

    def __init__(self, search_text, link=BASE_LINK_AMAZON):
        self.search_text = search_text
        self.link = BASE_LINK_AMAZON
        self.parser = SearchParser()

    def start(self):
        product_list = list()
        page = "1"
        crawl = True
        while crawl:

            if page == 2:
                break
            print(page)

            search_result = get(self.link.format(self.search_text, page))
            soup = BeautifulSoup(search_result, "lxml")

            each_product = soup.find_all("div", attrs={"class": PRODUCT_ATTR["section"]})
            crawl = bool(len(each_product) != 0)

            for product in each_product:
                product_list.append(self.parser.parse(product))

            page = str(int(page) + 1)
        return product_list


if __name__ == "__main__":
    search = CrawlSearch("laptop")
    print(search.start())
