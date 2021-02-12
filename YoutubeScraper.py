import random
import os
import googleapiclient.discovery
import TweetMaker
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "DEVELOPER_KEY"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

def CookPostYT(content_url):
    video_id = content_url.split("/")[-1]
    image_url = "https://img.youtube.com/vi/{}/0.jpg".format(video_id)
    request = youtube.commentThreads().list(part="snippet,replies", videoId=video_id)
    try:
        response = request.execute()
        if response["items"]:
            chosencomment = response["items"][random.randint(0, len(response["items"])-1)]['snippet']['topLevelComment']['snippet']['textOriginal']
        else:
            chosencomment = ""
        text = chosencomment + "\n" + content_url
        TweetMaker.MakeTweet(image_url, text)
    except:
        print("UNABLE TO COOK YOUTUBE VIDEO")

