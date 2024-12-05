from config import SpotifyConfig  # Import necessary modules
from spotify_client import SpotifyClient
from duplicate_finder import DuplicateFinder
from playlist_cleaner import PlaylistCleaner

def main():
    try:
        config = SpotifyConfig()
        spotify_client = SpotifyClient(config)
        duplicate_finder = DuplicateFinder(spotify_client)
        playlist_cleaner = PlaylistCleaner(spotify_client)
        
        # Retrieve playlists
        print("\nRetrieving playlists...")
        playlists = spotify_client.get_user_playlists()
        
        if not playlists:
            print("No playlists found.")
            exit(1)
        
        # Display playlists
        print("\nPlaylists:")
        for idx, playlist in enumerate(playlists):
            name, _ = playlist  # playlist is now a tuple
            print(f"{idx + 1}. {name}")
        
        # Perform duplicate analysis
        print("\nSearching for duplicate tracks...")
        duplicates = duplicate_finder.find_cross_playlist_duplicates(playlists)
        
        if duplicates:
            print(f"\n{len(duplicates)} tracks found in multiple playlists:")
            
            # Display duplicate tracks
            for track_id, locations in duplicates.items():
                first_location = locations[0]
                print(f"\n{first_location['track_name']} - {first_location['artists']}")
                print("Found in playlists:")
                for loc in locations:
                    print(f"- {loc['playlist_name']}")
            
            # Ask user which playlist to keep duplicates in
            keep_idx = int(input("\nWhich playlist would you like to keep the tracks in? (Enter number): ")) - 1
            
            if 0 <= keep_idx < len(playlists):
                keep_playlist_name, keep_playlist_id = playlists[keep_idx]
                
                confirm = input(f"\nDuplicate tracks will be kept in '{keep_playlist_name}' and "
                              f"removed from other playlists. Do you confirm? (y/n): ")
                
                if confirm.lower() == 'y':
                    print("\nRemoving duplicate tracks...")
                    playlist_cleaner.remove_duplicates(duplicates, keep_playlist_id)
                    print("\nOperation completed!")
                else:
                    print("\nOperation cancelled.")
            else:
                print("\nInvalid selection!")
        else:
            print("\nNo tracks found in multiple playlists!")
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()