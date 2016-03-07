import tweepy

consumer_key, consumer_secret = [line.rstrip('\n') for line in open('twitterKeys.txt')]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
api = tweepy.API(auth)

#print api.trends_available()
print api.trends_place(1)

