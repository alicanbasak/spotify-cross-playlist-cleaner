from fastapi import FastAPI, HTTPException, Query
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
    artists: list[str] | None = None
    albums: list[str] | None = None
    years: list[int] | None = None

class ScheduleRequest(BaseModel):
    keep_playlist_id: str
    frequency: str = "daily"

@app.get("/playlists")
async def list_playlists():
    playlists = spotify_client.get_user_playlists()
    return [{"name": name, "id": pid} for name, pid in playlists]

@app.get("/duplicates")
async def list_duplicates(
    artists: list[str] | None = Query(None),
    albums: list[str] | None = Query(None),
    years: list[int] | None = Query(None),
):
    playlists = spotify_client.get_user_playlists()
    duplicates = duplicate_finder.find_cross_playlist_duplicates(
        playlists, artists=artists, albums=albums, years=years
    )
    return duplicates

@app.get("/stats")
async def get_stats(
    artists: list[str] | None = Query(None),
    albums: list[str] | None = Query(None),
    years: list[int] | None = Query(None),
):
    playlists = spotify_client.get_user_playlists()
    duplicates = duplicate_finder.find_cross_playlist_duplicates(
        playlists, artists=artists, albums=albums, years=years
    )
    stats = DuplicateFinder.get_duplicate_stats(duplicates)
    return stats

@app.post("/cleanup")
async def cleanup_duplicates(req: CleanupRequest):
    playlists = spotify_client.get_user_playlists()
    playlist_ids = [pid for _, pid in playlists]
    if req.keep_playlist_id not in playlist_ids:
        raise HTTPException(status_code=400, detail="Playlist not found")
    duplicates = duplicate_finder.find_cross_playlist_duplicates(
        playlists,
        artists=req.artists,
        albums=req.albums,
        years=req.years,
    )
    stats = playlist_cleaner.remove_duplicates(duplicates, req.keep_playlist_id)
    return {"status": "duplicates removed", "stats": stats}

@app.post("/schedule")
async def schedule_cleanup(req: ScheduleRequest):
    from scheduler import start_scheduler
    start_scheduler(req.keep_playlist_id, req.frequency)
    return {"status": "scheduled"}
