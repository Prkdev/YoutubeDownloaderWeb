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
3. Press **Download Playlist** to download all videos. After the download finishes a zip archive of the playlist is created and a **Download ZIP** button will appear allowing you to save it locally.

