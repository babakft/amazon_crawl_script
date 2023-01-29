import json
from abc import ABC, abstractmethod
from databases import MongoDatabase


class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data):
        pass


class MongoStorage(StorageAbstract):

    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data):
        collection = getattr(self.mongo.database, "result")

        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)


class FileStorage(StorageAbstract):
    def store(self, data):
        unique_attr = data['details']['product_information'].get(" ASIN ", data['title'])
        with open(f"result/{unique_attr}.json", 'w') as file:
            file.write(json.dumps(data))
        return
