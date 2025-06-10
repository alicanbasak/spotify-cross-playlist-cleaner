import unittest
from unittest.mock import patch, MagicMock
from spotify_client import SpotifyClient
from config import SpotifyConfig

class TestSpotifyClient(unittest.TestCase):
    @patch('spotipy.oauth2.SpotifyOAuth')
    @patch('spotipy.Spotify')
    def test_get_user_playlists(self, mock_spotify, mock_spotify_oauth):
        # Create a mock Spotify instance
        spotify_instance = MagicMock()
        mock_spotify.return_value = spotify_instance

        # Create a mock SpotifyOAuth instance with required methods
        oauth_instance = MagicMock()
        oauth_instance.get_cached_token.return_value = {'access_token': 'token'}
        mock_spotify_oauth.return_value = oauth_instance

        # Mock the current_user method
        spotify_instance.current_user.return_value = {'id': 'test_user_id'}

        # Mock the current_user_playlists method
        spotify_instance.current_user_playlists.return_value = {
            'items': [
                {
                    'name': 'Playlist 1',
                    'id': '1',
                    'owner': {'id': 'test_user_id'}
                },
                {
                    'name': 'Playlist 2',
                    'id': '2',
                    'owner': {'id': 'test_user_id'}
                }
            ]
        }
        
        config = SpotifyConfig()
        client = SpotifyClient(config)
        # Override the user_id to match our mock
        client.user_id = 'test_user_id'
        
        playlists = client.get_user_playlists()
        
        # Verify the results
        self.assertEqual(len(playlists), 2)
        self.assertEqual(playlists[0][0], 'Playlist 1')
        self.assertEqual(playlists[1][0], 'Playlist 2')
        
        # Verify that the methods were called
        # current_user is called twice: once in __init__ and once in get_user_playlists
        self.assertEqual(spotify_instance.current_user.call_count, 2)
        spotify_instance.current_user_playlists.assert_called_once()

    @patch('spotipy.oauth2.SpotifyOAuth')
    @patch('spotipy.Spotify')
    def test_remove_tracks_from_playlist(self, mock_spotify, mock_spotify_oauth):
        spotify_instance = MagicMock()
        mock_spotify.return_value = spotify_instance

        oauth_instance = MagicMock()
        oauth_instance.get_cached_token.return_value = {'access_token': 'token'}
        mock_spotify_oauth.return_value = oauth_instance

        config = SpotifyConfig()
        client = SpotifyClient(config)

        client.remove_tracks_from_playlist('playlist', ['uri1', 'uri2'])

        spotify_instance.playlist_remove_all_occurrences_of_items.assert_called_once_with(
            'playlist', ['uri1', 'uri2']
        )

if __name__ == '__main__':
    unittest.main() 
