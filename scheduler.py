from schedule import every, run_pending
import time
from config import SpotifyConfig
from spotify_client import SpotifyClient
from duplicate_finder import DuplicateFinder
from playlist_cleaner import PlaylistCleaner

config = SpotifyConfig()
spotify_client = SpotifyClient(config)
duplicate_finder = DuplicateFinder(spotify_client)
playlist_cleaner = PlaylistCleaner(spotify_client)

def cleanup_job(keep_playlist_id, frequency):
    playlists = spotify_client.get_user_playlists()
    duplicates = duplicate_finder.find_cross_playlist_duplicates(playlists)
    playlist_cleaner.remove_duplicates(duplicates, keep_playlist_id)
    print(f"Scheduled cleanup executed ({frequency})")


def start_scheduler(keep_playlist_id: str, frequency: str = "daily") -> None:
    if frequency == "daily":
        every().day.do(cleanup_job, keep_playlist_id, frequency)
    elif frequency == "weekly":
        every().week.do(cleanup_job, keep_playlist_id, frequency)
    else:
        raise ValueError("Frequency must be 'daily' or 'weekly'")

    print(f"Starting scheduled cleanup: {frequency}")
    while True:
        run_pending()
        time.sleep(1)
