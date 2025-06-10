from typing import Dict, List, Optional
from spotify_client import SpotifyClient

class PlaylistCleaner:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client

    def remove_duplicates(
        self,
        duplicates: Dict[str, List[Dict[str, str]]],
        keep_playlist_id: str,
        exclude: Optional[List[str]] = None,
    ) -> None:
        """Remove duplicate tracks from playlists except the one to keep"""
        exclude_set = set(exclude or [])
        for track_id, locations in duplicates.items():
            for location in locations:
                playlist_name = location['playlist_name']
                playlist_id = location['playlist_id']

                if playlist_id == keep_playlist_id or playlist_id in exclude_set:
                    continue

                print(f"Removing track from playlist: {playlist_name}")
                self.spotify_client.remove_tracks_from_playlist(
                    playlist_id, [{'uri': f'spotify:track:{track_id}'}]
                )
