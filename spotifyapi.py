from urllib.parse import urlencode
import base64,requests, datetime, random, json, string
class SpotifyAPI:
    def __init__(self, client_ID,client_secret):
        self.CLIENT_ID = client_ID
        self.CLIENT_SECRET = client_secret
        
        client_creds = f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'
        self.client_creds_b64 = base64.b64encode(client_creds.encode())

        self.performAuth()
        
    def performAuth(self):
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {"grant_type" : "client_credentials"}
        token_headers = {"Authorization": f"Basic {self.client_creds_b64.decode()}"}
        
        r = requests.post(token_url,data=token_data,headers=token_headers)
        
        data = r.json()
        self.valid_request = r.status_code in range(200,299)
        
        if self.valid_request:
            self.access_token = data['access_token']
            expires_in = data['expires_in']
            now = datetime.datetime.now()
            expires = now + datetime.timedelta(seconds=expires_in)
            self.access_token_expires = expires
            self.access_token_did_expire = expires < now
            return True
        else: raise Exception("Authentication failed")

    def getAccessToken(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.performAuth()
            return self.getAccessToken()
        return token
    
    def getResourceHeader(self):
        access_token = self.getAccessToken()
        return {"Authorization" : f"Bearer {access_token}"}
    
    def getResource(self,_id,resource_type):
        endpoint = f"https://api.spotify.com/v1/{resource_type}/{_id}"
        headers = self.getResourceHeader()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def Search(self,query,search_type):
        headers = self.getResourceHeader()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": f"{query}","type": f"{search_type.lower()}"})
        url = f'{endpoint}?{data}'
        r = requests.get(url, headers=headers)
        if r.status_code in range(200,299): return r.json()

    def getAlbum(self, _id):
        return self.getResource(_id,'albums')

    def getArtist(self, _id):
        return self.getResource(_id,'artists')

    def searchArtist(self, query,result=1):
        try: return self.getArtist(self.Search(query,'artist')['artists']['items'][result-1]['id'])
        except TypeError: return False

    def searchAlbum(self, query,result=1):
        try: return self.getAlbum(self.Search(query,'album')['albums']['items'][result-1]['id'])
        except TypeError: return False


class SpotifyArtist(SpotifyAPI):
    def __init__(self,_id,client_id,client_secret):
        super().__init__(client_id,client_secret)

        self._id = _id
        self.artist = self.getArtist(self._id)
        self.url = f'https://api.spotify.com/v1/artists/{self._id}'
        self.name = self.artist["name"]
        self.follower_count = self.artist['followers']['total']
        self.genres = self.artist['genres']
        self.popularity = self.artist['popularity']

    def getTopTracks(self, rjson=True):
        headers = self.getResourceHeader()
        endpoint = f"{self.url}/top-tracks?country=GB"
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        if rjson: return r.json()
    
    def __repr__(self): return f'{self.name} | Rating: {self.popularity} | Followers: {self.follower_count}\nGenres: {self.genres}'
