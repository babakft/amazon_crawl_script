import unittest
from parser import SearchParser
from bs4 import BeautifulSoup
from crawl_products import CrawlSearch


class CrawlSearchTestCase(unittest.TestCase):
    def setUp(self):
        """I copy the ps4 page one result and put it in my website to test crawl"""

        self.normal_sample = CrawlSearch("ps4", "1", "https://firstbabakdeepcore.ir/amazon_pages/{}page{}.html")

    def test_constructor(self):
        """Test constructor for the value that they should have"""
        self.assertIsInstance(self.normal_sample, CrawlSearch)
        self.assertTrue(hasattr(self.normal_sample, "search_text"))
        self.assertTrue(hasattr(self.normal_sample, "page_number"))
        self.assertTrue(hasattr(self.normal_sample, "parser"))
        self.assertTrue(hasattr(self.normal_sample, "link"))
        self.assertTrue(hasattr(self.normal_sample, "storage"))

        self.normal_sample.start()

    def test_parser(self):
        """test the detail extractor by a section that is saved in section.txt"""
        with open("tests/section.txt", "r") as section:
            soup = BeautifulSoup(section, "lxml")
            self.normal_sample.parser.parse(soup)
            """delete the price to check if the code work for product without price in search text """
            soup.find("span", attrs={"aria-hidden": "true"}).string = ""
            self.normal_sample.parser.parse(soup)

