from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

class MongoConnection:
    def __init__(self, host='mongoDB', port=27017, username='apihrp', password='apihrpservice', db_name=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.client = None
        self.db = None

    def conect(self):
        try:
            self.client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                serverSelectionTimeoutMS=5000
            )
            # Prueba la conexión
            self.client.admin.command('ping')
            if self.db_name:
                self.db = self.client[self.db_name]
            print('Conexión a MongoDB exitosa')
            return True
        except ConnectionFailure as e:
            print(f'Error de conexión a MongoDB: {e}')
            return False

    def get_db(self):
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            print('Conexión a MongoDB cerrada')

    def insert_value(self, collection_name, data):
        """
        Insert a document into the specified collection.
        Returns the inserted id or None if it fails.
        """
        if self.db == None :
            print('No active database connection.')
            return None
        try:
            result = self.db[collection_name].insert_one(data)
            print(f'Document inserted with id: {result.inserted_id}')
            return result.inserted_id
        except Exception as e:
            print(f'Error inserting document: {e}')
            return None

    def get_values(self, collection_name, filter=None):
        """
        Get documents from the specified collection according to the filter (dict).
        If no filter is given, returns all documents.
        Converts ObjectId to string for JSON serialization.
        """
        if self.db == None:
            print('No active database connection.')
            return []
        try:
            if filter == None:
                filter = {}
                collection = self.db[collection_name]
                results = list(collection.find())
            else:
                collection = self.db[collection_name]
                results = list(collection.find(filter))
            # Convert ObjectId to string
            for doc in results:
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['_id'] = str(doc['_id'])
            # print(f'Obtained {len(results)} documents from {collection_name}')
            return 200,results[0]
        except Exception as e:
            print(f'Error getting documents: {e}')
            return 400, []
