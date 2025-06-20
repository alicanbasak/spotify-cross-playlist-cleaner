from typing import Dict, List
from spotify_client import SpotifyClient

class PlaylistCleaner:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client

    def remove_duplicates(
        self, duplicates: Dict[str, List[Dict[str, str]]], keep_playlist_id: str
    ) -> Dict[str, int]:
        """Remove duplicate tracks from playlists except the one to keep.
        Returns a dict with number of removed tracks per playlist."""
        stats: Dict[str, int] = {}
        for track_id, locations in duplicates.items():
            for location in locations:
                playlist_name = location['playlist_name']
                playlist_id = location['playlist_id']

                if playlist_id != keep_playlist_id:
                    print(f"Removing track from playlist: {playlist_name}")
                    self.spotify_client.remove_tracks_from_playlist(
                        playlist_id, [f'spotify:track:{track_id}']
                    )
                    stats[playlist_id] = stats.get(playlist_id, 0) + 1
        return stats
