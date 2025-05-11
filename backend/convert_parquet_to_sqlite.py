import pandas as pd
import sqlite3
from pathlib import Path

# Paths
parquet_path = './data/songs_2m_parquet.parquet'
sqlite_path = './data/tracksdb.db'

# Read the Parquet file
df = pd.read_parquet(parquet_path)

# Create SQLite database (deletes existing one if present)
Path(sqlite_path).unlink(missing_ok=True)  # Remove old database if exists

# Connect to SQLite and write data
with sqlite3.connect(sqlite_path) as conn:
    df.to_sql(
        name='songs',          # Table name
        con=conn,              # Database connection
        if_exists='replace',   # Overwrite if table exists
        index=False,           # Don't write DataFrame index
        chunksize=100000,      # Batch size for large datasets
        dtype={                # Optional: specify column types
            'id': 'INTEGER',
            'artist': 'TEXT',
            'track': 'TEXT',
            'album': 'TEXT',
            'genre': 'TEXT',
            'duration': 'INTEGER',
            'year': 'INTEGER',
            'tempo': 'INTEGER',
            'popularity': 'INTEGER',
            'mode': 'TEXT',
            'key': 'TEXT',
            'signature': 'TEXT',
            'acousticness': 'REAL',
            'danceability': 'REAL',
            'energy': 'REAL',
            'instrumentalness': 'REAL',
            'liveness': 'REAL',
            'loudness': 'REAL',
            'speechiness': 'REAL',
            'valence': 'REAL'
        }
    )
    
print(f"Successfully converted {len(df)} rows to SQLite database at {sqlite_path}")

with sqlite3.connect(sqlite_path) as conn:
    # Count rows
    row_count = conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
    # Get sample data
    sample = conn.execute("SELECT * FROM songs LIMIT 5").fetchall()
    
print(f"Database contains {row_count} rows")
print("Sample rows:")
for row in sample:
    print(row)