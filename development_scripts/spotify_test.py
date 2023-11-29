import json 
import spotipy 
import webbrowser
import pprint

username = 'thebuckemeisterfresh'
clientID = ''
clientSecret = ''
redirect_uri = 'http://google.com/callback/'
scope = "user-read-playback-state,user-modify-playback-state"

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri,
                                    scope=scope) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = spotipy.Spotify(auth=token) 
user_name = spotifyObject.current_user() 
 
# To print the response in readable format. 
# print(json.dumps(user_name, sort_keys=True, indent=4)) 
playlists = spotifyObject.user_playlists(username)
# print(json.dumps(playlists, sort_keys=True, indent=4))

for list in playlists['items']:
    print(list['name'])
    playlist_uri = list['external_urls']['spotify']
    tracks = spotifyObject.playlist_tracks(playlist_uri)["items"]
    for track in tracks:
        track_name = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_duration = track['track']['duration_ms']
        track_uri = track['track']['external_urls']['spotify']
        print(f"{track_name} - {track_artist}: {track_duration}")
        print(f"{track_uri}")
        
        # Requires premium account
        # spotifyObject.start_playback(uris=[track_uri])
        
        # Open the Song in Web Browser
        # kinda clunky spoofing a webbrowser but doable
        # webbrowser.open(track_uri)

        # spoof being an android app to play the track

        # print(json.dumps(tracks, sort_keys=True, indent=4))
