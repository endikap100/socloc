import tweepy
import mysql.connector

cnx = mysql.connector.connect(user='root', password='soclocapi',
                              host='127.0.0.1',
                              database='socloc')
print "conect"
cursor = cnx.cursor()
consumer_key, consumer_secret = [line.rstrip('\n') for line in open('twitterKeys.txt')]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret,"http://soclocapi.appspot.com/callback")
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
        print tweet.coordinates.coordinates[0] + ","+tweet.coordinates.coordinates[1]
        #location = Location(hashtag=tendencies[0], location=tweet.coordinates)
        #location.put()
        add_location = ("INSERT INTO location(hashtag, location)VALUES (%s, %s)")
        data_location = (tendencies[0], tweet.coordinates.coordinates[0] + ","+tweet.coordinates.coordinates[1])

        # Insert new employee
        cursor.execute(add_location, data_location)
        emp_no = cursor.lastrowid
        cnx.commit()

cnx.close()
cnx.close()
