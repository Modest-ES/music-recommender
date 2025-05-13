import pandas as pd
import re
import sqlite3
from typing import List, Dict
from contextlib import closing
from collections import defaultdict

# =================================================================
# sqlite data input search (unstable)

# class MusicSearcher:
#     def __init__(self, db_path):
#         self.db_path = db_path

#     def _get_db_connection(self):
#         """Get a new database connection"""
#         conn = sqlite3.connect(self.db_path)
#         conn.row_factory = sqlite3.Row
#         return conn

#     def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
#         if not query:
#             return []

#         # Clean and split query into terms
#         query = query.lower().strip()
#         terms = re.split(r'\s+', query)
        
#         # Get exclude IDs
#         exclude_ids = [t['id'] for t in liked_tracks + disliked_tracks if 'id' in t]
#         exclude_condition = f"AND id NOT IN ({','.join(['?']*len(exclude_ids))})" if exclude_ids else ""

#         with closing(self._get_db_connection()) as conn:
#             # Base query
#             base_query = f"""
#             SELECT id, artist, track, album, genre,
#                    duration, year, tempo, popularity,
#                    mode, key, signature,
#                    acousticness, danceability, energy, instrumentalness,
#                    liveness, loudness, speechiness, valence
#             FROM songs
#             WHERE 1=1 {exclude_condition}
#             """
            
#             # Execute with parameters
#             params = exclude_ids if exclude_ids else []
#             df = pd.read_sql(base_query, conn, params=params)

#         if df.empty:
#             return []

#         # Calculate match scores (same logic as before)
#         def calculate_score(row):
#             artist = row['artist'].lower()
#             track = row['track'].lower()
            
#             if f"{artist} {track}" == query:
#                 return 100
#             if artist in query:
#                 return 90
#             if track in query:
#                 return 80
                
#             artist_terms = re.split(r'\s+', artist)
#             track_terms = re.split(r'\s+', track)
            
#             score = 0
#             for term in terms:
#                 if term in artist_terms or term in track_terms:
#                     score += 10
#             return score

#         df['score'] = df.apply(calculate_score, axis=1)

#         # Return sorted results
#         return (
#             df.sort_values('score', ascending=False)
#             .head(limit)
#             .drop(columns=['score'])
#             .to_dict('records')
#         )

# =================================================================
# stable standard search

# class MusicSearcher:
#     def __init__(self, outer_dataframe):
#         self.df = outer_dataframe
        
#     def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
#         if not query:
#             return []
            
#         # Clean and split query into terms
#         query = query.lower().strip()
#         terms = re.split(r'\s+', query)
        
#         # Get exclude IDs
#         exclude_ids = [t['id'] for t in liked_tracks + disliked_tracks if 'id' in t]
        
#         # Create search masks
#         artist_mask = pd.Series(False, index=self.df.index)
#         track_mask = pd.Series(False, index=self.df.index)
        
#         # Check if query contains artist-track pattern 
#         for i in range(1, len(terms)):
#             artist_part = ' '.join(terms[:i])
#             track_part = ' '.join(terms[i:])
            
#             artist_mask |= self.df['artist'].str.lower().str.contains(artist_part)
#             track_mask |= self.df['track'].str.lower().str.contains(track_part)
        
#         # Also search for each term individually in both fields
#         for term in terms:
#             artist_mask |= self.df['artist'].str.lower().str.contains(term)
#             track_mask |= self.df['track'].str.lower().str.contains(term)
        
#         # Combine masks and apply exclusions
#         combined_mask = (artist_mask | track_mask) & (~self.df['id'].isin(exclude_ids))
#         results = self.df[combined_mask].copy()
        
#         if results.empty:
#             return []
        
#         # Calculate match scores
#         def calculate_score(row):
#             artist = row['artist'].lower()
#             track = row['track'].lower()
            
#             # Exact matches get highest score
#             if f"{artist} {track}" == query:
#                 return 100
#             if artist in query:
#                 return 90
#             if track in query:
#                 return 80
            
#             # Count matching terms
#             artist_terms = re.split(r'\s+', artist)
#             track_terms = re.split(r'\s+', track)
            
#             score = 0
#             for term in terms:
#                 if term in artist_terms or term in track_terms:
#                     score += 10
            
#             return score
        
#         results['score'] = results.apply(calculate_score, axis=1)
        
