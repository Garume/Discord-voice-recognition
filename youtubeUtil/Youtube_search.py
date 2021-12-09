import json
from apiclient.discovery import build


class Youtube_Serch:
    def __init__(self):
        self.MAX_RESULT = 1
        self.API_KEY = self.read_key()
    
    def read_key(self):
        with open("util/env.json","r") as file:
            API = json.load(file)["youtube_api"]
        return API

    def youtube_search(self,KEY_WORD):
        youtube = build("youtube", "v3", developerKey=self.API_KEY)

        search_response = youtube.search().list(
        q=KEY_WORD,
        part="id,snippet",
        maxResults=self.MAX_RESULT
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(search_result["snippet"]["title"])
                videos.append("https://www.youtube.com/watch?v=%s" % search_result["id"]["videoId"])

        return videos