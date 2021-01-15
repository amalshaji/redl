import sys
from redl import utils


def main():
    # get the post URL from the user
    if len(sys.argv) < 2:
        print("Enter post URL as argument")
        return

    url = sys.argv[1]

    # remove the trailing `/` and add .json
    if url[-1] == "/":
        url = url[:-1]
    url = f"{url}.json"

    video_url: str = utils.get_video_url(url)

    # generate audio link be replacing the DASH_{video_size} by "audio".
    # Thus DASH_640 becomes DASH_audio

    # make simple splits to seperate parts of the URL
    left = video_url.split("DASH")[0]
    right = video_url.split("?")[-1]
    middle = "DASH_audio.mp4"

    audio_url = f"{left}{middle}?{right}"

    # download both audio and video

    # video_url = "https://v.redd.it/wtxu0waz27b61/DASH_360.mp4?source=fallback"
    # audio_url = "https://v.redd.it/wtxu0waz27b61/DASH_audio.mp4?source=fallback"

    print("downloading video")
    utils.download(video_url, "video.mp4")

    try:
        print("downloading audio")
        utils.download(audio_url, "audio.mp4")
    except Exception:
        print("no audio available for the video, file saved to video.mp4")
        sys.exit(0)

    if not utils.check_exec():
        print("ffmpeg is not on PATH, please install or add it to PATH")
        sys.exit(0)

    # merge audio and video to a single file
    utils.merge_audio_video("video.mp4", "audio.mp4")


if __name__ == "__main__":
    main()