#         # Select columns and sort by score
#         columns_to_keep = [
#             'id', 'artist', 'track', 'album', 'genre',
#             'popularity', 'duration', 'tempo', 'year',
#             'mode', 'key', 'signature',
#             'acousticness', 'danceability', 'energy', 'valence',
#             'liveness', 'instrumentalness', 'speechiness', 'loudness'
#         ]
        
#         return (
#             results[columns_to_keep + ['score']]
#             .sort_values('score', ascending=False)
#             .head(limit)
#             .drop(columns=['score'])
#             .to_dict('records')
#         )

# =================================================================
# docker-stable optimized search

class MusicSearcher:
    def __init__(self, outer_dataframe):
        self.df = outer_dataframe
        # Pre-process data for faster searching
        self._build_search_index()
        
    def _build_search_index(self):
        """Build optimized search indices"""
        # Create lowercase versions for case-insensitive search
        self.df['artist_lower'] = self.df['artist'].str.lower()
        self.df['track_lower'] = self.df['track'].str.lower()
        
        # Build term-to-rows mapping
        self.term_index = defaultdict(set)
        for idx, row in self.df.iterrows():
            # Index artist terms
            for term in re.split(r'\s+', row['artist_lower']):
                if term:  # Skip empty terms
                    self.term_index[term].add(idx)
            # Index track terms
            for term in re.split(r'\s+', row['track_lower']):
                if term:
                    self.term_index[term].add(idx)
        
        # Store as DataFrame for vectorized operations
        self.df = self.df.reset_index(drop=True)

    def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
        if not query:
            return []
            
        # Clean and prepare query
        query = query.lower().strip()
        terms = [t for t in re.split(r'\s+', query) if t]
        
        # Get exclude IDs
        exclude_ids = {t['id'] for t in liked_tracks + disliked_tracks if 'id' in t}
        
        # Early exit if no search terms
        if not terms:
            return []
        
        # Find candidate rows using the term index
        candidate_indices = set()
        for term in terms:
            if term in self.term_index:
                candidate_indices.update(self.term_index[term])
        
        # If no candidates found, return empty
        if not candidate_indices:
            return []
            
        # Convert to list for pandas indexing
        candidate_indices = list(candidate_indices)
        
        # Get candidate rows
        candidates = self.df.iloc[candidate_indices].copy()
        
        # Apply exclusions
        if exclude_ids:
            candidates = candidates[~candidates['id'].isin(exclude_ids)]
        
        if candidates.empty:
            return []
        
        # Prepare for exact matching
        full_query = ' '.join(terms)
        artist_track_pairs = []
        
        # Generate all possible artist-track splits (max 3 terms for artist)
        max_artist_terms = min(3, len(terms) - 1)
        for i in range(1, max_artist_terms + 1):
            artist_part = ' '.join(terms[:i])
            track_part = ' '.join(terms[i:])
            artist_track_pairs.append((artist_part, track_part))
        
        # Add reverse order (track-artist)
        for i in range(1, min(3, len(terms))):
            track_part = ' '.join(terms[:i])
            artist_part = ' '.join(terms[i:])
            artist_track_pairs.append((artist_part, track_part))
        
        # Calculate scores - vectorized for performance
        scores = pd.Series(0, index=candidates.index)
        
        # Check for exact artist-track matches
        for artist_part, track_part in artist_track_pairs:
            exact_mask = (
                (candidates['artist_lower'] == artist_part) & 
                (candidates['track_lower'] == track_part))
            scores[exact_mask] = 100
        
        # Check for partial matches
        artist_contains = candidates['artist_lower'].str.contains(full_query)
        track_contains = candidates['track_lower'].str.contains(full_query)
        
        scores[artist_contains & (scores < 90)] = 90
        scores[track_contains & (scores < 80)] = 80
        
        # Term frequency scoring
        term_counts = pd.Series(0, index=candidates.index)
        for term in terms:
            term_counts += candidates['artist_lower'].str.contains(term, regex=False).astype(int)
            term_counts += candidates['track_lower'].str.contains(term, regex=False).astype(int)
        
        scores += term_counts * 10
        
        # Add scores to candidates
        candidates['score'] = scores
        
        # Select and return results
        columns_to_keep = [
            'id', 'artist', 'track', 'album', 'genre',
            'popularity', 'duration', 'tempo', 'year',
            'mode', 'key', 'signature',
            'acousticness', 'danceability', 'energy', 'valence',
            'liveness', 'instrumentalness', 'speechiness', 'loudness'
        ]
        
        return (
            candidates[columns_to_keep + ['score']]
            .sort_values('score', ascending=False)
            .head(limit)
            .drop(columns=['score'])
            .to_dict('records')
        )
