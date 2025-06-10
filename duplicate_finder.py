from typing import List, Dict, Tuple, Optional
from spotify_client import SpotifyClient

class DuplicateFinder:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client

    def find_cross_playlist_duplicates(
        self,
        playlists: List[Tuple[str, str]],
        artists: Optional[List[str]] = None,
        albums: Optional[List[str]] = None,
        years: Optional[List[int]] = None,
    ) -> Dict[str, List[Dict[str, str]]]:
        """Find duplicate tracks across multiple playlists with optional filtering"""
        track_locations = {}
        
        for playlist_name, playlist_id in playlists:
            print(f"Checking playlist: {playlist_name}")
            tracks = self.spotify_client.get_playlist_tracks(playlist_id)
            
            for track in tracks:
                track_info = track.get('track')
                if not track_info or not track_info.get('id'):
                    # Skip entries without track details or an ID
                    continue

                # Filtering by artists, albums or years if provided
                if artists:
                    track_artists = [a.get('name', '') for a in track_info.get('artists', [])]
                    if not any(a in artists for a in track_artists):
                        continue
                if albums:
                    album_name = track_info.get('album', {}).get('name')
                    if album_name not in albums:
                        continue
                if years:
                    release = track_info.get('album', {}).get('release_date', '')
                    year = release.split('-')[0] if release else ''
                    if not year or int(year) not in years:
                        continue

                track_id = track_info['id']
                track_name = track_info.get('name', '')
                artist_names = ', '.join(
                    artist.get('name', '') for artist in track_info.get('artists', [])
                )
                
                if track_id not in track_locations:
                    track_locations[track_id] = []
                
                track_locations[track_id].append({
                    'playlist_name': playlist_name,
                    'playlist_id': playlist_id,
                    'track_name': track_name,
                    'artists': artist_names,
                })
        
        # Filter out tracks that are not duplicates
        duplicates = {track_id: locs for track_id, locs in track_locations.items() if len(locs) > 1}
        
        return duplicates

    @staticmethod
    def get_duplicate_stats(duplicates: Dict[str, List[Dict[str, str]]]) -> Dict[str, int]:
        """Return how many duplicates appear in each playlist"""
        stats: Dict[str, int] = {}
        for locations in duplicates.values():
            for loc in locations:
                pid = loc['playlist_id']
                stats[pid] = stats.get(pid, 0) + 1
        return stats
