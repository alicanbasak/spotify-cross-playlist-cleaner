from typing import Dict, List
from spotify_client import SpotifyClient

class PlaylistCleaner:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client

    def remove_duplicates(self, duplicates: Dict[str, List[Dict]], keep_playlist_id: str):
        """Remove duplicate tracks from playlists except the one to keep"""
        for track_id, locations in duplicates.items():
            for location in locations:
                playlist_name = location['playlist_name']
                playlist_id = location['playlist_id']
                
                if playlist_id != keep_playlist_id:
                    print(f"Removing track from playlist: {playlist_name}")
                    self.spotify_client.remove_tracks_from_playlist(playlist_id, [{'uri': f'spotify:track:{track_id}'}])