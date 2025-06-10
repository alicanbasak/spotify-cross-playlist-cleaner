import unittest
from unittest.mock import MagicMock, patch

from main import interactive_flow
from spotify_client import SpotifyClient
from duplicate_finder import DuplicateFinder
from playlist_cleaner import PlaylistCleaner

class TestInteractiveFlow(unittest.TestCase):
    def test_invalid_input_does_not_crash(self):
        spotify_client = MagicMock(spec=SpotifyClient)
        duplicate_finder = MagicMock(spec=DuplicateFinder)
        playlist_cleaner = MagicMock(spec=PlaylistCleaner)

        # Prepare mocks
        spotify_client.get_user_playlists.return_value = [('Playlist 1', '1')]
        duplicate_finder.find_cross_playlist_duplicates.return_value = {
            'track1': [
                {
                    'playlist_name': 'Playlist 1',
                    'playlist_id': '1',
                    'track_name': 'Song 1',
                    'artists': 'Artist'
                }
            ]
        }

        with patch('builtins.input', return_value='abc'), patch('builtins.print') as mock_print:
            interactive_flow(spotify_client, duplicate_finder, playlist_cleaner)
            mock_print.assert_any_call("\nPlease enter a valid number.")
        playlist_cleaner.remove_duplicates.assert_not_called()

if __name__ == '__main__':
    unittest.main()
