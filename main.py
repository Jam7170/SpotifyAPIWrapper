import os, random, json
from spotifyapi import SpotifyAPI, SpotifyArtist

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

spotify = SpotifyAPI(CLIENT_ID,CLIENT_SECRET)

def searchAlbum(result=1):
    album = spotify.searchAlbum(input('Search Album\n> '),result)
    
    print(f"\n{album['name']} - {album['artists'][0]['name']}")
    for song in album['tracks']['items']:
        print(f'{song["track_number"]}: {song["name"]}')


searchAlbum()