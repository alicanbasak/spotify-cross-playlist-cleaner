import sys
import importlib
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


class TestWebService(unittest.TestCase):
    def setUp(self):
        # Patch SpotifyClient before importing web_service to avoid real network calls
        self.spotify_patcher = patch('spotify_client.SpotifyClient', autospec=True)
        MockClient = self.spotify_patcher.start()
        self.mock_spotify = MagicMock()
        MockClient.return_value = self.mock_spotify

        # Reload web_service so patched SpotifyClient is used
        if 'web_service' in sys.modules:
            self.ws = importlib.reload(sys.modules['web_service'])
        else:
            self.ws = importlib.import_module('web_service')

        self.client = TestClient(self.ws.app)

    def tearDown(self):
        self.spotify_patcher.stop()
        if 'web_service' in sys.modules:
            del sys.modules['web_service']

    def test_list_playlists(self):
        self.ws.spotify_client.get_user_playlists.return_value = [
            ('Playlist 1', '1'),
            ('Playlist 2', '2')
        ]

        response = self.client.get('/playlists')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{'name': 'Playlist 1', 'id': '1'}, {'name': 'Playlist 2', 'id': '2'}]
        )
        self.ws.spotify_client.get_user_playlists.assert_called_once()

    def test_list_duplicates(self):
        playlists = [('Playlist 1', '1'), ('Playlist 2', '2')]
        duplicates = {
            'track1': [
                {
                    'playlist_name': 'Playlist 1',
                    'playlist_id': '1',
                    'track_name': 'Song',
                    'artists': 'Artist'
                },
                {
                    'playlist_name': 'Playlist 2',
                    'playlist_id': '2',
                    'track_name': 'Song',
                    'artists': 'Artist'
                }
            ]
        }

        self.ws.spotify_client.get_user_playlists.return_value = playlists
        self.ws.duplicate_finder.find_cross_playlist_duplicates.return_value = duplicates

        response = self.client.get('/duplicates')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), duplicates)
        self.ws.duplicate_finder.find_cross_playlist_duplicates.assert_called_once_with(playlists)

    def test_cleanup_valid(self):
        playlists = [('Playlist 1', '1'), ('Playlist 2', '2')]
        duplicates = {
            'track1': [
                {
                    'playlist_name': 'Playlist 1',
                    'playlist_id': '1',
                    'track_name': 'Song',
                    'artists': 'Artist'
                },
                {
                    'playlist_name': 'Playlist 2',
                    'playlist_id': '2',
                    'track_name': 'Song',
                    'artists': 'Artist'
                }
            ]
        }
        self.ws.spotify_client.get_user_playlists.return_value = playlists
        self.ws.duplicate_finder.find_cross_playlist_duplicates.return_value = duplicates
        self.ws.playlist_cleaner.remove_duplicates = MagicMock()

        response = self.client.post('/cleanup', json={'keep_playlist_id': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'duplicates removed'})
        self.ws.playlist_cleaner.remove_duplicates.assert_called_once_with(duplicates, '1')

    def test_cleanup_invalid_playlist(self):
        self.ws.spotify_client.get_user_playlists.return_value = [('Playlist 1', '1')]
        response = self.client.post('/cleanup', json={'keep_playlist_id': 'nonexistent'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Playlist not found')


if __name__ == '__main__':
    unittest.main()
