import tweepy
import webapp2
from google.appengine.ext import db
import logging

class Location(db.Model):
    hashtag = db.StringProperty(required=True)
    location = db.StringProperty(required=True)

class Callback(webapp2.RequestHandler):
    def get(self):
        logging.debug("pasa")
        self.response.write("dcfvhyijpojcbv")

class LocationT(webapp2.RequestHandler):
    consumer_key, consumer_secret = [line.rstrip('\n') for line in open('twitterKeys.txt')]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token("471159702-nDvOvrkwvSdLQDCj2RZy94LUweMfXh1XhoSXuKyT", "bgL3Q2yYS6nAYGj7jzDqEmYd8mtZUT7kLBM2t0YlXHuJC")
    auth.secure = True
    api = tweepy.API(auth)
    #print api

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

app = webapp2.WSGIApplication([
    ('/update_twitter', LocationT),
    ('/callback',Callback)
], debug=True)