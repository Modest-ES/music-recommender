import pandas as pd
import sqlite3
from pathlib import Path
from tqdm import tqdm  # For progress bar

# Paths
parquet_path = './data/songs_2m_parquet.parquet'
sqlite_path = './data/tracksdb.db'

# Read the Parquet file
print("Reading Parquet file...")
df = pd.read_parquet(parquet_path)

# Create SQLite database (deletes existing one if present)
Path(sqlite_path).unlink(missing_ok=True)

# Connect to SQLite
with sqlite3.connect(sqlite_path) as conn:
    print("Creating table structure...")
    # Create table with primary key
    conn.execute("""
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY,
            artist TEXT,
            track TEXT,
            album TEXT,
            genre TEXT,
            duration INTEGER,
            year INTEGER,
            tempo INTEGER,
            popularity INTEGER,
            mode TEXT,
            key TEXT,
            signature TEXT,
            acousticness REAL,
            danceability REAL,
            energy REAL,
            instrumentalness REAL,
            liveness REAL,
            loudness REAL,
            speechiness REAL,
            valence REAL
        )
    """)

    # Insert data in smaller chunks
    chunk_size = 50000  # Reduced from 100000 to avoid SQLite variable limit
    total_chunks = (len(df) // chunk_size) + 1
    
    print(f"Inserting {len(df)} rows in {total_chunks} chunks...")
    for i in tqdm(range(0, len(df), chunk_size)):
        chunk = df.iloc[i:i + chunk_size]
        chunk.to_sql(
            name='songs',
            con=conn,
            if_exists='append',
            index=False,
            method=None  # Disable multi-row insert to avoid variable limit
        )
        conn.commit()  # Explicit commit after each chunk

    # Create indexes after all data is inserted (faster)
    print("Creating indexes...")
    conn.executescript("""
        CREATE INDEX idx_songs_artist ON songs(artist);
        CREATE INDEX idx_songs_genre ON songs(genre);
        CREATE INDEX idx_songs_track ON songs(track);
    """)

print("\nVerifying database...")
with sqlite3.connect(sqlite_path) as conn:
    # Basic verification
    row_count = conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
    print(f"Total rows inserted: {row_count} (should match {len(df)})")
    
    # Verify primary key
    pk_info = conn.execute("PRAGMA table_info(songs)").fetchone()
    print(f"First column is: {pk_info[1]} (type: {pk_info[2]}, PK: {'YES' if pk_info[-1] else 'NO'})")
    
    # Sample records
    print("\nSample records:")
    for row in conn.execute("SELECT id, artist, track FROM songs LIMIT 5"):
        print(row)

print("\nConversion complete!")