import json
import utils
import requests
import multiprocessing
import random
import re
import argparse


parser = argparse.ArgumentParser(description='Netease lyrics spider')
parser.add_argument('--src', default=str, required=True, help='song list waiting to be grabbed')
parser.add_argument('--dst', default=str, required=True, help='where to store result')
parser.add_argument('--proxy', default=False, type=bool, help='Use proxy or not')
args = parser.parse_args()


service_url = "127.0.0.1:3000"
song_list = utils.get_song_list(fname=args.src)

proxy_list = []
if args.proxy:
    proxy_list = utils.get_proxy_list(fname="./configs/proxy_list.json")

def worker_try(song_id):
    try:
        worker(song_id)
    except BaseException:
        return 
    return

def worker(song_id):
    request_lyric_url = "http://%s/lyric?id=%s" % (service_url, song_id)
    request_title_url = "http://%s/search?keywords=%s" % (service_url, song_id)
    if proxy_list != []:
        proxy = random.choice(proxy_list)
        request_lyric_url += "&proxy=%s" % proxy
        request_title_url += "&proxy=%s" % proxy

    # request api
    # TODO: use try ... expect ...
    try:
        lyric_data = requests.get(request_lyric_url).text
        title_data = requests.get(request_title_url).text
    except requests.ConnectionError:
        return 
    # print(data)

    # decode json
    lyric_data = json.loads(lyric_data)
    title_data = json.loads(title_data)


    if lyric_data.get("lrc", None) is None:
        return

    lyric = lyric_data["lrc"]["lyric"]

    # filter out timestamp in lyric
    lyric = re.sub(r"\[.*\]", "", lyric)

    if title_data["result"]["songs"] == []:
        return
    
    title = title_data["result"]["songs"][0]["name"]
    title = re.sub("[/*?:<>|\"\\\\]", "", title)

    # write file
    with open(args.dst + "/%s_%s.txt" % (song_id, title), "w") as f:
        f.write(lyric)


def main():
    # multiporcessing
    with multiprocessing.Pool(8) as p:
        p.map(worker_try, song_list)


if __name__ == "__main__":
    main()
