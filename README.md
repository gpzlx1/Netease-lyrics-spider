# Netease-lyrics-spider
Usage:

1. `git clone --recurse-submodules https://github.com/gpzlx1/Netease-lyrics-spider.git`

2. `cd Netease-lyrics-spider && PROJECT_ROOT=$(pwd)`

3. `cd $PROJECT_ROOT/modules/NeteaseCloudMusicApi`

4. `npm install && node app.js`

5. `cd $PROJECT_ROOT/configs` and edit your song list and proxy list.

6. `python3 src/get_lyric.py --src song_list.json --dst target_dir`.

    For example,

    ```shell
    python3 src/get_lyric.py --src configs/ballad-songs.json --dst data
    ```

    You also can use `--proxy true` to use Proxy.

7. Data is saved at `$PROJECT_ROOT/data`
