import httplib2
import os
import argparse
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.tools import argparser, run_flow
from urllib.parse import urlparse
from langdetect import detect

CLIENT_SECRETS_FILE = "client_secrets.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://developers.google.com/console

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(videoID):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message = MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("my-oauth2.json")
  credentials = storage.get()

  parser = argparse.ArgumentParser(parents=[tools.argparser])
  flags = parser.parse_args()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, flags)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, \
               developerKey='AIzaSyBHtGi8R0VXINpTKvuGGUolCTjJkiaYSko')

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  # with open("youtube-v3-discoverydocument.json", "r") as f:
  #   doc = f.read()
  #   return build(doc, http=credentials.authorize(httplib2.Http()))


# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
  ).execute()

  return results["items"]

def get_comments(youtube, parent_id):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  return results["items"]

def list_captions(youtube, video_id):
  results = youtube.captions().list(
    part="snippet",
    videoId=video_id
  ).execute()

  for item in results["items"]:
    id = item["id"]
    name = item["snippet"]["name"]
    language = item["snippet"]["language"]

  return results["items"]

def get_youtube_comments(link):
    o = urlparse(link)
    query = o.query.split('&')
    videoID = query[0].replace('v=', '')
    youtube = get_authenticated_service(videoID)

    # All the available methods are used in sequence just for the sake of an example.
    text = ''
    video_comment_threads = get_comment_threads(youtube, videoID)
    for thread in video_comment_threads:
        topComment = thread["snippet"]["topLevelComment"]

        cmt = topComment["snippet"]["textDisplay"] + '\n'
        if detect(cmt) == 'en':
            text += cmt

        parent_id = thread["id"]
        video_comments = get_comments(youtube, parent_id)

        for child_comments in video_comments:
            cmt = child_comments["snippet"]["textDisplay"] + '\n'
            if detect(cmt) == 'en':
                text += cmt

    return text