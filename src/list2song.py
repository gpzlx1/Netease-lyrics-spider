"""
Given a song list id, crawl all the song inside it
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
from tqdm import tqdm
import multiprocessing
import json
import time
import random
import requests

class Netease_song:
    def __init__(self,
                 label,
                 service=None):
        self.service = service or "127.0.0.1:3000"
        self.file4list = f"{label}-list.json"
        self.label = label
        self.songs = []


    def get_candidate_list(self):
        with open(self.file4list, 'r') as f:
            lists = json.load(f)
        return [
            playlist['list_url'].split("?id=")[1] 
            for playlist in lists 
            if int(playlist['play_count']) > 100000
        ]

    def get_song_id(self, list_id):
        access = f"http://{self.service}/playlist/detail?id={list_id}"
        try:
            data = json.loads(requests.get(access).text)
        except requests.ConnectionError:
            return
        playlist = data.get('playlist', None)
        if not playlist:
            return
        trackIds = playlist['trackIds']
        ids = [str(trackid['id']) for trackid in trackIds]
        # self.songs.extend(ids)
        print(f"Complete {len(ids)}\r", end='')
        return ids

    def run(self, core=8):
        lists = self.get_candidate_list()
        print(f"Search {len(lists)} playlist for {self.label}")
        with multiprocessing.Pool(core) as pool:
            results = pool.map(self.get_song_id, lists)
        for result in results:
            self.songs.extend(result)  
        self.songs = list(set(self.songs))
        self.songs = sorted(self.songs)
        
        print()
        print(f"total {len(self.songs)}")
        data = {"song_list" : self.songs}
        with open(f"{self.label}-songs.json", 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    crawl = Netease_song("rock")
    # crawl.login()
    crawl.run()
