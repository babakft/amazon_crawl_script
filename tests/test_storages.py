import json
import os
import unittest
from databases import MongoDatabase, RedisDatabase, LazyLoader
from Image_downloader import ImageDownloader
from storage import FileStorage, MongoStorage, CsvStorage, RedisStorage
from config import PROJECT_CONFIG


class TestDataBase(unittest.TestCase):
    def setUp(self):
        with open("tests/product_instance.json", "r") as product_json:
            self.product_jason = json.load(product_json)

    def test_MongoDatabase(self):
        """ databases are singleton"""

        mongo = MongoDatabase()
        self.assertTrue(hasattr(mongo, 'client'))
        self.assertTrue(hasattr(mongo, 'database'))

    def test_RedisDatabase(self):
        redis = RedisDatabase()
        self.assertTrue(hasattr(redis, 'client'))

    def test_Image_downloader(self):
        if os.path.exists("tests/image_test.jpg"):
            os.remove("test/image_test.jpg")

        ImageDownloader().download_and_save_to_disk("tests/", self.product_jason)

    def test_FileStorage(self):
        filestorage = FileStorage()
        """test file storage while downloading image is disable"""
        file_path = filestorage.build_file_path("ps4", "1", "test_folder")
        self.assertEqual(file_path, "result/result_ps4_1")
        # os.remove(file_path)

        """test file storage while downloading image is enable"""
        PROJECT_CONFIG["DOWNLOAD_IMAGE"] = True
        file_path = filestorage.build_file_path("ps4", "1", "test_folder")

        self.assertEqual(file_path, "result/result_ps4_1/test_folder")
        PROJECT_CONFIG["DOWNLOAD_IMAGE"] = False

        filestorage.store(self.product_jason, "ps4", "1")

    def test_MongoStorage(self):
        mongo_storage = MongoStorage()

        """test mongo storage while downloading image is disable"""
        file_path = mongo_storage.build_file_path("ps4", "1")
        self.assertEqual(file_path, "result/result_ps4_1/")

        mongo_storage.store(self.product_jason, "ps4", "1")

    def test_RedisStorage(self):
        redis_storage = RedisStorage()

        """test redis storage while downloading image is disable"""
        file_path = redis_storage.build_file_path("ps4", "1")
        self.assertEqual(file_path, "result/result_ps4_1/")

        redis_storage.store(self.product_jason, "ps4", "1")

    def test_CscStorage(self):
        csv_storage = CsvStorage()

        """test file storage while downloading image is disable"""
        file_path = csv_storage.build_file_path("ps4", "1", "test_folder")
        self.assertEqual(file_path, "result/result_ps4_1")
        # os.remove(file_path)

        """test file storage while downloading image is enable"""
        PROJECT_CONFIG["DOWNLOAD_IMAGE"] = True
        file_path = csv_storage.build_file_path("ps4", "1", "test_folder")

        self.assertEqual(file_path, "result/result_ps4_1/test_folder")
        PROJECT_CONFIG["DOWNLOAD_IMAGE"] = False

        csv_storage.store(self.product_jason, "ps4", "1")

        synchronized_data = csv_storage.synchronizing_data_for_storing(self.product_jason)
        self.assertEqual(synchronized_data, {'title': 'PS5 Digital Edition- Horizon Forbidden West Bundle',
                                             'url': 'https://www.amazon.com//Digital-Horizon-Forbidden-Bundle-PlayStation-5/dp/B0B167VTXQ/ref=sr_1_4?keywords=ps5&qid=1676968415&sr=8-4',
                                             'image_url': 'https://m.media-amazon.com/images/I/71skn8zxlVL._AC_UY218_.jpg',
                                             'price': '$449.99', 'rate': '4.8 out of 5 stars', 'ASIN': 'B0B167VTXQ',
                                             'Release date': 'August 1, 2022',
                                             'Customer Reviews': '4.8 out of 5 stars        483 ratings    4.8 out of 5 stars',
                                             'Best Sellers Rank': '#2,282 in Video Games (See Top 100 in Video Games)  #264 in PlayStation 5 Consoles, Games & Accessories',
                                             'Pricing': 'The strikethrough price is the List Price. Savings represents a discount off the List Price.',
                                             'Package Dimensions': '20 x 18.4 x 8.6 inches; 13 Pounds',
                                             'Type of item': 'CD-ROM', 'Item model number': '1000032006',
                                             'Item Weight': '13 pounds', 'Manufacturer': 'PlayStation',
                                             'Country of Origin': 'China',
                                             'Batteries': '1 Lithium Ion batteries required. (included)',
                                             'Date First Available': 'August 1, 2022'}
                         )

    def tearDown(self):
        pass

    """ I dont have access to delete file that are in parent so please delete file that are created in this unittest"""
