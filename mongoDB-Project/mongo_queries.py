"""
Name   : Srinivas ka Ritu Raj
Course : CMPS 5303 - Advance Database Management System
Project: MongoDb Project
"""
"""
1.Find all restaurants with zip code X or Y -Using 89117 and 89122 answer = 1083
"""
##db.yelp.business.find({$or: [{"full_address":{$regex: '89117'}},{"full_address":{$regex: '89122'}}]}).pretty()

"""
2.Find all restaurants in city "Las Vegas
"""
##db.yelp.business.find({"full_address":{$regex: 'Las Vegas'}}).pretty()

"""
3.Find the restaurants within 5 miles of lat , lon
"""
##db.yelp.business.find({loc: {$geoWithin: { $center: [ [ -80.839186,35.226504] , .004 ] }}}).pretty()

"""
4.Find all the reviews for restaurant X
"""
##db.yelp.review.find({"business_id" : "hB3kH0NgM5LkEWMnMMDnHw"}).count();

"""
5.Find all the reviews for restaurant X that are 5 stars.
"""
##db.yelp.review.find({"business_id" : "P1fJb2WQ1mXoiudj8UE44w", "stars":5}).count();

"""
6.Find all the users that have been 'yelping' for over 5 years.
"""
##db.yelp.user.find({"yelping_since" : { $lte : "2011-11"}});

"""
7.Find the business that has the tip with the most likes.
"""
##db.yelp.tip.find().sort({likes:-1}).limit(1);

"""
8.Find the average review_count for users.
"""
##db.yelp.user.aggregate([{$group: {"_id":null, avgReviewCountForUsers: {$avg:"$review_count"} } }]);

"""
9.Find all the users that are considered elite.
"""
##db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1});

"""
10.Find the longest elite user.
"""
##db.yelp.user.aggregate( [{ $unwind : "$elite" },{ $group : { _id : "$_id", maxEliteYears : { $sum : 1 }} },{ $sort : { maxEliteYears : -1 } },{ $limit : 13 }] );

"""
11.Of elite users, whats the average number of years someone is elite.
"""
##db.yelp.user.aggregate([{ $unwind : "$elite" },{ $group : { _id : "$_id", maxElite : { $sum : 1 }}},{$group: {"_id":null, avgEliteUsers: {$avg:"$maxElite"} } }])
