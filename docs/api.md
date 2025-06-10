# API Documentation

This document describes the HTTP endpoints provided by the `web_service.py` FastAPI application.

## Base URL

```
http://localhost:8000
```

## Endpoints

### `GET /playlists`

Returns the user's playlists.

**Response**

```
[
  {
    "name": "My Playlist",
    "id": "abcd1234"
  },
  ...
]
```

### `GET /duplicates`

Finds duplicate tracks across all playlists. Optional query parameters
`artists`, `albums` and `years` can be provided multiple times for filtering.

**Response**

```
{
  "track_id": [
    {
      "playlist_name": "Playlist A",
      "playlist_id": "123",
      "track_name": "Song",
      "artists": "Artist"
    },
    ...
  ],
  ...
}
```

### `POST /cleanup`

Removes duplicate tracks keeping them in the playlist specified by `keep_playlist_id`.

**Request Body**

```
{
  "keep_playlist_id": "playlist_id_to_keep"
}
```

Optional fields `artists`, `albums` and `years` allow filtering.

**Response**

```
{
  "status": "duplicates removed"
}
```

### `GET /stats`

Returns how many duplicate tracks are found in each playlist.

**Response**

```
{
  "playlist_id": 3,
  "another_playlist": 1
}
```

### `POST /schedule`

Starts scheduled cleanup. The request body accepts `keep_playlist_id` and an optional `frequency` (`daily` or `weekly`).

**Request Body**

```
{
  "keep_playlist_id": "playlist_id_to_keep",
  "frequency": "daily"
}
```

**Response**

```
{
  "status": "scheduled"
}
```
