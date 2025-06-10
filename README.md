# Spotify Cross Playlist Cleaner

A Python application to manage your Spotify playlists and remove duplicate tracks across multiple playlists.

## Features

- Lists all your Spotify playlists
- Finds duplicate tracks across different playlists
- Allows you to keep duplicates in one playlist and remove them from others
- Handles pagination for large playlists
- Secure authentication using environment variables

## Prerequisites

- Python 3.9 or higher
- Spotify Developer Account
- Spotify API Credentials

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/imalican/spotify-cross-playlist-cleaner.git
   cd spotify-cross-playlist-cleaner
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` in the project root and fill in your Spotify API credentials:
   ```bash
   cp .env.example .env
   # then edit .env and set:
   # SPOTIFY_CLIENT_ID=your_client_id
   # SPOTIFY_CLIENT_SECRET=your_client_secret
   # SPOTIFY_REDIRECT_URI=your_redirect_uri
   ```

## Usage

### Command Line

1. Run the application:

   ```bash
   python main.py
   ```

2. Follow the authentication process in your browser

3. The app will:
   - Display all your playlists
   - Find duplicate tracks
   - Let you choose which playlist to keep duplicates in
   - Remove duplicates from other playlists

## Web Service

Run the FastAPI application with **uvicorn**:

```bash
uvicorn web_service:app
```

Endpoints:

- `GET /playlists` – list playlists
- `GET /duplicates` – find duplicate tracks
- `POST /cleanup` – remove duplicates while keeping a specified playlist

See [docs/api.md](docs/api.md) for full details.

## Testing

Install the test dependencies using `pip`:

```bash

pip install -r requirements.txt
```

Run the test suite with:

```bash
pytest
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
