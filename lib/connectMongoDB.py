#
##########################################
from pymongo import MongoClient

class MongoDBConnection:
    #def __init__(self, *args, **kwargs):
    #    return super().__init__(*args, **kwargs)

    def connect_mongo(arg, *args):  #連線資料庫
        
        mongo_host=arg
        mongo_db=args[0]
        mongo_collection=args[1]
        #print(arg,args[0],args[1])
        mongo_username=args[2]
        mongo_password=args[3]

        uri_mongo = "mongodb://{}:{}@{}:27017" 

        client = MongoClient(uri_mongo.format(mongo_username,mongo_password,mongo_host))
        db = client[mongo_db]
        collection = db[mongo_collection]
        print(collection)

        return collection