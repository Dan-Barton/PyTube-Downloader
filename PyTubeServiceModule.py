from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist

import os
import subprocess
import datetime

# TEST VIDEO AND PLAYLIST

# https://www.youtube.com/watch?v=FAyKDaXEAgc - 10 second video
# https://www.youtube.com/watch?v=FbPuqJcbBIs&list=PLvN4NeV0zrpYd77AaaN_u1PBzSAIFda1c - test (2 video playlist)

# Subprocess to update PyTube (acquire the most recent cypher key)
def update_pytube() -> None:
    try:
        subprocess.run(['pip', 'install', '--upgrade', 'pytube'], check=True)
    except subprocess.CalledProcessError:
        pass

# Return video title and length formatted as hh:mm:ss
def get_video_info(link: str) -> [str]:
    yt = YouTube(link)
    title = yt.title
    length = str(datetime.timedelta(seconds=yt.length))

    return title, length

# Return playlist title and length (number of videos) from link as string list
def get_playlist_info(link: str) -> [str]:
    playlist = Playlist(link)
    title = playlist.title
    length = playlist.length

    return title, length

# Return video/playlist thumbnail JPEG URL from link
def get_thumbnail_url(link: str) -> str:
    yt = YouTube(link)

    return yt.thumbnail_url

# Download video as mp4 in selected resolution to specified or default Downloads DIR
# Resolution serves as prefix to distinguish stream as a unique file, not to be overridden
def download_as_mp4(link: str, quality: str, target_directory=os.path.join(os.path.expanduser('~'), 'Downloads')) -> None:
    yt = YouTube(link)

    if quality == 'high':
        download_file = yt.streams.get_highest_resolution()
        res = yt.streams.get_highest_resolution().resolution
    elif quality == 'medium':
        download_file = yt.streams.filter(res='720p', mime_type='video/mp4', progressive=True).first()
        res = "720p"
    else:
        download_file = yt.streams.filter(res='360p', mime_type='video/mp4', progressive=True).first()
        res = "360p"

    download_file.download(output_path=target_directory, filename_prefix=f"({res}) ")

# Download video as mp3 to specified or default Downloads DIR
def download_as_mp3(link: str, target_directory=os.path.join(os.path.expanduser('~'), 'Downloads')) -> None:
    yt = YouTube(link)
    # Downloads audio only mp4
    audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()
    # Adds "mp3" prefix to distinguish file from mp4 downloads in path
    download_file = audio_stream.download(output_path=target_directory, filename_prefix="(mp3) ")

    # Edit file extension
    base, _ = os.path.splitext(download_file)
    new_file = base + '.mp3'

    # Extract audio from audio only mp4
    audio_clip = AudioFileClip(download_file)
    # Write audio to new mp3 file
    audio_clip.write_audiofile(new_file, codec='mp3')
    # Close process
    audio_clip.close()

    # Remove audio only mp4
    os.remove(download_file)

# Download videos in playlist as mp4's in specified resolution
def download_playlist_as_mp4(link: str, quality: str) -> None:
    playlist = Playlist(link)

    # Create new folder for playlist in Downloads if no such folder exists with file-type suffix
    target_directory = os.path.join(os.path.expanduser('~'), 'Downloads', f"{playlist.title} (mp4)")
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    # Download each video in playlist using video as mp4 method to specified DIR
    for video in playlist.videos:
        download_as_mp4(video.watch_url, quality, target_directory)

# Download videos in playlist as mp3's
# Same logic as playlist as mp4 method, additional file type conversion step required for every file
    # as in the video as mp3 method
def download_playlist_as_mp3(link: str) -> None:
    playlist = Playlist(link)

    target_directory = os.path.join(os.path.expanduser('~'), 'Downloads', f"{playlist.title} (mp3)")

    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    for video in playlist.videos:
        download_as_mp3(video.watch_url, target_directory)
