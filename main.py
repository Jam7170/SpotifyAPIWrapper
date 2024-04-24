import os, random, json
from spotifyapi import SpotifyAPI, SpotifyArtist

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

spotify = SpotifyAPI(CLIENT_ID,CLIENT_SECRET)


