import pymongo

# Replace these values with your MongoDB connection details
host = "localhost"
port = 27017

# Create a MongoClient instance
client = pymongo.MongoClient(host, port)

# Access the database and collection
db_name = "mydatabase"
collection_name = "mycollection"
db = client[db_name]
collection = db[collection_name]

try:
    # Find all documents in the collection
    documents = collection.find()

    # Print each document
    for document in documents:
        print(document)
except Exception as e:
    print("An error occurred:", e)
