import pymongo as pymongo


class DatabaseManager:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://williamwells:L1UMa5d0IP1zHtpa@existing-drones-databas.tw38p1z"
                                          ".mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["existing-drones"]
        self.collection = self.db["drones"]

    def insert_docs(self, docs):
        docs = standardize_units(docs)

        self.collection.insert_many(docs)

        print("Inserted documents")

    def update_docs(self, docs):
        pass

    def fetch_docs(self):
        return self.collection.find({})

    def __del__(self):
        self.client.close()


def standardize_units(docs):
    for drone in docs:
        for spec in drone:
            split_spec = strip_unit(drone[spec])
            drone[spec] = split_spec

    return docs


def strip_unit(string):
    new_string = string
    split = string.split(' ')

    if len(split) == 2:  # assuming that numbers always have two parts: value and unit
        first = split[0]
        second = split[1]

        for unit in ['hrs', 'hr', 'km/h', 'km', 'm', 'kg']:
            if second == unit:  # found measurement string
                first = first.replace(',', '')
                if first != '--':
                    new_string = float(first)
                else:
                    new_string = first
                break

    return new_string
