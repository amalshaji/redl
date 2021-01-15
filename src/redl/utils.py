import os
import sys
import uuid
import requests
import subprocess
import urllib.request
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    """Generate a custom tqdm progress bar

    Args:
        tqdm ([type]): Inherit tqdm class
    """

    def update_to(self, b: int = 1, bsize: int = 1024, tsize: int = None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download(url: str, output_path: str):
    """Download the given url

    Args:
        url (str): Link to download file
        output_path (str): Location to save the file to
    """
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1) as d:
        urllib.request.urlretrieve(
            url,
            filename=output_path,
            reporthook=d.update_to,
        )


def merge_audio_video(video: str, audio: str):
    """Nothing fancy here. Just call ffmpeg using subprocess

    Args:
        video (str): video file name
        audio (str): audio file name
    """

    target = f"{generate_random_target()}.mp4"

    # ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4
    subprocess.call(
        f"ffmpeg -i {video} -i {audio} -c:v copy -c:a aac {target}",
        shell=True,
    )

    # perform cleanup
    os.remove("video.mp4")
    os.remove("audio.mp4")

    print(f"Video file written to {target}")


def get_video_url(post_url: str) -> str:
    """Get the original video URL from
    the post.json file

    Args:
        post_url (str): URL to the post containing the video

    Returns:
        str: URL pointing to the actual media
    """
    data = requests.get(post_url).json()

    if isinstance(data, dict):
        print(data["message"])
        sys.exit(0)

    # url = data[0]["data"]["children"][0]["data"]["crosspost_parent_list"][0][
    #     "secure_media"
    # ]["reddit_video"]["fallback_url"]
    url: str = None

    try:
        url = data[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"][
            "fallback_url"
        ]
    except KeyError:
        print("Cannot get URL from post")
        sys.exit(0)

    return url


def generate_random_target() -> str:
    """Generate a random target file name

    Returns:
        str: A random string of length 6
    """
    return str(uuid.uuid4())[:6]


def check_exec() -> bool:
    """Check if ffmpeg exists on PATH

    Returns:
        bool: True for exists
    """
    from shutil import which

    return which("ffmpeg") is not None