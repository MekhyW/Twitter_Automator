#https://developer.twitter.com/en/apps
import time
import tweepy
import requests
import os
import GoogleSheetsReader
auth = tweepy.OAuthHandler('HANDLER', 'HANDLER')
auth.set_access_token('TOKEN', 'TOKEN')
api = tweepy.API(auth)
timewindow = 0
minutewindow = 0
remainingtweets = 25
remainingFollows = 4
remainingUnfollows = 4
follow_target = None
public_tweets = []

def FeedRetweet():
    global timewindow
    global minutewindow
    global remainingtweets
    global remainingFollows
    global remainingUnfollows
    global follow_target
    global public_tweets
    if time.clock() - timewindow > 900 or remainingtweets==25:
        try:
            GoogleSheetsReader.WatchColumns()
            remainingtweets = 25
            remainingFollows = 4
            remainingUnfollows = 4
            timewindow = time.clock()
            for user in tweepy.Cursor(api.followers, screen_name=follow_target).items(10):
                if remainingFollows > 0 and not user.following and user.friends_count >= user.followers_count:
                    api.create_friendship(screen_name=user.screen_name)
                    print("FOLLOWED " + user.screen_name)
                    remainingFollows -= 1
                elif remainingUnfollows > 0 and user.following and not user.followed_by:
                    api.destroy_friendship(screen_name=user.screen_name)
                    print("UNFOLLOWED " + user.screen_name)
                    remainingUnfollows -= 1
            public_tweets = api.home_timeline()
        except:
            pass
    if (time.clock() - minutewindow > 300 and remainingtweets > 0 and time.clock() - timewindow > 60) or remainingtweets==25:
        if public_tweets:
            try:
                minutewindow = time.clock()
                remainingtweets -= 1
                already_retweeted = False
                for tweet in public_tweets:
                    author = tweet.author._json.get('id')
                    if not already_retweeted and author != 1180517923619819521 and not hasattr(tweet, 'retweeted_status') and not tweet.in_reply_to_status_id:
                        api.create_favorite(tweet.id)
                        tweet.retweet()
                        print(tweet.author.friends_count)
                        already_retweeted = True
                    follow_target = tweet.author.screen_name
            except:
                pass
    
def MakeTweet(image_url, text):
    global remainingtweets
    remainingtweets -= 1
    request = requests.get(image_url, stream=True)
    if request.status_code == 200:
        with open('temp.jpg', 'wb') as image:
            for chunk in request:
                image.write(chunk)
        api.update_with_media('temp.jpg', status=text)
        os.remove('temp.jpg')
    else:
        print("UNABLE TO DOWNLOAD IMAGE")
    print(image_url, text)