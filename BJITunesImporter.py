import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine
import os
from os import path
from itertools import product
from tqdm import tqdm
import re

# login credentials, outdated
SPOTIPY_CLIENT_ID="d4cda9a688074720a0f43fc547e2dfd5"
SPOTIPY_CLIENT_SECRET = "540fc072359d497a96b5d0ecab65fc67"

# connect to spotipy api
auth_manager = SpotifyClientCredentials(client_secret = SPOTIPY_CLIENT_SECRET, client_id = SPOTIPY_CLIENT_ID)
sp = spotipy.Spotify(auth_manager=auth_manager)

#get bj's playlist and remove what's not needed
df_itunes = pd.read_csv("BJPlaylist.txt", encoding="UTF-16-le", sep="\t")
"""
df_itunes is the dataframe containing bj's ITunes playlist dump. The following is it's head

[Titelname, Künstler, Komponist, Album, Gruppierung, Werk, Satznummer, Satzzähler, Satzname, Genre, Größe, Dauer, Disc-Nummer, Anzahl der CDs, Titelnummer, Anzahl der Titel, Jahr, Geändert, Hinzugefügt, Datenrate, Abtastrate, Lautstärkeanpassung, Art, Equalizer, Kommentar, Wiedergaben, Zuletzt gespielt, Übersprungen, Zuletzt übersprungen, Meine Wertung, Ort]
"""
df_itunes = df_itunes[["Titelname", "Künstler", "Album", "Dauer", "Jahr", "Wiedergaben"]]
df_itunes = df_itunes.sort_values("Wiedergaben", ascending=False)

#get best fitting spotify URI
failures = []
URIs = []
re_br = re.compile('\([^\)]*\)')
print("Searching tracks in spotify...")
for index, row in tqdm(df_itunes.iterrows(), total=df_itunes.shape[0]):
    res = sp.search(q=f"track:{row['Titelname']} artist:{row['Künstler']} album:{row['Album']}", limit=1, type="track")
    if res["tracks"]["total"] == 0:
        res = sp.search(q=f"track:{row['Titelname']} artist:{row['Künstler']}", limit=1, type="track")
        if res["tracks"]["total"] == 0:
            res = sp.search(q=f"{row['Titelname']} {row['Künstler']}", limit=1, type="track")
            if res["tracks"]["total"] == 0:
                q = re_br.sub("", f"{row['Titelname']} {row['Künstler']}")
                res = sp.search(q=q, limit=1, type="track")
                if res["tracks"]["total"] == 0:
                    failures.append(f"{row['Titelname']}\t{row['Künstler']}\t{row['Album']}")
                    continue
    URI = res["tracks"]["items"][0]["uri"]
    URIs.append(URI)

print(f"Successfully recovered {len(URIs)} songs and failed with {len(failures)}")
print("Writing results...")
with open("BJSucc.txt", "w") as f:
    for uri in URIs:
        _ = f.write(uri)
        _ = f.write("\n")
with open("BJFail.txt", "w") as f:
    for i, fail in enumerate(failures):
        try:
            _ = f.write(fail)
        except:
            print(fail)
        _ = f.write("\n")
print("Finished.")
print("Go to BJSucc.txt and copy the contents into an empty spotify playlist.")
print("The file BJFail.txt contains a list of all failures")