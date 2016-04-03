import tweepy
from google.appengine.ext import db

class Location(db.Model):
    hashtag = db.StringProperty(required=True)
    location = db.StringProperty(required=True)

consumer_key, consumer_secret = [line.rstrip('\n') for line in open('twitterKeys.txt')]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
api = tweepy.API(auth)

#1 for global geolocation
global_tendencies = api.trends_place(1)
tendencies = []

for trend in global_tendencies[0]["trends"]:
    tendencies.append(trend["name"])

#print tendencies

print tendencies[0]

for tweet in tweepy.Cursor(api.search, q=(tendencies[0])).items():
    if tweet.coordinates != None:
        print ""
        print tweet
        print tweet.coordinates
        location = Location(hashtag=tendencies[0], location=tweet.coordinates)
        location.put()
