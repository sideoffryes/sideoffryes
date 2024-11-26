from dotenv import load_dotenv
import requests
import os
import base64
from flask import Flask, request, redirect, render_template
import urllib.parse
import threading

# load env vars
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
USER_TOKEN = None

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("newIndex.html")

def get_token():
    # authenticate with spotify
    url = "https://accounts.spotify.com/api/token"
    header = {"Content-Type":"application/x-www-form-urlencoded"}
    msg = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"

    try:
        response = requests.post(url, headers=header, data=msg)

        if response.status_code == 200:
            ACCESS_TOKEN = response.json()["access_token"]
            return ACCESS_TOKEN
        else:
            print(f"ERROR! HTTP Status cude: {response.status_code}")
    except:
        print("Post Request Error!")

@app.route('/callback')
def callback():
    global USER_TOKEN
    auth_code = request.args.get('code')
    if not auth_code:
        error = request.args.get('error')
        print(f"User code request error! Error: {error}")
        return "Code Authorization failed.", 400

    # request code
    url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }

    auth64 = (CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")
    auth64 = str(base64.b64encode(auth64), "utf-8")

    headers = {
        "Authorization": "Basic " + auth64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        token_response = requests.post(url, data=body, headers=headers)
        
        # Exchange code for access token
        if token_response.status_code == 200:
            data = token_response.json()
            access_token = data["access_token"]
            USER_TOKEN = access_token
            return f"User token: {USER_TOKEN}"
        else:
            return f"Code to Token Exchange Error! HTTP Status Code: {token_response.status_code}", token_response.status_code
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 400 

def get_user_token():
    # get user to authenticate with spotify
    url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-read"
    }
    auth_url = f"{url}?{urllib.parse.urlencode(params)}"
    return auth_url

def get_authorization_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_artist_info(artist_uri, access_token):
    # set URL for artist
    url = f"https://api.spotify.com/v1/artists/{artist_uri}"

    # get authorization header
    header = get_authorization_header(access_token)

    # make GET request
    response = requests.get(url, headers=header)

    # test if request was successful
    if response.status_code == 200:
        info = response.json()
        
        # artist name
        name = info["name"]
        
        # artist spotify followers
        followers = info["followers"]["total"]
        
        # combine list of genres into string, comma separated, ending with and
        genres = info["genres"]
        if len(genres) > 2:
            genres = ", ".join(genres[:-1]) + ", and " + genres[-1]
        elif len(genres == 2):
            genres = genres[0] + " and " + genres[1]
        else:
            genres = genres[0]

        print(f"{name} is a {genres} artist with {followers} followers.")
    else:
        print(f"Artist Lookup Error! HTTP status code: {response.status_code}")

def get_artist_albums(artist_uri, access_token):
    # set URL for artist
    url = f"https://api.spotify.com/v1/artists/{artist_uri}/albums"

    # get authorization header
    header = get_authorization_header(access_token)

    # set params to only return albums
    params = {"include_groups": "album"}

    # make GET request
    response = requests.get(url, headers=header, params=params)

    # test response
    if response.status_code == 200:
        items = response.json()["items"]
        counter = 1
        for album in items:
            num_tracks = album["total_tracks"]
            name = album["name"]
            release = album["release_date"]

            print(f"{counter:>2}. {name} has {num_tracks} tracks on it and was released on/in {release}")
            counter += 1
    else:
        print(f"Album Lookup Error! HTTP Status Code: {response.status_code}")

def get_artist_top_tracks(artist_uri, access_token):
    # set URL for artist
    url = f"https://api.spotify.com/v1/artists/{artist_uri}/top-tracks"

    # get authorization header
    header = get_authorization_header(access_token)

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        tracks = response.json()["tracks"]
        counter = 1
        for t in tracks:
            name = t["name"]
            album = t["album"]["name"]
            print(f"{counter:>2}. {name} from {album}")
            counter += 1
    else:
        print(f"Top Tracks Error! HTTP Status Cude: {response.status_code}")

def get_my_info(access_token):
    url = "https://api.spotify.com/v1/me"
    header = get_authorization_header(access_token)

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        data = response.json()
        name = data["display_name"]
        followers = data["followers"]["total"]

        print(f"You are {name}, and you have {followers} followers!")
    else:
        print(f"My Info Error! HTTP Status Code: {response.status_code}")

def get_user_top_items(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    header = get_authorization_header(access_token)
    time_range = ["long_term", "medium_term", "short_term"]
    
    for time in time_range:
        params = {"time_range": time}
        response = requests.get(url, headers=header, params=params)
        
        if response.status_code == 200:
            match time:
                case "long_term":
                    print(f"Over the last year,", end=" ")
                case "medium_term":
                    print(f"Over the last 6 months,", end=" ")
                case "short_term":
                    print("Over the last month,", end=" ")
                case _:
                    print("ERROR! No time length matched!")
            
            print("these were your top tracks:")
        
            tracks = response.json()["items"]
            counter = 1
            for t in tracks:
                album_obj = t["album"]
                album_name = album_obj["name"]
                
                artists_obj = t["artists"]
                artist_names = []
                for artist in artists_obj:
                    artist_names.append(artist["name"])
                artist_names = " ".join(artist_names)
                
                name = t["name"]
                
                print(f"{counter:>2}. {name} by {artist_names} from {album_name}")
                counter += 1
        else:
            print(f"Error fetching user's tracks! HTTP status code: {response.status_code}")
            
        print()
            

if __name__ == "__main__":
    # access_token = get_token()
    # artist = "3TVXtAsR1Inumwj472S9r4"
    # get_artist_info(artist, access_token)
    # print()
    # get_artist_top_tracks(artist, access_token)
    # print()
    # get_artist_albums(artist, access_token)
    # print()
    server_thread = threading.Thread(target=lambda: app.run(port=4400, use_reloader=False, debug=True))
    server_thread.start()
    
    auth_url = get_user_token()
    print(auth_url)
    
    input("Press enter when authentication is complete...")
    
    get_my_info(USER_TOKEN)
    get_user_top_items(USER_TOKEN)