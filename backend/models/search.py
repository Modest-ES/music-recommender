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

# class MusicSearcher:
#     def __init__(self, outer_dataframe):
#         self.df = outer_dataframe
#         # Pre-process data for faster searching
#         self._build_search_index()
        
#     def _build_search_index(self):
#         """Build optimized search indices"""
#         # Create lowercase versions for case-insensitive search
#         self.df['artist_lower'] = self.df['artist'].str.lower()
#         self.df['track_lower'] = self.df['track'].str.lower()
        
#         # Build term-to-rows mapping
#         self.term_index = defaultdict(set)
#         for idx, row in self.df.iterrows():
#             # Index artist terms
#             for term in re.split(r'\s+', row['artist_lower']):
#                 if term:  # Skip empty terms
#                     self.term_index[term].add(idx)
#             # Index track terms
#             for term in re.split(r'\s+', row['track_lower']):
#                 if term:
#                     self.term_index[term].add(idx)
        
#         # Store as DataFrame for vectorized operations
#         self.df = self.df.reset_index(drop=True)

#     def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
#         if not query:
#             return []
            
#         # Clean and prepare query
#         query = query.lower().strip()
#         terms = [t for t in re.split(r'\s+', query) if t]
        
#         # Get exclude IDs
#         exclude_ids = {t['id'] for t in liked_tracks + disliked_tracks if 'id' in t}
        
#         # Early exit if no search terms
#         if not terms:
#             return []
        
#         # Find candidate rows using the term index
#         candidate_indices = set()
#         for term in terms:
#             if term in self.term_index:
#                 candidate_indices.update(self.term_index[term])
        
#         # If no candidates found, return empty
#         if not candidate_indices:
#             return []
            
#         # Convert to list for pandas indexing
#         candidate_indices = list(candidate_indices)
        
#         # Get candidate rows
#         candidates = self.df.iloc[candidate_indices].copy()
        
#         # Apply exclusions
#         if exclude_ids:
#             candidates = candidates[~candidates['id'].isin(exclude_ids)]
        
#         if candidates.empty:
#             return []
        
#         # Prepare for exact matching
#         full_query = ' '.join(terms)
#         artist_track_pairs = []
        
#         # Generate all possible artist-track splits (max 3 terms for artist)
#         max_artist_terms = min(3, len(terms) - 1)
#         for i in range(1, max_artist_terms + 1):
#             artist_part = ' '.join(terms[:i])
#             track_part = ' '.join(terms[i:])
#             artist_track_pairs.append((artist_part, track_part))
        
#         # Add reverse order (track-artist)
#         for i in range(1, min(3, len(terms))):
#             track_part = ' '.join(terms[:i])
#             artist_part = ' '.join(terms[i:])
#             artist_track_pairs.append((artist_part, track_part))
        
#         # Calculate scores - vectorized for performance
#         scores = pd.Series(0, index=candidates.index)
        
#         # Check for exact artist-track matches
#         for artist_part, track_part in artist_track_pairs:
#             exact_mask = (
#                 (candidates['artist_lower'] == artist_part) & 
#                 (candidates['track_lower'] == track_part))
#             scores[exact_mask] = 100
        
#         # Check for partial matches
#         artist_contains = candidates['artist_lower'].str.contains(full_query)
#         track_contains = candidates['track_lower'].str.contains(full_query)
        
#         scores[artist_contains & (scores < 90)] = 90
#         scores[track_contains & (scores < 80)] = 80
        
#         # Term frequency scoring
#         term_counts = pd.Series(0, index=candidates.index)
#         for term in terms:
#             term_counts += candidates['artist_lower'].str.contains(term, regex=False).astype(int)
#             term_counts += candidates['track_lower'].str.contains(term, regex=False).astype(int)
        
#         scores += term_counts * 10
        
#         # Add scores to candidates
#         candidates['score'] = scores
        
#         # Select and return results
#         columns_to_keep = [
#             'id', 'artist', 'track', 'album', 'genre',
#             'popularity', 'duration', 'tempo', 'year',
#             'mode', 'key', 'signature',
#             'acousticness', 'danceability', 'energy', 'valence',
#             'liveness', 'instrumentalness', 'speechiness', 'loudness'
#         ]
        
#         return (
#             candidates[columns_to_keep + ['score']]
#             .sort_values('score', ascending=False)
#             .head(limit)
#             .drop(columns=['score'])
#             .to_dict('records')
#         )

# ====================================================================================
# sqlite offline

import re
import sqlite3
import threading
from typing import List, Dict
from collections import defaultdict
from contextlib import closing

# Thread-local storage for SQLite connections
thread_local = threading.local()

