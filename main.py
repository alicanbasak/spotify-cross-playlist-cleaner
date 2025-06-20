from config import SpotifyConfig
from spotify_client import SpotifyClient
from duplicate_finder import DuplicateFinder
from playlist_cleaner import PlaylistCleaner
import argparse

def interactive_flow(
    spotify_client: SpotifyClient,
    duplicate_finder: DuplicateFinder,
    playlist_cleaner: PlaylistCleaner,
) -> None:
    try:
        
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
            try:
                keep_idx = int(input("\nWhich playlist would you like to keep the tracks in? (Enter number): ")) - 1
            except ValueError:
                print("\nPlease enter a valid number.")
                return
            
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spotify Cross Playlist Cleaner CLI"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list-playlists", help="List all playlists")
    find_parser = sub.add_parser(
        "find-duplicates", help="Find duplicate tracks across your playlists"
    )
    find_parser.add_argument("--artists", nargs="*", help="Filter by artist names")
    find_parser.add_argument("--albums", nargs="*", help="Filter by album names")
    find_parser.add_argument("--years", nargs="*", type=int, help="Filter by release years")
    clean_parser = sub.add_parser(
        "remove-duplicates",
        help="Remove duplicates keeping tracks in the specified playlist",
    )
    clean_parser.add_argument(
        "--keep",
        required=True,
        help="Playlist ID to keep duplicate tracks in",
    )
    clean_parser.add_argument("--artists", nargs="*", help="Filter by artist names")
    clean_parser.add_argument("--albums", nargs="*", help="Filter by album names")
    clean_parser.add_argument("--years", nargs="*", type=int, help="Filter by release years")

    schedule_parser = sub.add_parser(
        "schedule-cleanup",
        help="Schedule periodic cleanup",
    )
    schedule_parser.add_argument("--keep", required=True, help="Playlist ID to keep")
    schedule_parser.add_argument(
        "--frequency", choices=["daily", "weekly"], default="daily",
        help="Cleanup frequency"
    )

    args = parser.parse_args()

    config = SpotifyConfig()
    spotify_client = SpotifyClient(config)
    duplicate_finder = DuplicateFinder(spotify_client)
    playlist_cleaner = PlaylistCleaner(spotify_client)

    if args.command == "list-playlists":
        playlists = spotify_client.get_user_playlists()
        for name, pid in playlists:
            print(f"{name}\t{pid}")
    elif args.command == "find-duplicates":
        playlists = spotify_client.get_user_playlists()
        duplicates = duplicate_finder.find_cross_playlist_duplicates(
            playlists,
            artists=args.artists,
            albums=args.albums,
            years=args.years,
        )
        if not duplicates:
            print("No duplicates found")
            return
        for track_id, locations in duplicates.items():
            first = locations[0]
            print(f"{first['track_name']} - {first['artists']}")
            for loc in locations:
                print(f"  {loc['playlist_name']} ({loc['playlist_id']})")
    elif args.command == "remove-duplicates":
        playlists = spotify_client.get_user_playlists()
        duplicates = duplicate_finder.find_cross_playlist_duplicates(
            playlists,
            artists=args.artists,
            albums=args.albums,
            years=args.years,
        )
        stats = playlist_cleaner.remove_duplicates(duplicates, args.keep)
        print("Duplicates removed")
        if stats:
            total = sum(stats.values())
            print(f"Total removed: {total}")
    elif args.command == "schedule-cleanup":
        from scheduler import start_scheduler
        start_scheduler(args.keep, args.frequency)
    else:
        interactive_flow(spotify_client, duplicate_finder, playlist_cleaner)


if __name__ == "__main__":
    main()
