#https://ssl.reddit.com/prefs/apps/
import random
import requests
import praw
import TweetMaker
reddit = praw.Reddit(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', password='PASSWORD', user_agent='Project KALEIDONITE', username='USERNAME')

def CookPostRD(content, includePostUrl):
    cell = content.split()
    posturl = requests.get(cell[0]).url
    image_url = requests.get(cell[1]).url
    try:
        submission = reddit.submission(url=posturl)
        commentroulette = []
        submission.comments.replace_more(limit=None)
        for top_level_comment in submission.comments:
            commentroulette.append(top_level_comment.body)
        if len(commentroulette) > 1:
            chosencomment = commentroulette[random.randint(1, len(commentroulette)-1)]
        else:
            chosencomment = ""
        if includePostUrl:
            text = "{}\n{}\n".format(chosencomment, posturl)
            for tag in cell[2:]:
                text += "{} ".format(tag)
            TweetMaker.MakeTweet(image_url, text)
        else:
            text = "{}\n".format(chosencomment)
            for tag in cell[2:]:
                text += "{} ".format(tag)
            TweetMaker.MakeTweet(image_url, text)
    except:
        print("UNABLE TO COOK SUBREDDIT POST")

