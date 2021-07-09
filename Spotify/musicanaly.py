import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine
import os
from os import path
from itertools import product

# login credentials
SPOTIPY_CLIENT_ID="d4cda9a688074720a0f43fc547e2dfd5"
SPOTIPY_CLIENT_SECRET = "540fc072359d497a96b5d0ecab65fc67"

# connect to spotipy api
auth_manager = SpotifyClientCredentials(client_secret = SPOTIPY_CLIENT_SECRET, client_id = SPOTIPY_CLIENT_ID)
sp = spotipy.Spotify(auth_manager=auth_manager)

# get playlist
playlist_uri = input("Please enter uri of playlist: ")
playlist_name = input("Please enter a name for the playlist: ")
playlist = sp.playlist_items(playlist_uri)
total = playlist["total"]

# get items
items = playlist["items"]
for i in range(len(items), total-99, 100):
    items.extend( sp.playlist_items(playlist_uri, offset=i, fields=["items"])["items"] )

if(len(items) < total):
    items.extend( sp.playlist_items(playlist_uri, offset=len(items), fields=["items"])["items"] )

print("Got playlist and its items")

# remove local items, as they have no features information
items = list(filter(lambda x: not x["is_local"], items))

# get tracks as items[i]["track"]
tracks = list(map(lambda x: x["track"], items))

# convert to nice dataframe and remove unnecessary data
df_items = pd.DataFrame(items).drop(
        ["added_by", "is_local", "primary_color", "video_thumbnail"], axis=1)
df_items["track"] = df_items["track"].apply(lambda x: x["uri"])
df_tracks = pd.DataFrame(tracks).drop(
        ["album", "is_local", "available_markets", "disc_number", "episode", "explicit", "external_ids", "external_urls", "href", "id", "preview_url", "type", "track_number", "track"], axis=1)

#linked_from sometimes appears and will introduce NULLs that crash sqlalchemy
if "linked_from" in df_tracks.columns:
    df_tracks = df_tracks.drop("linked_from", axis=1)

#add added_at from df_items to df_tracks and discard df_items
added_col = df_items.sort_values("track")["added_at"]
df_tracks = df_tracks.sort_values("uri").join(added_col)
del df_items

print("Processed items into dataframe (df_tracks)")

# retrieve audio features
features = list()
for i in range(0, len(df_tracks)-99, 100):
    features.extend( sp.audio_features(df_tracks["uri"][i:i+100]) )

if(len(features) < len(df_tracks)):
    features.extend( sp.audio_features(df_tracks["uri"][len(features):]) )

# convert features to dataframe
df_features = pd.DataFrame(features).drop(["analysis_url", "track_href", "id", "type", "duration_ms"], axis=1)

print("Got and processed audio features")

# create artists table containing the artists for each track
madeby = [ [artist["uri"], track["uri"]] for track in tracks for artist in track["artists"] ]
df_madeby = pd.DataFrame(madeby, columns=["artist", "track"])

print("Processed madeby information")

# retreive all artist information
artists = list()
artist_uris = df_madeby["artist"].unique()
for i in range(0, len( artist_uris )-49, 50):
    artists.extend( sp.artists(artist_uris[i:i+50])["artists"] )

if(len(artists) < len(artist_uris)):
    artists.extend( sp.artists(artist_uris[len(artists):])["artists"] )

df_artists = pd.DataFrame(artists).drop(["external_urls", "genres", "href", "id", "images", "type"], axis=1)
df_artists["followers"] = df_artists["followers"].apply(lambda x: x["total"])

#extract genre information
genres = [ [artist["uri"], g] for artist in artists for g in artist["genres"]]
df_genres = pd.DataFrame(genres, columns=["artist", "genre"])

print("Got and processed artist information")

# create SQL database
if(path.exists(f"{playlist_name}.db")):
    os.remove(f"{playlist_name}.db")

db = create_engine(f"sqlite:///{playlist_name}.db", echo=False)

# add tracks and features tables (but exclude the json artist information)
df_tracks.drop("artists", axis=1).to_sql("Tracks", con=db)
df_features.to_sql("Features", con=db)
df_madeby.to_sql("Madeby", con=db)
df_artists.to_sql("Artists", con=db)
df_genres.to_sql("Genres", con=db)

print("Set up SQL database")

"""
Resulting SQL Tables:

Tracks
[index, duration_ms, name, popularity, uri, added_at]

Features
[index, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, uri references Tracks.uri, time_signature]

Madeby
[index, artist references Artists.uri, track references Tracks.uri]

Artists
[index, name, uri, track]

Genres
[index, artist references Artists.uri, genre]



For the following, see https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

acousticness
    A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
danceability
    Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
energy
    Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
instrumentalness
    Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
key
    The key the track is in. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
liveness
    Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
loudness
    The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.
mode
    Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
speechiness
    Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
tempo
    The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
time_signature
    An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).
valence
    A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
"""

"""
#Run this to access the db
import pandas as pd
from sqlalchemy import create_engine

db = None

def query(str):
    re = db.execute(str)
    return pd.DataFrame(re.fetchall(), columns=re.keys())

def init():
    return create_engine(f"sqlite:///{input('Enter playlist name: ')}.db", echo=False)

db = init()
"""


def query(str):
    re = db.execute(str)
    return pd.DataFrame(re.fetchall(), columns=re.keys())

def feature_per_time(feature, deg_fit=5):
    data = query(f"SELECT added_at, {feature} FROM items join features on items.track = features.uri order by added_at")
    data["added_at"] = data["added_at"].apply(lambda x: int(x[0:10].replace("-", "")))
    x = list(range(0, len(data[feature])))
    y = data[feature]
    plt.scatter(x, y)
    z = np.polyfit(x, y, deg_fit)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    plt.show()