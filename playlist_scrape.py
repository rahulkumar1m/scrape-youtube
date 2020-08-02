# Importing the dependencies
import pandas as pd
from apiclient.discovery import build


# playlist class consisting of all the functions involved in extracting data on videos in a playlist
class playlist():
    # Each scrape needs api_key and playlist_id from the user
    def __init__(self, api_key, playlist_id):
        self.api_key = api_key
        self.playlist_id = playlist_id

        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.title = []
        self.channelId = []
        self.channelTitle = []
        self.categoryId = []
        self.videoId = []
        self.viewCount = []
        self.likeCount = []
        self.dislikeCount = []
        self.commentCount = []
        self.favoriteCount = []
        self.category = []
        self.tags = []
        self.videos = []
        self.nextPageToken = ''

    def scrape(self):
        """
        `scrape` method starts scraping list of all the videos in a playlist and store it in `items` list.
        It then calls `pageScrape` function by passing items to it which scrape `statistics` and `snippets`.
        If there is more than one page of playlist, it calls `nextPage` to scrape videos from there too.
        This method doesn't accept any paramets except for `self`.
        It returns a `pandas.DataFrame` object containing all the desired data about all the videos in the playlist.
        """
        res = self.youtube.playlistitems().list(playlistId=self.playlist_id,
                                                part='snippet,id', maxResults=50).execute()

        items = res['items']

        self.pageScrape(items)

        if 'nextPageToken' in res:
            self.nextPageToken = res['nextPageToken']

        while self.nextPageToken:
            self.nextPage()

        youtube_dict = {'tags': self.tags, 'channelId': self.channelId, 'channelTitle': self.channelTitle,
                        'categoryId': self.categoryId, 'title': self.title, 'videoId': self.videoId,
                        'viewCount': self.viewCount, 'likeCount': self.likeCount, 'dislikeCount': self.dislikeCount,
                        'commentCount': self.commentCount, 'favoriteCount': self.favoriteCount}
        return pd.DataFrame(youtube_dict)

    def nextPage(self):
        """
        `nextPage` scrapes the list of videos on present page and checks if next pages exist 
        and store the `nextPageToken` to a variable for next use. 
        It doesn't accept any parameter and doesn't return anything.
        """
        page = self.youtube.playlistitems().list(playlistId=self.playlist_id, part='snippet,id',
                                                 maxResults=50, pageToken=self.nextPageToken).execute()

        items = page['items']
        self.pageScrape(items)

        if 'nextPageToken' in page:
            self.nextPageToken = page['nextPageToken']
        else:
            self.nextPageToken = ''

    def pageScrape(self, items):
        """
        `pageScrape` method accepts `items` list as parameter containing the videos whose data needs to be scraped.
        It scrapes the `statistics and `snippets` of a video and stores them in desired variables as declared in __init__.
        """
        statss = []
        for data in items:
            # Finding the Id of given video and finding it's statistics in the code below
            a = data['snippet']['resourceId']['videoId']
            stats = self.youtube.videos().list(
                part='statistics,snippet',
                id=a).execute()
            statss.append(stats)

        for count in range(len(items)):
            # if a given video is private it's count items variable is empty therfore length zero so we skip that video
            if(len(statss[count]['items']) != 0):

                self.title.append(items[count]['snippet']['title'])
                self.videoId.append(
                    items[count]['snippet']['resourceId']['videoId'])

                stats = statss[count]

                self.channelId.append(
                    stats['items'][0]['snippet']['channelId'])
                self.channelTitle.append(
                    stats['items'][0]['snippet']['channelTitle'])
                self.categoryId.append(
                    stats['items'][0]['snippet']['categoryId'])
                self.favoriteCount.append(
                    stats['items'][0]['statistics']['favoriteCount'])
                self.viewCount.append(
                    stats['items'][0]['statistics']['viewCount'])

                try:
                    self.likeCount.append(
                        stats['items'][0]['statistics']['likeCount'])
                except:
                    self.likeCount.append("Not available")

                try:
                    self.dislikeCount.append(
                        stats['items'][0]['statistics']['dislikeCount'])
                except:
                    self.dislikeCount.append("Not available")

                if 'commentCount' in stats['items'][0]['statistics'].keys():
                    self.commentCount.append(
                        stats['items'][0]['statistics']['commentCount'])
                else:
                    self.commentCount.append(0)

                if 'tags' in stats['items'][0]['snippet'].keys():
                    self.tags.append(stats['items'][0]['snippet']['tags'])
                else:
                    self.tags.append("No Tags")
