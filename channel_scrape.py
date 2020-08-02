# -*- coding: utf-8 -*-

# Importing the dependencies
import pandas as pd
from apiclient.discovery import build


# channel class consists of functions to retrieve data about a youtube channel
class channel():

    def __init__(self, api_key, channelId):
        self.channelId = channelId
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlists = []
        self.nextPageToken = ''

    def scrape(self):
        request = self.youtube.playlists().list(
            part="id,snippet",
            channelId=self.channelId,
            maxResults=50)
        response = request.execute()
        items = response['items']
        self.pageScrape(items)

        if 'nextPageToken' in response:
            self.nextPageToken = response['nextPageToken']

        while self.nextPageToken:
            nextPage(self.nextPageToken)

        return self.playlists

    def nextPage(self):
        request = self.youtube.playlists().list(part="id,snippet", channelId=self.channelId,
                                                maxResults=50, pageToken=self.nextPageToken)
        response = request.execute()
        self.pageScrape(response['items'])

        if 'nextPageToken' in response:
            self.nextPageToken = response['nextPageToken']
        else:
            self.nextPageToken = ''

    def pageScrape(self, items):
        for item in items:
            self.playlists.append(item['id'])
