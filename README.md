# Youtube Playlist Downloader Web

This simple Streamlit app allows you to download every video from a YouTube playlist.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

## Usage

1. Enter a YouTube playlist URL.
2. (Optional) Upload a `cookies.txt` file if the playlist requires login.
3. Press **Download Playlist** to fetch all videos in the highest available quality. Video and audio are automatically merged into a single `mp4` file. The app shows how many videos will be downloaded, an estimated total length and a progress bar with the remaining time. After the download finishes a zip archive of the playlist is created and a **Download ZIP** button lets you save it locally.
