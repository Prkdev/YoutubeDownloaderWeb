import os
import shutil
import tempfile
import streamlit as st
from yt_dlp import YoutubeDL

st.title("YouTube Playlist Downloader")

playlist_url = st.text_input("Playlist URL")

cookie_file = st.file_uploader("Upload cookies.txt (optional)", type=["txt"])

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

if st.button("Download Playlist"):
    if playlist_url:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'nocheckcertificate': True
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
