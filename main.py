from pytube import Playlist
import os
import subprocess
import json


def download_playlist_songs(playlist_url, ffmpeg_path):
    playlist = Playlist(playlist_url)

    download_folder = "downloads"

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for video in playlist.videos:
        file_name = (
            video.title.replace("|", "")
            .replace(":", "")
            .replace('"', "")
            .replace("/", "")
            .replace("\\", "")
            .replace("?", "")
            .replace("*", "")
        )
        stream = video.streams.get_audio_only()
        file_path = stream.download(
            output_path=download_folder, filename=f"{file_name}.mp4"
        )

        mp3_file_path = file_path.replace(".mp4", ".mp3")

        # subprocess.run komutunu ffmpeg'in tam yolu ile çağırıyoruz ve shell=True ekliyoruz
        subprocess.run([ffmpeg_path, "-i", file_path, mp3_file_path], shell=True)

        os.remove(file_path)

        print(f"Downloaded and converted: {file_name}")


# Playlist URL ve ffmpeg path from links.json
with open("links.json", "r") as file:
    links = json.load(file)

playlist_url = links["playlist_url"]
ffmpeg_path = links["ffmpeg_path"]

download_playlist_songs(playlist_url, ffmpeg_path)
