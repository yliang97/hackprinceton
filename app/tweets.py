from app import app

from flask import url_for, request, json
from flask import render_template


import tweepy
import keys

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

consumer_key = keys.key
consumer_secret = keys.secret
access_token = keys.token
access_token_secret = keys.tsecret


def twitter (username):
    #return "Top 12 tweets from" + username

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
    #    print (tweet.text) 
    tweetData = []

    person = username
    new_tweets = api.user_timeline(screen_name = person, count = 200)
    tweetData.extend(new_tweets)
    oldest = tweetData[-1].id - 1
    while len(new_tweets) > 0:
    # ("getting tweets before %s" % (oldest))

        new_tweets = api.user_timeline(screen_name = person, count = 200, max_id = oldest)

        tweetData.extend(new_tweets)

        oldest = tweetData[-1].id - 1

        # ("...%s tweets downloaded so far" % (len(tweetData)))

        dataQueue = Q.PriorityQueue()

    for tweet1 in tweetData:
        dataQueue.put((-tweet1.favorite_count, tweet1.text))


    numTweets = dataQueue.qsize()
    # ("Total number of tweets: " + (str)(numTweets))
    json_result = {}
    if (numTweets < 12):

        for i in range (numTweets):

            #takes the top most favorited
            storeData = dataQueue.get(True)
            #print (storeData.find(""))
            #turns the tuple data type into a string
            storeData = (str)(storeData)
            #finds the index of the end of the number of favorites
            endInt = (int) (storeData.find(","))
            #substrings from the - to the end of the int to give the integer of number of favorites
            numFavs = storeData[2: endInt]
            #substrings from 3 after the end of the number of favorites (remove shit in the middle) to the end of the relevant tweet string
            tweetScoop = storeData[endInt + 3: len(storeData) - 2]

            #print("Favorites: " + (str)(numFavs))
            #print ("Tweet: " + tweetScoop + "\n")
            json_result[i + 1] = (str)(numFavs) + " favorites: " + (str)(tweetScoop)
    else:
        for i in range(12):
            storeData = dataQueue.get(True)
            #print (storeData.find(""))
            storeData = (str)(storeData)
            endInt = (int) (storeData.find(","))
            numFavs = storeData[2: endInt]
            tweetScoop = storeData[endInt + 3: len(storeData) - 2]
            #print("Favorites: " + (str)(numFavs))
            #print ("Tweet: " + tweetScoop + "\n")
            json_result[i + 1] = (str)(numFavs) + " favorites: " + (str)(tweetScoop)
    return  json.jsonify(json_result)



@app.route('/user')
def helloworld():
    return twitter(request.args['username'])


# @app.route('/')
@app.route('/')
def begin():
    return render_template('twitter.html')
