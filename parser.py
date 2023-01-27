import requests
from bs4 import BeautifulSoup

from config import PRODUCT_ATTR, HEADER


def get(link):
    try:
        return requests.get(link, headers=HEADER).content
    except requests.HTTPError as error:
        print(error)


class SearchParser:

    @staticmethod
    def parse(section):

        product = {"title": None, "url": None, "image_url": None,
                   "price": None, "rate": None, "details": None}

        title = section.find("span", attrs={"class": PRODUCT_ATTR['title']})
        url = section.find("a", attrs={"class": PRODUCT_ATTR['url']})
        img_url = section.find("img", attrs={"class": PRODUCT_ATTR['img']})
        price = section.find("span", attrs={"aria-hidden": PRODUCT_ATTR['price']})
        rate = section.find("span", attrs={"class": PRODUCT_ATTR['rate']})

        if title is not None:
            product['title'] = title.text

        if url is not None:
            product['url'] = "https://www.amazon.com/" + url.get("href")
            product['details'] = SearchParser.__get_product_details(product['url'])

        if img_url is not None:
            product['image_url'] = img_url.get("src")

        if rate is not None:
            product['rate'] = rate.text

        if price is not None:
            __price = ""
            for price_part in price:
                __price += price_part.text

            product['price'] = __price

        return product

    @staticmethod
    def __get_product_details(product_link):

        soup = BeautifulSoup(get(product_link), "lxml")
        find_product_information = soup.find_all("table", attrs={"class": "a-keyvalue prodDetTable"})

        product_details = dict()
        for product in find_product_information:
            for i in product.find_all("tr"):
                product_details[i.find("th").text] = i.find("td").text.replace("\n", "").strip().replace("\u200e", "")
        return product_details
