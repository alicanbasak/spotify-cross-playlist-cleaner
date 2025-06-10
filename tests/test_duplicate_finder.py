import unittest
from unittest.mock import MagicMock
from duplicate_finder import DuplicateFinder
from spotify_client import SpotifyClient

class TestDuplicateFinder(unittest.TestCase):
    def setUp(self):
        self.mock_spotify_client = MagicMock(spec=SpotifyClient)
        self.duplicate_finder = DuplicateFinder(self.mock_spotify_client)

    def test_find_cross_playlist_duplicates(self):
        # Mock playlists and tracks
        playlists = [('Playlist 1', '1'), ('Playlist 2', '2')]
        self.mock_spotify_client.get_playlist_tracks.side_effect = [
            [{'track': {'id': 'track1', 'name': 'Song 1', 'artists': [{'name': 'Artist 1'}]}}],
            [{'track': {'id': 'track1', 'name': 'Song 1', 'artists': [{'name': 'Artist 1'}]}}]
        ]
        
        duplicates = self.duplicate_finder.find_cross_playlist_duplicates(playlists)
        
        self.assertIn('track1', duplicates)
        self.assertEqual(len(duplicates['track1']), 2)

if __name__ == '__main__':
    unittest.main() 
