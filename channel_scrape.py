# -*- coding: utf-8 -*-

# Importing the dependencies
from apiclient.discovery import build


# channel class consists of functions to retrieve data about a youtube channel
class channel():
    """
    This module scrapes a YouTube channel for playlists associated with it.
    """

    def __init__(self, api_key, channelId):
        self.channelId = channelId
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlists = []
        self.nextPageToken = ''

    def scrape(self):
        """
        scrape function starts scraping a channel for its playlists,
        checks for multiple pages, and returns a list of playlistId 
        for all the playlist of the channel.
        """

        request = self.youtube.playlists().list(
            part="id,snippet",
            channelId=self.channelId,
            maxResults=50)
        response = request.execute()
        items = response['items']
        for item in items:
            self.playlists.append(item['id'])

        if 'nextPageToken' in response:
            self.nextPageToken = response['nextPageToken']

        while self.nextPageToken:
            request = self.youtube.playlists().list(part="id,snippet", channelId=self.channelId,
                                                maxResults=50, pageToken=self.nextPageToken)
            response = request.execute()
            for item in items:
                self.playlists.append(item['id'])

            if 'nextPageToken' in response:
                self.nextPageToken = response['nextPageToken']
            else:
                self.nextPageToken = ''

        return self.playlists
