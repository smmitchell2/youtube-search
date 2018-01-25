#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import datetime
from rfc3339 import rfc3339


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = 'API key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    type="video",
    part='id,snippet',
    order=options.order,
    maxResults=options.max_results,
    publishedBefore = options.published_before,
    publishedAfter = options.published_after
  ).execute()

  search_videos = []
  videoId = []
  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    search_videos.append(search_result["id"]["videoId"])
  videoId = ",".join(search_videos)
  
  video_response = youtube.videos().list(
    id=videoId,
    part='id,snippet,statistics'
  ).execute()
  
  #doesnt work because of videoId try to build a class
  for video_result in video_response.get("items",[]):
        videos.append("%s %s %s" % (video_result["id"],
                                video_result["snippet"]["title"],
                                video_result["statistics"]["viewCount"]))
  print 'Videos:\n', '\n'.join(videos), '\n'


if __name__ == '__main__':
  timestamp = time.time()
  print(time.asctime(time.localtime(timestamp - 86400)),time.asctime(time.localtime(timestamp)))
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='landslide')
  parser.add_argument('--order',help='Order',default='viewCount')
  parser.add_argument('--max-results', help='Max results', default=10)
  parser.add_argument('--published-before',help ='Published before',default=rfc3339(timestamp))
  parser.add_argument('--published-after',help ='Published after',default=rfc3339(timestamp - 86400))
  args = parser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)