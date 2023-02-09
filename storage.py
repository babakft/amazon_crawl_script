import csv
import json
import time
from abc import ABC, abstractmethod
from databases import MongoDatabase, RedisDatabase
import os
from config import PROJECT_CONFIG
from Image_downloader import ImageDownloader


class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, search_text, page_number):
        pass

    @abstractmethod
    def build_file_path(self, search_text, page_number):
        pass

    @staticmethod
    def check_and_download_image(path, data):
        if PROJECT_CONFIG["DOWNLOAD_IMAGE"] is True:
            ImageDownloader().download_and_save_to_disk(path, data)


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()

    def build_file_path(self, search_text, page_number):
        'this file path just saves image'
        file_path = f"result/result_{search_text}_{page_number}/"
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def store(self, data, search_text, page_number):
        collection = getattr(self.mongo.database, f"result_{search_text}_{page_number}")

        if collection.find_one({"title": data["title"]}) is not None:
            return

        self.check_and_download_image(self.build_file_path(search_text, page_number), data)

        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)


class RedisStorage(StorageAbstract):

    def __init__(self):
        self.redis = RedisDatabase()
        self.connection = getattr(self.redis, 'client', None)

    def build_file_path(self, search_text, page_number):
        pass

    def store(self, data, search_text, page_number):

        redis_set_key = f"result_{search_text}_{page_number}"

        if self.connection.exists(redis_set_key):
            for value in self.connection.lrange(redis_set_key, 0, -1):
                value = json.loads(bytes.decode(value))
                if value['title'] == data['title']:
                    return
        self.connection.rpush(redis_set_key, json.dumps(data))


class FileStorage(StorageAbstract):

    def build_file_path(self, search_text, page_number, unique_attr):
        """If we have to download the picture of the product we put information and image in one file for each product
                    But if we don't have to download images we store
                    All product information in one file"""

        if PROJECT_CONFIG["DOWNLOAD_IMAGE"] is True:
            file_path = f"result/result_{search_text}_{page_number}/{unique_attr}"
        else:
            file_path = f"result/result_{search_text}_{page_number}"
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def store(self, data, search_text, page_number):
        unique_attr = data['details']['product_information'].get(" ASIN ", data['title'].split(" ")[0])
        directory = self.build_file_path(search_text, page_number, unique_attr)

        try:
            self.check_and_download_image(directory, data)

            with open(f"{directory}/{unique_attr}.json", 'x') as file:
                file.write(json.dumps(data))
        except FileExistsError:
            pass


class CsvStorage(StorageAbstract):

    def build_file_path(self, search_text, page_number, unique_attr):
        """If we have to download the picture of the product we put information and image in one file for each product
            But if we don't have to download images we store
            All product information in one file"""

        if PROJECT_CONFIG["DOWNLOAD_IMAGE"] is True:
            file_path = f"result/result_{search_text}_{page_number}/{unique_attr}"
        else:
            file_path = f"result/result_{search_text}_{page_number}"
        os.makedirs(file_path, exist_ok=True)

        return file_path

    @staticmethod
    def synchronizing_data_for_storing(data):
        header = dict()

        for main_header in data:
            if main_header != "details":
                header[main_header] = data[main_header]

        for detail_attr in data["details"]:
            for detail_header in data["details"][detail_attr]:
                header[detail_header.strip()] = data["details"][detail_attr][detail_header].strip()
        return header

    def store(self, data, search_text, page_number):
        unique_attr = data['details']['product_information'].get(" ASIN ", data['title'].split(" ")[0])
        directory = self.build_file_path(search_text, page_number, unique_attr)

        try:
            self.check_and_download_image(directory, data)

            with open(f"{directory}/{unique_attr}.csv", 'x') as file:
                csv_writer = csv.writer(file)
                synchronized_data = self.synchronizing_data_for_storing(data)

                header = synchronized_data.keys()
                csv_writer.writerow(header)

                values = synchronized_data.values()
                csv_writer.writerow(values)

        except FileExistsError:
            pass
