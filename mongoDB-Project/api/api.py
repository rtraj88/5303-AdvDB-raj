```
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

import json
import urllib
import pql


import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)
db = client['advdb']
businessdb = db['yelp.business']
reviewdb = db['yelp.review']
userdb = db['yelp.user']
tipdb = db['yelp.tip']


parser = reqparse.RequestParser()

"""=================================================================================="""
"""=================================================================================="""
      #ROOT DIRECTORY
"""=================================================================================="""
@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list
"""=================================================================================="""
       # 1.RESTAURANTS WITH ZIP CODE
"""=================================================================================="""
@app.route("/zip/<args>", methods=['GET'])
def find_zips(args):
    args = myParseArgs(args)
    data = []
    zip = args['zips']
    zip1,zip2 = zip.split(',')
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = businessdb.find({'$or': [{"full_address":{'$regex':zip1}},{"full_address":{'$regex':zip2}}]},{"_id":0,"business_id":1,"name":1,"full_address":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = businessdb.find({'$or': [{"full_address":{'$regex':zip1}},{"full_address":{'$regex':zip2}}]},{"_id":0,"business_id":1,"name":1,"full_address":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = businessdb.find({'$or': [{"full_address":{'$regex':zip1}},{"full_address":{'$regex':zip2}}]},{"_id":0,"business_id":1,"name":1,"full_address":1}).limit(limit)
    else:
        result = businessdb.find({'$or': [{"full_address":{'$regex':zip1}},{"full_address":{'$regex':zip2}}]},{"_id":0,"business_id":1,"name":1,"full_address":1}).limit(10)
    for r in result:
       data.append(r)
    return {"data":data}
    
"""==============================================================================="""
         # 2.RESTAURANTS BY CITY
"""==============================================================================="""

@app.route("/city/<args>", methods=['GET'])
def city(args):

    args = myParseArgs(args)
    city = args['city']
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = businessdb.find({'full_address':{'$regex':city}},{'_id':0,'business_id':1,'name':1,'full_address':1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = businessdb.find({'full_address':{'$regex':city}},{'_id':0,'business_id':1,'name':1,'full_address':1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = businessdb.find({'full_address':{'$regex':city}},{'_id':0,'business_id':1,'name':1,'full_address':1}).limit(limit)
    else:
        result = businessdb.find({'full_address':{'$regex':city}},{'_id':0,'business_id':1,'name':1,'full_address':1}).limit(10) 
    for r in result:
        data.append(r)
    return {"data":data}
"""=================================================================================="""
        # 3.BUSINESS WITH IN 5 MILES RADIUS GEO LOCATION 
"""=================================================================================="""
@app.route("/closest/<args>", methods=['GET'])
def closest(args):
    args = myParseArgs(args)
    data = []
    lon = float(args['lon'])
    lat = float(args['lat'])
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = businessdb.find({"loc": {'$geoWithin': { '$center': [ [lon,lat] , 5 ] }}},{"_id":0,"business_id":1,"name":1,"full_address":1,"loc":1,"hours":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = businessdb.find({"loc": {'$geoWithin': { '$center': [ [lon,lat] , 5 ] }}},{"_id":0,"business_id":1,"name":1,"full_address":1,"loc":1,"hours":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = businessdb.find({"loc": {'$geoWithin': { '$center': [ [lon,lat] , 5 ] }}},{"_id":0,"business_id":1,"name":1,"full_address":1,"loc":1,"hours":1}).limit(limit)
    else:
        result = businessdb.find({"loc": {'$geoWithin': { '$center': [ [lon,lat] , 5 ] }}},{"_id":0,"business_id":1,"name":1,"full_address":1,"loc":1,"hours":1}).limit(10)
    for r in result:
        data.append(r)
    return {"data":data}

"""=================================================================================="""
        # 4.REVIEWS FOR RESTAURANT X
"""=================================================================================="""
@app.route("/reviews/<args>", methods=['GET'])
def reviews(args):
    args = myParseArgs(args)
    data = []
    bid = str(args['id'])
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = reviewdb.find({"business_id" :bid},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = reviewdb.find({"business_id" :bid},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = reviewdb.find({"business_id" :bid},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1}).limit(limit)
    else:
        result = reviewdb.find({"business_id" :bid},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1}).limit(10)
    for r in result:
        data.append(r)
    return {"data":data}

"""=================================================================================="""
        # 5.REVIEWS FOR RESTAURANT X THAT ARE 5 STARS
"""=================================================================================="""
@app.route("/stars/<args>", methods=['GET'])
def stars(args):
    args = myParseArgs(args)
    data = []
    bid = str(args['id'])
    num_stars = int(args['num_stars'])
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = reviewdb.find({"business_id" : bid, "stars":num_stars},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1,"stars":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = reviewdb.find({"business_id" : bid, "stars":num_stars},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1,"stars":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = reviewdb.find({"business_id" : bid, "stars":num_stars},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1,"stars":1}).limit(limit)
    else:
        result = reviewdb.find({"business_id" : bid, "stars":num_stars},{"_id":0,"business_id":1,"review_id":1,"user_id":1,"text":1,"stars":1}).limit(10)
    for r in result:
        data.append(r)
    return {"data":data}

"""=================================================================================="""
       # 6.USERS YELPING OVER 5 YEARS
"""=================================================================================="""
@app.route("/yelping/<args>", methods=['GET'])
def yelping(args):
    args = myParseArgs(args)
    data = []
    min_years = int(args['min_years'])
    d = 2016-min_years
    m = 12
    check = str(d)+"-"+str(m)
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = userdb.find({"yelping_since":{'$lte':check}},{"_id":0,"name":1,"user_id":1,"yelping_since":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = userdb.find({"yelping_since":{'$lte':check}},{"_id":0,"name":1,"user_id":1,"yelping_since":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = userdb.find({"yelping_since":{'$lte':check}},{"_id":0,"name":1,"user_id":1,"yelping_since":1}).limit(limit)
    else:
        result = userdb.find({"yelping_since":{'$lte':check}},{"_id":0,"name":1,"user_id":1,"yelping_since":1}).limit(10)
    for r in result:
        data.append(r)
    return {"data":data}

"""=================================================================================="""
         # 7.BUSINESS WITH MOST LIKES 
"""=================================================================================="""
@app.route("/most_likes/<args>", methods=['GET'])
def most_likes(args):
    args = myParseArgs(args)
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = tipdb.find({},{"_id":0}).sort("likes",pymongo.DESCENDING)[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = tipdb.find({},{"_id":0}).sort("likes",pymongo.DESCENDING).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = tipdb.find({},{"_id":0}).sort("likes",pymongo.DESCENDING).limit(limit)
    else:
        result = tipdb.find({},{"_id":0}).sort("likes",pymongo.DESCENDING).limit(10)
    for r in result:
        data.append(r)
    return {"data":data}

"""=================================================================================="""
        # 8. AVERAGE REVIEW COUNT FOR USERS
"""=================================================================================="""
@app.route("/review_count/", methods=['GET'])
def review_count():
    data = []
    result = userdb.aggregate([{'$group': {"_id":"null", "avgReviewCountForUsers": {'$avg':"$review_count"} } }])
    data.append(result)
    return {"data":data}

"""=================================================================================="""
         # 9.ELITE USERS
"""=================================================================================="""
@app.route("/elite/<args>", methods=['GET'])
def elite(args):
    args = myParseArgs(args)
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        start = int(args['start'])
        limit = int(args['limit'])
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})[start:limit].limit(limit)
    elif 'start' in args.keys():
        start = int(args['start'])
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).skip(start)
    elif 'limit' in args.keys():
        limit = int(args['limit'])
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(limit)
    else:
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(10)  

    for row in result:
        data.append(row)
    return {"data":data}

"""=================================================================================="""
         # 10.LONGEST ELITE USERS
"""=================================================================================="""
@app.route("/longest_elite/<args>", methods=['GET'])
def longest_elite(args):
    args = myParseArgs(args)
    data = []
    start = int(args['start'])
    limit = int(args['limit'])
    sorted = args['sorted']
    result = userdb.aggregate([{'$group':{'_id':0,'longestEliteYears':{'$max':{'$size':'$elite'}}}}])  
    return {"data":result}

"""=================================================================================="""
         # 11. AVERAGE ELITE USERS
"""=================================================================================="""
@app.route("/avg_elite/", methods=['GET'])
def avg_elite():
    data = []
    result = userdb.aggregate([{'$unwind':"$elite"},{'$group':{'_id':"$_id",'maxElite':{'$sum':1}}},{'$group':{"_id":0,'avgEliteUsers':{'$avg':"$maxElite"}}}])
    return {"data":result}

"""=================================================================================="""
       # USER
"""=================================================================================="""
@app.route("/user/<args>", methods=['GET'])
def user(args):

    args = myParseArgs(args)
    
    if 'skip' in args.keys():
        args['skip'] = int(args['skip'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    #.skip(1).limit(1)
    
    if 'skip' in args.keys() and 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip']).limit(args['limit'])
    elif 'skip' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip'])
    elif 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).limit(args['limit'])
    else:
        result = userdb.find({},{'_id':0}).limit(10)  

    for row in result:
        data.append(row)


    return {"data":data}


"""=================================================================================="""
        #SNAP TIME
"""=================================================================================="""
def snap_time(time,snap_val):
    time = int(time)
    m = time % snap_val
    if m < (snap_val // 2):
        time -= m
    else:
        time += (snap_val - m)
        
    if (time + 40) % 100 == 0:
        time += 40
        
    return int(time)

"""=================================================================================="""
         #PARSE ARGS
"""=================================================================================="""
def myParseArgs(pairs=None):
    """Parses a url for key value pairs. Not very RESTful.
    Splits on ":"'s first, then "=" signs.
    
    Args:
        pairs: string of key value pairs
        
    Example:
    
        curl -X GET http://cs.mwsu.edu:5000/images/
        
    Returns:
        json object with all images
    """
    
    if not pairs:
        return {}
    
    argsList = pairs.split(":")
    argsDict = {}

    for arg in argsList:
        key,val = arg.split("=")
        argsDict[key]=str(val)
        
    return argsDict
    

if __name__ == "__main__":
    app.run(debug=True,host='67.205.136.57',port=5000)
```
