#Import this to access the db
import pandas as pd
from sqlalchemy import create_engine

db = None

def query(str):
    re = db.execute(str)
    return pd.DataFrame(re.fetchall(), columns=re.keys())

def init():
    return create_engine(f"sqlite:///{input('Enter playlist name: ')}.db", echo=False)

db = init()

print("""
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
""")