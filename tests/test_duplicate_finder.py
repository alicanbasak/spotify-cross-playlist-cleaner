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

    def test_find_cross_playlist_duplicates_with_missing_id(self):
        playlists = [('Playlist 1', '1')]
        # Track missing an ID and a None track
        self.mock_spotify_client.get_playlist_tracks.return_value = [
            {'track': {'id': None, 'name': 'Song 1', 'artists': [{'name': 'Artist 1'}]}},
            {'track': None}
        ]

        duplicates = self.duplicate_finder.find_cross_playlist_duplicates(playlists)

        self.assertEqual(duplicates, {})

if __name__ == '__main__':
    unittest.main() 
