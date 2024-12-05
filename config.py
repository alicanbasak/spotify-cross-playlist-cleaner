import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class SpotifyConfig:
    CLIENT_ID: str = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET: str = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI: str = os.getenv('SPOTIFY_REDIRECT_URI')
    SCOPE: str = "playlist-modify-public playlist-modify-private playlist-read-private user-library-read user-read-private"
