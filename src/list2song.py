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


# class Netease_song:
#     def __init__(self):
#         self.file2save = f'netease--ancient-song.json'
#         self.file4list = 'netease-ancient.json'

#         self.songs = []
#         self.browser = self._init_drive()

#     def _init_drive(self):
#         opt = webdriver.chrome.options.Options()
#         opt.headless = True
#         return webdriver.Chrome(ChromeDriverManager().install(), options=opt)

#     def login(self, cookie = 'cookie.json'):
#         """To GET more songs!
#         """
#         with open(cookie, 'r') as f:
#             cookies = json.load(f)
#         url = 'https://music.163.com/'
#         self.browser.get(url)
#         self.browser.delete_all_cookies()
#         for i in cookies:
#             i.pop('sameSite')
#             self.browser.add_cookie(i)
#         self.browser.get(url)

#     def get_song(self, url):
#         """return songs ids and names from the playlist url

#         Args:
#             url (str)

#         Returns:
#             list[str]: ids   of the songs
#             list[str]: names of the songs
#         """
#         self.browser.get(url)
#         self.browser.switch_to.frame('g_iframe')
#         html = self.browser.page_source
#         html_elem = etree.HTML(html)
#         songs_id = html_elem.xpath(r"//tbody/tr/td[2]/div/div/div/span/a/@href")
#         songs_id = [song[9:] for song in songs_id]

#         songs_name = html_elem.xpath(r"//tbody/tr/td[2]/div/div/div/span/a/b/@title")
#         return songs_id, songs_name

#     def get_candidate_list(self):
#         with open(self.file4list, 'r') as f:
#             lists = json.load(f)
#         return [playlist['list_url']
#                 for playlist in lists]

#     def crawl(self):
#         """main function
#         """
#         candidate_list = self.get_candidate_list()
#         songs_id = set()
#         songs_name = []
#         bar = tqdm(candidate_list)
#         for url in bar:
#             ids, names = self.get_song(url)
#             songs_id.update(ids)
#             bar.set_description(f"Now {len(songs_id)}")
#         total_data = {
#             "songlist" : list(songs_id),
#         }
#         with open(self.file2save, 'w') as f:
#             json.dump(total_data, f, ensure_ascii=False, indent=4)


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
