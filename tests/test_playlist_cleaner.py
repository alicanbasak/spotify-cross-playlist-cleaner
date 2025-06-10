import unittest
from unittest.mock import MagicMock
from playlist_cleaner import PlaylistCleaner
from spotify_client import SpotifyClient

class TestPlaylistCleaner(unittest.TestCase):
    def setUp(self):
        self.mock_spotify_client = MagicMock(spec=SpotifyClient)
        self.playlist_cleaner = PlaylistCleaner(self.mock_spotify_client)

    def test_remove_duplicates(self):
        duplicates = {
            'track1': [
                {'playlist_name': 'Playlist 1', 'playlist_id': '1'},
                {'playlist_name': 'Playlist 2', 'playlist_id': '2'}
            ]
        }
        
        self.playlist_cleaner.remove_duplicates(duplicates, '1')
        
        self.mock_spotify_client.remove_tracks_from_playlist.assert_called_once_with(
            '2', [{'uri': 'spotify:track:track1'}]
        )

if __name__ == '__main__':
    unittest.main() 
