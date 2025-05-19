import sqlite3
from typing import Dict, Tuple
from contextlib import closing

# class SongManager:
#     def __init__(self, db_path):
#         self.db_path = db_path
#         self._create_tables()

#     def _get_db_connection(self):
#         """Get a new database connection"""
#         conn = sqlite3.connect(self.db_path)
#         conn.row_factory = sqlite3.Row
#         return conn

#     def _create_tables(self):
#         """Ensure tables exist with proper schema"""
#         with closing(self._get_db_connection()) as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS songs (
#                     id INTEGER PRIMARY KEY,
#                     artist TEXT NOT NULL,
#                     track TEXT NOT NULL,
#                     album TEXT,
#                     genre TEXT NOT NULL,
#                     duration INTEGER,
#                     year INTEGER,
#                     tempo INTEGER,
#                     popularity INTEGER,
#                     mode TEXT,
#                     key TEXT,
#                     signature TEXT,
#                     acousticness REAL,
#                     danceability REAL,
#                     energy REAL,
#                     instrumentalness REAL,
#                     liveness REAL,
#                     loudness REAL,
#                     speechiness REAL,
#                     valence REAL
#                 )
#             """)
#             conn.commit()

#     def add_song(self, song_data: Dict) -> Tuple[Dict, int]:
#         try:
#             # Validate required fields
#             if not song_data.get('track') or not song_data.get('artist') or not song_data.get('genre'):
#                 return {"error": "Track, artist, and genre are required fields"}, 400

#             with closing(self._get_db_connection()) as conn:
#                 cursor = conn.cursor()
                
#                 # Get next ID
#                 cursor.execute("SELECT MAX(id) FROM songs")
#                 max_id = cursor.fetchone()[0]
#                 new_id = 1 if max_id is None else max_id + 1

#                 # Insert new song
#                 cursor.execute("""
#                     INSERT INTO songs (
#                         id, artist, track, album, genre,
#                         duration, year, tempo, popularity,
#                         mode, key, signature,
#                         acousticness, danceability, energy, instrumentalness,
#                         liveness, loudness, speechiness, valence
#                     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """, (
#                     new_id,
#                     song_data.get('artist', '').strip(),
#                     song_data.get('track', '').strip(),
#                     song_data.get('album', 'NoData').strip(),
#                     song_data.get('genre', '').strip(),
#                     int(song_data.get('duration', 0)),
#                     int(song_data.get('year', 0)),
#                     int(song_data.get('tempo', 0)),
#                     int(song_data.get('popularity', 0)),
#                     song_data.get('mode', 'NoData'),
#                     song_data.get('key', 'NoData'),
#                     song_data.get('signature', 'NoData'),
#                     float(song_data.get('acousticness', 0.0)),
#                     float(song_data.get('danceability', 0.0)),
#                     float(song_data.get('energy', 0.0)),
#                     float(song_data.get('instrumentalness', 0.0)),
#                     float(song_data.get('liveness', 0.0)),
#                     float(song_data.get('loudness', -6.0)),
#                     float(song_data.get('speechiness', 0.0)),
#                     float(song_data.get('valence', 0.0))
#                 ))
#                 conn.commit()

#                 # Return the inserted song
#                 cursor.execute("SELECT * FROM songs WHERE id = ?", (new_id,))
#                 added_song = dict(cursor.fetchone())
#                 return added_song, 201

#         except Exception as e:
#             print(f"Error adding song: {str(e)}")
#             return {"error": "Could not add song", "details": str(e)}, 500

#     def get_total_songs(self):
#         """Helper method to get total song count"""
#         with closing(self._get_db_connection()) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT COUNT(*) FROM songs")
#             return cursor.fetchone()[0]

# class SongManager:
#     def __init__(self, outer_dataframe):
#         """
#         Initialize with path to the parquet data file
#         """
#         self.df = outer_dataframe
        
#     def add_song(self, song_data: Dict) -> Tuple[Dict, int]:
#         """
#         Add a new song to the dataset
#         Args:
#             song_data: Dictionary containing song attributes
#         Returns:
#             Tuple of (added_song_data, status_code)
#         """
#         try:
#             # Get current dataset length for new ID
#             new_id = len(self.df) + 1
            
#             # Create new song with default values
#             new_song = {
#                 'id': new_id,
#                 'track': song_data.get('track', '').strip(),
#                 'artist': song_data.get('artist', '').strip(),
#                 'genre': song_data.get('genre', '').strip(),
#                 'album': song_data.get('album', 'NoData').strip(),
#                 'year': int(song_data.get('year', 0)),
#                 'duration': int(song_data.get('duration', 0)),
#                 'tempo': int(song_data.get('tempo', 0)),
#                 'popularity': int(song_data.get('popularity', 0)),
#                 'acousticness': float(song_data.get('acousticness', 0.0)),
#                 'energy': float(song_data.get('energy', 0.0)),
#                 'danceability': float(song_data.get('danceability', 0.0)),
#                 'liveness': float(song_data.get('liveness', 0.0)),
#                 'speechiness': float(song_data.get('speechiness', 0.0)),
#                 'instrumentalness': float(song_data.get('instrumentalness', 0.0)),
#                 'valence': float(song_data.get('valence', 0.0)),
#                 'loudness': float(song_data.get('loudness', -6.0)),
#                 'key': song_data.get('key', 'NoData'),
#                 'mode': song_data.get('mode', 'NoData'),
#                 'signature': song_data.get('signature', 'NoData')
#             }
            
