import pymongo.errors
from pymongo import MongoClient


class MongoDatabase:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.client = MongoClient()
        self.database = self.client['crawler']

        try:
            self.client.list_database_names()
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Can't connect to mongodb database ,"
                  "make sure mongodb is running in localhost ")
            exit()
