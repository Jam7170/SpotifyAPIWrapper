from urllib.parse import urlencode
import base64,requests, datetime, random, json, string
class SpotifyAPI:
    def __init__(self, client_ID,client_secret):
        self.CLIENT_ID = client_ID
        self.CLIENT_SECRET = client_secret
        
        client_creds = f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'
        self.client_creds_b64 = base64.b64encode(client_creds.encode())

        self.perform_auth()
        
    def perform_auth(self):
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

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        return {"Authorization" : f"Bearer {access_token}"}
    
    def get_resource(self,_id,resource_type):
        endpoint = f"https://api.spotify.com/v1/{resource_type}/{_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def search(self,query,search_type):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": f"{query}","type": f"{search_type.lower()}"})
        url = f'{endpoint}?{data}'
        r = requests.get(url, headers=headers)
        if r.status_code in range(200,299): return r.json()

    def get_album(self, _id):
        return self.get_resource(_id,'albums')

    def get_artist(self, _id):
        return self.get_resource(_id,'artists')

    def search_artist(self, query,result=1):
        try: return self.get_artist(self.search(query,'artist')['artists']['items'][result-1]['id'])
        except TypeError: return False

    def search_album(self, query,result=1):
        try: return self.get_album(self.search(query,'album')['albums']['items'][result-1]['id'])
        except TypeError: return False