class MusicSearcher:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_connection()
        self._build_search_index()
        
    def _initialize_connection(self):
        """Initialize a thread-local SQLite connection"""
        if not hasattr(thread_local, "conn"):
            thread_local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            thread_local.conn.execute("PRAGMA journal_mode=WAL")
        
    def _get_connection(self):
        """Get the thread-local connection"""
        if not hasattr(thread_local, "conn"):
            self._initialize_connection()
        return thread_local.conn
    
    def _build_search_index(self):
        """Build optimized search indices"""
        self.term_index = defaultdict(set)
        self.tracks_data = {}
        
        with closing(self._get_connection().cursor()) as cursor:
            cursor.execute("SELECT id, artist, track FROM songs")
            for idx, (track_id, artist, track) in enumerate(cursor.fetchall()):
                self.tracks_data[idx] = {
                    'id': track_id,
                    'artist': artist,
                    'track': track,
                    'artist_lower': artist.lower(),
                    'track_lower': track.lower()
                }
                
                # Index terms
                for term in re.split(r'\s+', artist.lower()):
                    if term: self.term_index[term].add(idx)
                for term in re.split(r'\s+', track.lower()):
                    if term: self.term_index[term].add(idx)
    
    def update_index_with_new_song(self, song_data):
        """Add a single song to the search index"""
        idx = len(self.tracks_data)
        self.tracks_data[idx] = {
            'id': song_data['id'],
            'artist': song_data['artist'],
            'track': song_data['track'],
            'artist_lower': song_data['artist'].lower(),
            'track_lower': song_data['track'].lower()
        }
        
        # Index terms
        for term in re.split(r'\s+', song_data['artist'].lower()):
            if term: self.term_index[term].add(idx)
        for term in re.split(r'\s+', song_data['track'].lower()):
            if term: self.term_index[term].add(idx)

    def _get_full_track_data(self, track_ids: List[str]) -> List[Dict]:
        """Fetch complete track data for results"""
        if not track_ids:
            return []
            
        placeholders = ','.join(['?'] * len(track_ids))
        query = f"""
            SELECT id, artist, track, album, genre,
                   popularity, duration, tempo, year,
                   mode, key, signature,
                   acousticness, danceability, energy, valence,
                   liveness, instrumentalness, speechiness, loudness
            FROM songs
            WHERE id IN ({placeholders})
        """
        
        with closing(self._get_connection().cursor()) as cursor:
            cursor.execute(query, track_ids)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def search(self, query: str, liked_tracks: list = [], disliked_tracks: list = [], limit: int = 20) -> List[Dict]:
        if not query:
            return []
            
        # Clean and prepare query
        query = query.lower().strip()
        terms = [t for t in re.split(r'\s+', query) if t]
        
        # Get exclude IDs
        exclude_ids = {t['id'] for t in liked_tracks + disliked_tracks if 'id' in t}
        
        # Check for numeric ID search
        id_matches = []
        for term in terms:
            if term.isdigit():
                # Check if this numeric term matches any song ID
                if term in {str(track['id']) for idx, track in self.tracks_data.items()}:
                    id_matches.append(term)
        
        # If we found ID matches, prioritize them
        if id_matches:
            # Get full data for matched IDs (excluding liked/disliked tracks)
            results = self._get_full_track_data([id for id in id_matches if id not in exclude_ids])
            # If we have enough ID matches, return them immediately
            if len(results) >= limit:
                return results[:limit]
            # Otherwise, we'll combine with regular search results below
        
        # Proceed with regular search if no ID matches or not enough results
        # Find candidate indices using the term index
        candidate_indices = set()
        for term in terms:
            if term in self.term_index:
                candidate_indices.update(self.term_index[term])
        
        # If no candidates found, return any ID matches we found
        if not candidate_indices:
            return id_matches and self._get_full_track_data(id_matches[:limit]) or []
            
        # Get candidate tracks from our in-memory index
        candidates = []
        for idx in candidate_indices:
            track = self.tracks_data[idx]
            if track['id'] not in exclude_ids:
                candidates.append(track)
        
        if not candidates:
            return id_matches and self._get_full_track_data(id_matches[:limit]) or []
        
        # Score each candidate
        scored_results = []
        for track in candidates:
            score = self._calculate_match_score(track, terms)
            scored_results.append((score, track['id']))
        
        # Sort by score (descending) and get top results
        scored_results.sort(reverse=True, key=lambda x: x[0])
        top_results = [track_id for (score, track_id) in scored_results[:limit - len(id_matches)]]
        
        # Combine ID matches with regular results
        combined_results = []
        if id_matches:
            combined_results.extend(self._get_full_track_data(id_matches))
        combined_results.extend(self._get_full_track_data(top_results))
        
        return combined_results[:limit]

    def _calculate_match_score(self, track: Dict, query_terms: List[str]) -> float:
        """Calculate match score with proper prioritization"""
        artist = track['artist_lower']
        track_name = track['track_lower']
        combined = f"{artist} {track_name}"
        reversed_combined = f"{track_name} {artist}"
        
        # Exact match checks (highest priority)
        exact_query = ''.join(query_terms)
        if combined == exact_query or reversed_combined == exact_query:
            return 1000  # Highest possible score
        
        # Check for exact artist match
        if artist == exact_query:
            return 900
        
        # Check for exact track match
        if track_name == exact_query:
            return 800
        
        # Check for all terms matching in either artist or track
        all_in_artist = all(term in artist for term in query_terms)
        all_in_track = all(term in track_name for term in query_terms)
        
        if all_in_artist and all_in_track:
            return 700
        elif all_in_artist:
            return 600
        elif all_in_track:
            return 500
        
        # Partial matches
        score = 0
        for term in query_terms:
            if term in artist:
                score += 100
            if term in track_name:
                score += 50
                
        return score

    def __del__(self):
        """Clean up connections when done"""
        if hasattr(thread_local, "conn"):
            thread_local.conn.close()
