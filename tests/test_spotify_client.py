import unittest
from unittest.mock import patch, MagicMock
from spotify_client import SpotifyClient
from config import SpotifyConfig

class TestSpotifyClient(unittest.TestCase):
    @patch('spotipy.Spotify')
    def test_get_user_playlists(self, mock_spotify):
        # Create a mock Spotify instance
        spotify_instance = MagicMock()
        mock_spotify.return_value = spotify_instance

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

if __name__ == '__main__':
    unittest.main() 
