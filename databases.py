from pymongo import MongoClient, errors
from redis import Redis, exceptions


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
        except errors.ServerSelectionTimeoutError:
            print("Can't connect to mongodb database ,"
                  "make sure mongodb is running in localhost ")
            exit()


class RedisDatabase:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.client = Redis()
        try:
            self.client.ping()
        except exceptions.ConnectionError:
            print("Can't connect to Redis,"
                  "make sure redis is running in localhost")
            exit()
