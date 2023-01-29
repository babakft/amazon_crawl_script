import json
from abc import ABC, abstractmethod
from databases import MongoDatabase
import os
from config import DOWNLOAD_IMAGE
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
        if DOWNLOAD_IMAGE is True:
            ImageDownloader().download_and_save_to_disk(path, data)


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()

    def build_file_path(self, search_text, page_number):
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


class FileStorage(StorageAbstract):

    def build_file_path(self, search_text, page_number, unique_attr):
        if DOWNLOAD_IMAGE is True:
            file_path = f"result/result_{search_text}_{page_number}/{unique_attr}"
        else:
            file_path = f"result/result_{search_text}_{page_number}"
        os.makedirs(file_path, exist_ok=True)

        return file_path

    def store(self, data, search_text, page_number):
        unique_attr = data['details']['product_information'].get(" ASIN ", data['title'])
        directory = self.build_file_path(search_text, page_number, unique_attr)

        try:
            self.check_and_download_image(directory, data)

            with open(f"{directory}/{unique_attr}.json", 'x') as file:
                file.write(json.dumps(data))
        except FileExistsError as error:
            pass
