import os
import shutil
import tempfile
import time
import streamlit as st
from yt_dlp import YoutubeDL

st.title("YouTube Playlist Downloader")

playlist_url = st.text_input("Playlist URL")

cookie_file = st.file_uploader("Upload cookies.txt (optional)", type=["txt"])

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

if st.button("Download Playlist"):
    if playlist_url:
        progress_bar = st.progress(0)
        status = st.empty()

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'ffmpeg_location': shutil.which('ffmpeg') or 'ffmpeg',
            'postprocessors': [{
                'key': 'FFmpegMerger',
                'preferredcodec': 'mp4'
            }]
        }
        tmp_cookie_path = None
        if cookie_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.txt') as tmp:
                tmp.write(cookie_file.read())
                tmp_cookie_path = tmp.name
            ydl_opts['cookiefile'] = tmp_cookie_path

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            playlist_title = info.get('title', 'playlist')
            entries = [e for e in info.get('entries', []) if e]
            num_videos = len(entries)
            total_duration = sum(e.get('duration', 0) for e in entries)
            if num_videos == 0:
                st.error("No videos found in playlist.")
                st.stop()

            status.info(f"{num_videos} videos found. Estimated length: {total_duration//60}m{total_duration%60}s")

            downloaded = {'count': 0}
            start_time = time.time()

            def hook(d):
                if d.get('status') == 'finished':
                    downloaded['count'] += 1
                    elapsed = time.time() - start_time
                    estimated_total = (elapsed / downloaded['count']) * num_videos
                    remaining = max(0, estimated_total - elapsed)
                    progress_bar.progress(min(downloaded['count'] / num_videos, 1.0))
                    status.info(f"Downloaded {downloaded['count']}/{num_videos} - ~{int(remaining)}s remaining")

            ydl.add_progress_hook(hook)
            ydl.download([playlist_url])

        playlist_path = os.path.join(DOWNLOAD_DIR, playlist_title)
        zip_file = shutil.make_archive(playlist_path, 'zip', playlist_path)

        if tmp_cookie_path:
            os.remove(tmp_cookie_path)

        st.success("Download completed.")
        with open(zip_file, "rb") as f:
            st.download_button("Download ZIP", f, file_name=f"{playlist_title}.zip")
    else:
        st.error("Please provide a playlist URL.")
