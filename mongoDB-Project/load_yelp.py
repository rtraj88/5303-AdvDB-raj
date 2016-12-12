import os
import json

from pymongo import MongoClient
from bson import Binary, Code

DATABASENAME = 'advdb'
TEST = False

client = MongoClient('localhost', 27017)
if not TEST:
    db = client[DATABASENAME]

# Inside your yelp data directory, rename your files accordingly:
files = ['business.json','checkin.json','review.json','tip.json','user.json']

# This function to add a proper 2D "loc [x,y]" object to the document
# Make sure you create a 2D index after this file runs !!!
# e.g. db.yelp.business.createIndex({"loc":"2d"})
def add_2D_location(json):
    if 'longitude' in json and 'latitude' in json:
        loc = [json['longitude'],json['latitude']]
        json['loc'] = loc
    return json

"""
Following loops through the file list creating collections of name:
    yelp.business
    yelp.checkin
    yelp.review
    yelp.tip
    yelp.user
"""
for file in files:
    name,ext  = file.split('.')
    collection_name = 'yelp.'+name
    print(collection_name)

    # Creates collection in mongo here: 
    if not TEST:
        collection = db[collection_name]

    # Deletes documents from collection every time it's run
    if not TEST:
        result = collection.delete_many({})

    # Open actual data file and read a line at a time
    f = open(file)
    for line in f:
        # read a line, convert to json, add 2D location
        line = add_2D_location(json.loads(line))

        # insert into collection
        if not TEST:
            collection.insert(line)
