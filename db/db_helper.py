import pymongo

DB_NAME = "crack_stat"


class DbHelper:
    @staticmethod
    def get_client():
        client = pymongo.MongoClient('localhost', 27017)
        return client

    def get_db(self, db_name):
        real_db = db_name + "_db"
        db = self.get_client()[real_db]
        return db

    def get_collection(self, c_name, db_name=DB_NAME):
        return self.get_db(db_name)[c_name]

    def get_all_collections(self, db_name=DB_NAME):
        return self.get_db(db_name).collection_names()

    def insert_one(self, c_name, data):
        self.get_collection(c_name).insert_one(data)
        print('insert ' + str(data['app_pkg_name']) + str(data['install_time']))

    def insert_many(self, c_name, data_set):
        self.get_collection(c_name).insert_many(data_set)

    def find_one(self, c_name, query=None, *args, **kwargs):
        return self.get_collection(c_name).find_one(filter=query, *args, **kwargs)

    def find(self, c_name, *args, **kwargs):
        return self.get_collection(c_name).find(*args, **kwargs)

    def update(self, c_name, data):
        self.get_collection(c_name).update(data)

    def remove(self, c_name, query=None):
        self.get_collection(c_name).remove(query)
