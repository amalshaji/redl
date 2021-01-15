# redl - A Reddit video downloader(with audio)


### ⚠️ Requires `ffmpeg` installed


Redl scrapes the reddit post json and retrives both audio and video URLs. Once these files are downloaded, it uses `ffmpeg` to join them. 

### Installation

```bash
pip install redl --user
```

### Usage

```bash
redl https://www.reddit.com/r/Damnthatsinteresting/comments/kwrbde/making_a_grapefruit_dessert/
```

