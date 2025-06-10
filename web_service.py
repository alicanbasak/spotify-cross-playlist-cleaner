from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import SpotifyConfig
from spotify_client import SpotifyClient
from duplicate_finder import DuplicateFinder
from playlist_cleaner import PlaylistCleaner

app = FastAPI(title="Spotify Cross Playlist Cleaner API")

config = SpotifyConfig()
spotify_client = SpotifyClient(config)
duplicate_finder = DuplicateFinder(spotify_client)
playlist_cleaner = PlaylistCleaner(spotify_client)

class CleanupRequest(BaseModel):
    keep_playlist_id: str

@app.get("/playlists")
def list_playlists():
    playlists = spotify_client.get_user_playlists()
    return [{"name": name, "id": pid} for name, pid in playlists]

@app.get("/duplicates")
def list_duplicates():
    playlists = spotify_client.get_user_playlists()
    duplicates = duplicate_finder.find_cross_playlist_duplicates(playlists)
    return duplicates

@app.post("/cleanup")
def cleanup_duplicates(req: CleanupRequest):
    playlists = spotify_client.get_user_playlists()
    playlist_ids = [pid for _, pid in playlists]
    if req.keep_playlist_id not in playlist_ids:
        raise HTTPException(status_code=400, detail="Playlist not found")
    duplicates = duplicate_finder.find_cross_playlist_duplicates(playlists)
    playlist_cleaner.remove_duplicates(duplicates, req.keep_playlist_id)
    return {"status": "duplicates removed"}