#             # Validate required fields
#             if not new_song['track'] or not new_song['artist'] or not new_song['genre']:
#                 return {"error": "Track, artist, and genre are required fields"}, 400
            
#             # Add to dataset
#             self.df.loc[new_id] = new_song
            
#             # Save to persistent storage (you'll need to implement this)
#             # self._save_data()
            
#             return new_song, 201
            
#         except Exception as e:
#             print(f"Error adding song: {str(e)}")
#             return {"error": "Could not add song", "details": str(e)}, 500
    
#     def _save_data(self):
#         """
#         Internal method to save the updated dataset
#         (Implement this based on your storage solution)
#         """
#         # Example for parquet:
#         # self.df.to_parquet(self.data_path)
#         pass

# =================================================
# sqlite offline

import sqlite3
import threading
from typing import Dict, Tuple
from contextlib import closing

# Thread-local storage for SQLite connections
thread_local = threading.local()

class SongManager:
    def __init__(self, db_path: str):
        """
        Initialize with path to SQLite database
        """
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _get_connection(self):
        if not hasattr(thread_local, "conn"):
            thread_local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            thread_local.conn.execute("PRAGMA journal_mode=WAL")
        return thread_local.conn

    def _create_table_if_not_exists(self):
        """Ensure songs table exists with proper schema"""
        with closing(sqlite3.connect(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    album TEXT,
                    year INTEGER,
                    duration INTEGER,
                    tempo INTEGER,
                    popularity INTEGER,
                    acousticness REAL,
                    energy REAL,
                    danceability REAL,
                    liveness REAL,
                    speechiness REAL,
                    instrumentalness REAL,
                    valence REAL,
                    loudness REAL,
                    key TEXT,
                    mode TEXT,
                    signature TEXT
                )
            """)
            conn.commit()

    def add_song(self, song_data: Dict) -> Tuple[Dict, int]:
        """
        Add a new song to the database
        Args:
            song_data: Dictionary containing song attributes
        Returns:
            Tuple of (added_song_data, status_code)
        """
        try:
            # Validate required fields
            if not song_data.get('track') or not song_data.get('artist') or not song_data.get('genre'):
                return {"error": "Track, artist, and genre are required fields"}, 400

            with closing(sqlite3.connect(self.db_path)) as conn:
                cursor = conn.cursor()

                # Insert new song
                cursor.execute("""
                    INSERT INTO songs (
                        track, artist, genre, album, year, duration, tempo,
                        popularity, acousticness, energy, danceability, liveness,
                        speechiness, instrumentalness, valence, loudness,
                        key, mode, signature
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    song_data.get('track', '').strip(),
                    song_data.get('artist', '').strip(),
                    song_data.get('genre', '').strip(),
                    song_data.get('album', 'NoData').strip(),
                    int(song_data.get('year', 0)),
                    int(song_data.get('duration', 0)),
                    int(song_data.get('tempo', 0)),
                    int(song_data.get('popularity', 0)),
                    float(song_data.get('acousticness', 0.0)),
                    float(song_data.get('energy', 0.0)),
                    float(song_data.get('danceability', 0.0)),
                    float(song_data.get('liveness', 0.0)),
                    float(song_data.get('speechiness', 0.0)),
                    float(song_data.get('instrumentalness', 0.0)),
                    float(song_data.get('valence', 0.0)),
                    float(song_data.get('loudness', -6.0)),
                    song_data.get('key', 'NoData'),
                    song_data.get('mode', 'NoData'),
                    song_data.get('signature', 'NoData')
                ))

                # Get the inserted song with its new ID
                song_id = cursor.lastrowid
                cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
                columns = [col[0] for col in cursor.description]
                added_song = dict(zip(columns, cursor.fetchone()))

                conn.commit()
                return added_song, 201

        except ValueError as e:
            print(f"Validation error adding song: {str(e)}")
            return {"error": "Invalid data format", "details": str(e)}, 400
        except sqlite3.Error as e:
            print(f"Database error adding song: {str(e)}")
            return {"error": "Database operation failed", "details": str(e)}, 500
        except Exception as e:
            print(f"Unexpected error adding song: {str(e)}")
            return {"error": "Could not add song", "details": str(e)}, 500

    def get_song_count(self) -> int:
        """Get total number of songs in database"""
        with closing(sqlite3.connect(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM songs")
            return cursor.fetchone()[0]