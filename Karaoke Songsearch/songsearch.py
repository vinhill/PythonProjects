import pandas as pd
from sqlalchemy import create_engine, MetaData
import re
import sys
import os

class SongSearch():

    def __init__(self, insert_to_db=False, rewrite=False):
    #default table columns for output, rigmar, wii...
        self.tbl_columns = ["Source", "Artist", "Song"]
        self.usdb_columns = ["Source", "Artist", "Song", "Language", "Rating", "Views", "ID"]
        #clear database
        self.insert_to_db = insert_to_db
        if(insert_to_db):
            if(rewrite):
                os.remove("songs.db")
            self.engine = create_engine("sqlite:///songs.db", echo=False)
        
    def load_wii_data(self):
        file = open("Wii.txt", encoding="UTF-8")

        data = pd.DataFrame(columns = self.tbl_columns)

        cur_game = "Null"
        for line in file:
            line = line.strip()
            if(line.startswith("#")):
                cur_game = line[2:];
            else:
                tokens = line.split(" - ")
                try:
                    data.loc[len(data)] = [cur_game, tokens[0], tokens[1]]
                except IndexError:
                    print(tokens)
            if(len(data) % 100 == 0):
                sys.stdout.write(f"\rAt {len(data)}")
                sys.stdout.flush()
                
        file.close()
        
        print("Loaded dataset: Wii Karaoke Games")
        
        if(self.insert_to_db):
            data.to_sql("Songlist", con=self.engine, if_exists='append')
        
        return data

    def load_rigmar_Sunfly_data(self):
        return load_rigmar_data("Rigmar Sunfly.txt", "Rigmar Sunfly")

    def load_rigmar_Custom_data(self):
        return load_rigmar_data("Rigmar Custom.txt", "Rigmar Custom")

    def load_rigmar_data(self, file, name):
        file = open(file, encoding="ANSI")
        
        data = pd.DataFrame(columns = self.tbl_columns)
        
        for line in file:
            line = line.strip()
            tokens = line.split(" - ")
            try:
                data.loc[len(data)] = [name, tokens[0], tokens[1]]
            except IndexError:
                print(tokens)
            if(len(data) % 100 == 0):
                sys.stdout.write(f"\rAt {len(data)}")
                sys.stdout.flush()
                    
        file.close()
        
        print(f"Loaded dataset: {name} Collection")
        
        if(self.insert_to_db):
            data.to_sql("Songlist", con=self.engine, if_exists='append')
        
        return data

    def load_usdb_animux_data(self):
        file = open("USDB.txt", encoding="ANSI")
        
        data = pd.DataFrame(columns = self.usdb_columns)
        
        for line in file:
            line = line.strip()
            tokens = line.split(" --- ")
            tokens.insert(0, "USDB")
            try:
                data.loc[len(data)] = tokens
            except ValueError:
                print(tokens)
            if(len(data) % 100 == 0):
                sys.stdout.write(f"\rAt {len(data)}")
                sys.stdout.flush()
        
        file.close()
        
        print("Loaded dataset: USDB Animux Lyrics")
        
        if(self.insert_to_db):
            data.to_sql("Songlist", con=self.engine, if_exists='append')
        
        return data

    def _process_usdb_animux_html_dump(self):
        #extract artist, song name, language, rating, views, id
        file = open("USDB Dump.txt", encoding="ANSI")
        
        data = pd.DataFrame(columns = self.usdb_columns[1:])
        
        tr_entry = list()
        td_count = 0
        for line in file:
            line = line.replace("-", "")
            try:
                td_count += 1
                if line.startswith("</tr>") or line.startswith("<tr"):
                    #new table entry starts
                    try:
                        data.loc[len(data)] = tr_entry
                    except ValueError:
                        print(tr_entry)
                    tr_entry = list()
                    td_count = 0
                elif td_count == 8:
                    #id entry
                    tr_entry.append(re.search("addToList\((.*),", line).group(1))
                elif td_count == 6:
                    #rating entry
                    rating = len(re.findall("images/star.png", line))
                    if(re.search("images/half_star.png", line) is not None):
                        rating += 0.5
                    tr_entry.append(rating)
                elif td_count == 3 or td_count == 4:
                    #skip edition and golden notes
                    continue
                else:
                    tr_entry.append(re.search(">(.*)</td>", line).group(1))
            except AttributeError:
                print(line)
            if(len(data) % 100 == 0):
                sys.stdout.write(f"\rAt {len(data)}")
                sys.stdout.flush()
        
        file.close()
        
        file = open("USDB.txt", "w", encoding="ANSI")
        for _, row in data.iterrows():
            try:
                #using --- as "-" sometimes appears in this data set
                file.write(f"{row[0]} --- {row[1]} --- {row[2]} --- {row[3]} --- {row[4]} --- {row[5]}\n")
            except UnicodeEncodeError:
                print(row)
        file.flush()
        file.close()
        
        return data

    def query(self, str, limit=20):
        result = self.engine.execute(
                f"SELECT Source, Artist, Song \
                FROM Songlist \
                WHERE Source LIKE ? OR Artist LIKE ? OR Song LIKE ? \
                LIMIT ?", 
                f"%{str}%", f"%{str}%", f"%{str}%", limit).fetchall()
        df = pd.DataFrame(result, columns=self.tbl_columns)
        print(df.to_string())
        return df
        
    def cleanupDB(self):
        os.remove("songs.db")
        self.engine = create_engine("sqlite:///songs.db", echo=False)
        self.insert_to_db = False
        df = load_wii_data()
        df.to_sql("WiiSongs", con=self.engine)
        df = load_usdb_animux_data()
        df.to_sql("USDBSongs", con=self.engine)
        df = load_rigmar_Custom_data()
        df.to_sql("RigmarCustomSongs", con=self.engine)
        self.engine.execute("CREATE VIEW Songlist AS SELECT Source, Artist, Song FROM WiiSongs")

"""
Just running this file from cmd will provide the option to search through the files

For more advanced searches, It might be better to query the database directly:

import pandas as pd
from sqlalchemy import create_engine, MetaData
db = create_engine("sqlite:///songs.db", echo=True)

#query Databases: WiiSongs, USDBSongs Views: Songlist
res = db.execute("SELECT * FROM WiiSongs LIMIT 10")

#format nicely
col = res.keys()
dat = res.fetchall()
df = pd.DataFrame(dat, columns=col)
"""

if __name__ == "__main__":
    print("Welcome!")

    print("WARNING! Pursuing this program will rewrite the database")
    
    print("Available datasets: Rigmar Sunfly, Rigmar Custom, USDB and Wii")
    print("Enter all datasets that shall be loaded: ", end="")
    sets = input()
    se = SongSearch(insert_to_db = True, rewrite=True)
    if("Sunfly" in sets):
        se.load_rigmar_Sunfly_data()
    if("Custom" in sets):
        se.load_rigmar_Custom_data()
    if("USDB" in sets):
        se.load_usdb_animux_data()
    if("Wii" in sets):
        se.load_wii_data()
        
    print("Press control + C to exit")
    print("Query result limit: ", end="")
    limit = input()
    
    while(True):
        print("Search term: ", end="")
        se.query(input(), limit)