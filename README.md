# Netease-lyrics-spider
Usage:

0. `git clone --recurse-submodules https://github.com/gpzlx1/Netease-lyrics-spider.git`

1. `cd Netease-lyrics-spider && PROJECT_ROOT=$(pwd)`

2. `cd $PROJECT_ROOT/modules/NeteaseCloudMusicApi`

3. `npm install && node app.js`

4. `cd $PROJECT_ROOT/configs` and edit your song list and proxy list.

5. `cd $PROJECT_ROOT/src`

6. `python get_lyric.py`

7. Data is saved at `$PROJECT_ROOT/data`
