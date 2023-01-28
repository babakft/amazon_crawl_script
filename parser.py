from itertools import product

import requests
from bs4 import BeautifulSoup

from config import PRODUCT_ATTR, HEADER


def get(link):
    try:
        return requests.get(link, headers=HEADER).content
    except requests.HTTPError as error:
        print(error)


class SearchParser:

    def __init__(self):
        self.search_page = None
        self.detail_page = DetailParser()

    @property
    def title_tag(self):
        title = self.search_page.find("span", attrs={"class": PRODUCT_ATTR['title']})
        if title is not None:
            return title.text

    @property
    def url_tag(self):
        url = self.search_page.find("a", attrs={"class": PRODUCT_ATTR['url']})
        if url is not None:
            return "https://www.amazon.com/" + url.get("href")


    @property
    def img_url_tag(self):
        img_url = self.search_page.find("img", attrs={"class": PRODUCT_ATTR['img']})
        if img_url is not None:
            return img_url.get("src")

    @property
    def price_tag(self):
        price = self.search_page.find("span", attrs={"aria-hidden": PRODUCT_ATTR['price']})
        if price is not None:
            __price = ""
            for price_part in price:
                __price += price_part.text

            return __price

    @property
    def rate_tag(self):
        rate = self.search_page.find("span", attrs={"class": PRODUCT_ATTR['rate']})
        if rate is not None:
            return rate.text

    def parse(self, section):

        self.search_page = section

        product = {"title": self.title_tag, "url": self.url_tag, "image_url": self.img_url_tag,
                   "price": self.price_tag, "rate": self.rate_tag, "details": None}

        if product['url']:
            product["details"] = self.detail_page.parse(product['url'])

        return product


class DetailParser:
    def __init__(self):
        self.detail_page = None

    @property
    def product_information(self):
        find_product_information = self.detail_page.find_all("table", attrs={"class": "a-keyvalue prodDetTable"})

        product_information = dict()
        for information_table in find_product_information:

            for column in information_table.find_all("tr"):

                product_information[column.find("th").text] = \
                    column.find("td").text.replace("\n", "").strip().replace("\u200e", "")

        return product_information

    def parse(self, product_link):

        self.detail_page = BeautifulSoup(get(product_link), "lxml")

        product_details = {"product_information": self.product_information}

        return product_details
