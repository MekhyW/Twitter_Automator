#https://console.developers.google.com/apis/dashboard?authuser=1&folder=&organizationId=&project=project-kaleidon-1578631259772
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import YoutubeScraper
import RedditScraper
import TweetMaker
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/spreadsheets'])
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
spreadsheets = service.spreadsheets()
result = spreadsheets.values().get(spreadsheetId='1CS4n-tSPtM_3gM1L6tVWwZdMoPttXgnEpsrQP5zwmYo', range='A1:B50').execute()
values = result.get('values', [])
spreadsheets.values().clear(spreadsheetId='1CS4n-tSPtM_3gM1L6tVWwZdMoPttXgnEpsrQP5zwmYo', range='A1:B50').execute()


def WatchColumns():
    result = spreadsheets.values().get(spreadsheetId='1CS4n-tSPtM_3gM1L6tVWwZdMoPttXgnEpsrQP5zwmYo', range='A1:B50').execute()
    values = result.get('values', [])
    if values:
        print(values)
        for row in range(0, len(values)):
            if values[row] and TweetMaker.remainingtweets > 0:
                if values[row][0]:
                    YoutubeScraper.CookPostYT(values[row][0])
                    spreadsheets.values().clear(spreadsheetId='1CS4n-tSPtM_3gM1L6tVWwZdMoPttXgnEpsrQP5zwmYo', range='A{}'.format(row+1)).execute()
        for row in range(0, len(values)):
            if values[row] and TweetMaker.remainingtweets > 0:
                if len(values[row]) >= 2:
                    if row+1 in (1, 4):
                        RedditScraper.CookPostRD(values[row][1], True)
                    else:
                        RedditScraper.CookPostRD(values[row][1], False)
                    spreadsheets.values().clear(spreadsheetId='1CS4n-tSPtM_3gM1L6tVWwZdMoPttXgnEpsrQP5zwmYo', range='B{}'.format(row+1)).execute()