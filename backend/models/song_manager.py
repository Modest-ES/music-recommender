import pandas as pd
from typing import Dict, Tuple

class SongManager:
    def __init__(self, outer_dataframe):
        """
        Initialize with path to the parquet data file
        """
        self.df = outer_dataframe
        
    def add_song(self, song_data: Dict) -> Tuple[Dict, int]:
        """
        Add a new song to the dataset
        Args:
            song_data: Dictionary containing song attributes
        Returns:
            Tuple of (added_song_data, status_code)
        """
        try:
            # Get current dataset length for new ID
            new_id = len(self.df) + 1
            
            # Create new song with default values
            new_song = {
                'id': new_id,
                'track': song_data.get('track', '').strip(),
                'artist': song_data.get('artist', '').strip(),
                'genre': song_data.get('genre', '').strip(),
                'album': song_data.get('album', 'NoData').strip(),
                'year': int(song_data.get('year', 0)),
                'duration': int(song_data.get('duration', 0)),
                'tempo': int(song_data.get('tempo', 0)),
                'popularity': int(song_data.get('popularity', 0)),
                'acousticness': float(song_data.get('acousticness', 0.0)),
                'energy': float(song_data.get('energy', 0.0)),
                'danceability': float(song_data.get('danceability', 0.0)),
                'liveness': float(song_data.get('liveness', 0.0)),
                'speechiness': float(song_data.get('speechiness', 0.0)),
                'instrumentalness': float(song_data.get('instrumentalness', 0.0)),
                'valence': float(song_data.get('valence', 0.0)),
                'loudness': float(song_data.get('loudness', -6.0)),
                'key': song_data.get('key', 'NoData'),
                'mode': song_data.get('mode', 'NoData'),
                'signature': song_data.get('signature', 'NoData')
            }
            
            # Validate required fields
            if not new_song['track'] or not new_song['artist'] or not new_song['genre']:
                return {"error": "Track, artist, and genre are required fields"}, 400
            
            # Add to dataset
            self.df.loc[new_id] = new_song
            
            # Save to persistent storage (you'll need to implement this)
            # self._save_data()
            
            return new_song, 201
            
        except Exception as e:
            print(f"Error adding song: {str(e)}")
            return {"error": "Could not add song", "details": str(e)}, 500
    
    def _save_data(self):
        """
        Internal method to save the updated dataset
        (Implement this based on your storage solution)
        """
        # Example for parquet:
        # self.df.to_parquet(self.data_path)
        pass