import pymongo as pymongo


class DatabaseInsert:
    client = None
    db = None
    collection = None

    def init(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["your_database_name"]
        self.collection = self.db["your_collection_name"]

    def insert_docs(self, docs):
        self.collection.insert_many(docs)

    def __del__(self):
        self.client.close()
