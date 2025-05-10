import pandas as pd
import re
from typing import List, Dict

class MusicSearcher:
    def __init__(self, outer_dataframe):
        self.df = outer_dataframe
        
    def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
        if not query:
            return []
            
        # Clean and split query into terms
        query = query.lower().strip()
        terms = re.split(r'\s+', query)
        
        # Get exclude IDs
        exclude_ids = [t['id'] for t in liked_tracks + disliked_tracks if 'id' in t]
        
        # Create search masks
        artist_mask = pd.Series(False, index=self.df.index)
        track_mask = pd.Series(False, index=self.df.index)
        
        # Check if query contains artist-track pattern 
        for i in range(1, len(terms)):
            artist_part = ' '.join(terms[:i])
            track_part = ' '.join(terms[i:])
            
            artist_mask |= self.df['artist'].str.lower().str.contains(artist_part)
            track_mask |= self.df['track'].str.lower().str.contains(track_part)
        
        # Also search for each term individually in both fields
        for term in terms:
            artist_mask |= self.df['artist'].str.lower().str.contains(term)
            track_mask |= self.df['track'].str.lower().str.contains(term)
        
        # Combine masks and apply exclusions
        combined_mask = (artist_mask | track_mask) & (~self.df['id'].isin(exclude_ids))
        results = self.df[combined_mask].copy()
        
        if results.empty:
            return []
        
        # Calculate match scores
        def calculate_score(row):
            artist = row['artist'].lower()
            track = row['track'].lower()
            
            # Exact matches get highest score
            if f"{artist} {track}" == query:
                return 100
            if artist in query:
                return 90
            if track in query:
                return 80
            
            # Count matching terms
            artist_terms = re.split(r'\s+', artist)
            track_terms = re.split(r'\s+', track)
            
            score = 0
            for term in terms:
                if term in artist_terms or term in track_terms:
                    score += 10
            
            return score
        
        results['score'] = results.apply(calculate_score, axis=1)
        
        # Select columns and sort by score
        columns_to_keep = [
            'id', 'artist', 'track', 'album', 'genre',
            'popularity', 'duration', 'tempo', 'year',
            'mode', 'key', 'signature',
            'acousticness', 'danceability', 'energy', 'valence',
            'liveness', 'instrumentalness', 'speechiness', 'loudness'
        ]
        
        return (
            results[columns_to_keep + ['score']]
            .sort_values('score', ascending=False)
            .head(limit)
            .drop(columns=['score'])
            .to_dict('records')
        )