from typing import Dict, List, Tuple
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SpotifyConfig

class SpotifyClient:
    def __init__(self, config: SpotifyConfig):
        try:
            print("Spotify authentication process started...")
            auth_manager = SpotifyOAuth(
                client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                redirect_uri=config.REDIRECT_URI,
                scope=config.SCOPE,
                open_browser=True  # To open the browser automatically
            )
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test the connection
            user = self.sp.current_user()
            if user is None:
                raise Exception("Could not get user information")
            
            self.user_id = user['id']
            print(f"Connection successful! User: {self.user_id}")
            
        except Exception as e:
            print(f"Error during Spotify connection: {str(e)}")
            raise
    
    def get_user_playlists(self):
        """Get all playlists of the authenticated user"""
        try:
            print("Connecting to Spotify API...")
            current_user = self.sp.current_user()
            if current_user is None:
                print("Could not get user information. Authentication error.")
                return []
            
            print(f"User: {current_user['id']}")
            
            playlists = []
            offset = 0
            limit = 50  # Spotify API recommended limit
            
            while True:
                try:
                    # Get playlists with pagination
                    results = self.sp.current_user_playlists(limit=limit, offset=offset)
                    
                    if not results or 'items' not in results:
                        break
                    
                    # Break if no more items
                    if len(results['items']) == 0:
                        break
                    
                    for item in results['items']:
                        try:
                            # Only get playlists owned by the user
                            if (item.get('owner', {}).get('id') == self.user_id and 
                                'name' in item and 'id' in item):
                                playlist = (item['name'], item['id'])
                                playlists.append(playlist)
                                print(f"Found playlist: {item['name']}")
                        except Exception as item_error:
                            print(f"Error processing playlist: {str(item_error)}")
                            continue
                    
                    # Move to next page
                    offset += limit
                    
                    # Break if all playlists are fetched
                    if len(results['items']) < limit:
                        break
                    
                except Exception as page_error:
                    print(f"Error fetching page: {str(page_error)}")
                    break
            
            if not playlists:
                print("No playlists found.")
                return []
            
            print(f"Found total of {len(playlists)} playlists.")
            return playlists
        
        except Exception as e:
            print(f"Error during playlist fetching: {str(e)}")
            print(f"Error details: {type(e).__name__}")
            if hasattr(e, 'response'):
                print(f"API response: {e.response}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Get all tracks of a specific playlist"""
        tracks = []
        results = self.sp.playlist_items(playlist_id)
        
        while results:
            tracks.extend(results['items'])
            results = self.sp.next(results) if results['next'] else None
        
        return tracks

    def remove_tracks_from_playlist(self, playlist_id: str, tracks_to_remove: List[Dict]):
        """Remove tracks from a playlist"""
        for i in range(0, len(tracks_to_remove), 100):
            batch = tracks_to_remove[i:i + 100]
            self.sp.playlist_remove_specific_occurrences_of_items(playlist_id, batch)
