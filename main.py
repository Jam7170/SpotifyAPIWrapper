import os, random, json
from spotifyapi import SpotifyAPI

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

spotify = SpotifyAPI(CLIENT_ID,CLIENT_SECRET)

print(json.dumps(spotify.search_artist("James Marriott"), indent=4))
