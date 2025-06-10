from typing import List, Dict, Tuple
from spotify_client import SpotifyClient

class DuplicateFinder:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client

    def find_cross_playlist_duplicates(
        self, playlists: List[Tuple[str, str]]
    ) -> Dict[str, List[Dict[str, str]]]:
        """Find duplicate tracks across multiple playlists"""
        track_locations = {}
        
        for playlist_name, playlist_id in playlists:
            print(f"Checking playlist: {playlist_name}")
            tracks = self.spotify_client.get_playlist_tracks(playlist_id)
            
            for track in tracks:
                track_info = track.get('track')
                if not track_info or not track_info.get('id'):
                    # Skip entries without track details or an ID
                    continue

                track_id = track_info['id']
                track_name = track_info.get('name', '')
                artists = ', '.join(
                    artist.get('name', '') for artist in track_info.get('artists', [])
                )
                
                if track_id not in track_locations:
                    track_locations[track_id] = []
                
                track_locations[track_id].append({
                    'playlist_name': playlist_name,
                    'playlist_id': playlist_id,
                    'track_name': track_name,
                    'artists': artists,
                })
        
        # Filter out tracks that are not duplicates
        duplicates = {track_id: locs for track_id, locs in track_locations.items() if len(locs) > 1}
        
        return duplicates
