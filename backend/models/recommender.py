import pandas as pd
import numpy as np
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
# from implicit.als import AlternatingLeastSquares
# from scipy.sparse import csr_matrix
from contextlib import closing
import time

#=======================================================
# kNN via sqlite

# class MusicRecommender:
#     def __init__(self, db_path):
#         self.db_path = db_path
#         self._create_tables()
#         self._preprocess_data()
#         self._fit_models()

#     def _create_tables(self):
#         """Ensure necessary tables exist"""
#         with closing(sqlite3.connect(self.db_path)) as conn:
#             cursor = conn.cursor()
#             # Check if tracks table exists
#             cursor.execute("""
#                 SELECT name FROM sqlite_master 
#                 WHERE type='table' AND name='songs'
#             """)
#             if not cursor.fetchone():
#                 raise ValueError("songs table not found in database")

#     def _get_db_connection(self):
#         """Get a new database connection"""
#         conn = sqlite3.connect(self.db_path)
#         conn.row_factory = sqlite3.Row
#         return conn

#     def _preprocess_data(self):
#         """Load and preprocess data from SQLite"""
#         with closing(self._get_db_connection()) as conn:
#             # Load only necessary columns
#             query = """
#             SELECT id, artist, track, album, genre,
#                    duration, year, tempo, popularity,
#                    mode, key, signature,
#                    acousticness, danceability, energy, instrumentalness,
#                    liveness, loudness, speechiness, valence
#             FROM songs
#             """
#             self.df = pd.read_sql(query, conn)

#         # Store original values before normalization
#         self.display_columns = ['loudness', 'tempo', 'popularity', 'duration']
#         for col in self.display_columns:
#             self.df[f'original_{col}'] = self.df[col].copy()

#         # Feature columns for recommendations
#         self.feature_columns = [
#             'acousticness', 'danceability', 'energy', 'instrumentalness',
#             'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
#             'popularity', 'duration'
#         ]

#         # Normalize features
#         self.scaler = MinMaxScaler()
#         self.df[self.feature_columns] = self.scaler.fit_transform(
#             self.df[self.feature_columns]
#         )

#         # Prepare genre features if available
#         if 'genre' in self.df.columns:
#             self.df['genre'] = self.df['genre'].fillna('NoData')
#             self.genre_dummies = pd.get_dummies(self.df['genre'], prefix='genre')

#     def _fit_models(self):
#         """Train recommendation models"""
#         # Content-based similarity matrix
#         self.content_features = self.df[self.feature_columns]
#         if hasattr(self, 'genre_dummies'):
#             self.content_features = pd.concat(
#                 [self.content_features, self.genre_dummies], axis=1
#             )
        
#         # Item-item collaborative model
#         self.item_item_model = NearestNeighbors(
#             n_neighbors=50, 
#             metric='cosine', 
#             algorithm='brute'
#         )
#         self.item_item_model.fit(self.content_features)

#     def initial_recommendations(self, user_prefs):
#         try:
#             # Start with all songs from SQLite
#             results = self.df.copy()

#             # Calculate similarity for audio features
#             audio_features = [
#                 'popularity', 'loudness', 'acousticness', 'danceability',
#                 'energy', 'liveness', 'instrumentalness', 'speechiness', 'valence'
#             ]
            
#             # Filter to only features present in both request and database
#             valid_features = [f for f in audio_features if f in user_prefs and f in results.columns]
            
#             if not valid_features:
#                 return self._format_results(results.sample(min(10, len(results))))

#             # Create user preference vector
#             pref_vector = [user_prefs[f] for f in valid_features]
#             features = results[valid_features]
            
#             # Calculate similarity
#             similarities = cosine_similarity([pref_vector], features)[0]
#             results['similarity'] = similarities

#             # Get genre strictness (default to 5 if not specified)
#             genre_strictness = user_prefs['genre_strictness']
#             genre_penalty = 0.07 * genre_strictness  # 0.07 to 0.7 based on strictness

#             # Apply genre multiplier (but don't filter)
#             if 'genre_strictness' in user_prefs:
#                 selected_genres = [key[6:] for key in user_prefs if key.startswith('genre_')]
#                 def genre_multiplier(genre):
#                     if genre in selected_genres:
#                         return 1.0
#                     return max(0.1, 1.0 - genre_penalty)  # Minimum multiplier of 0.1
#                 results['genre_multiplier'] = results['genre'].apply(genre_multiplier)
#                 results['similarity'] = results['similarity'] * results['genre_multiplier']

#             # Calculate influence multipliers
#             liked_genre_influence = 1.0 + (0.02 * user_prefs.get('liked_genre_influence', 5))
#             disliked_genre_influence = 1.0 - (0.01 * user_prefs.get('disliked_genre_influence', 5))
#             liked_artist_influence = 1.0 + (0.02 * user_prefs.get('liked_artist_influence', 5))
#             disliked_artist_influence = 1.0 - (0.01 * user_prefs.get('disliked_artist_influence', 5))
            
#             # Get liked/disliked genres and artists
#             liked_genres = set(track['genre'] for track in user_prefs.get('liked_tracks', []) if 'genre' in track)
#             disliked_genres = set(track['genre'] for track in user_prefs.get('disliked_tracks', []) if 'genre' in track)
#             liked_artists = set(track['artist'] for track in user_prefs.get('liked_tracks', []) if 'artist' in track)
#             disliked_artists = set(track['artist'] for track in user_prefs.get('disliked_tracks', []) if 'artist' in track)
            
#             # Apply genre multipliers
#             def playlists_genre_multiplier(genre):
#                 if genre in liked_genres:
#                     return liked_genre_influence
#                 elif genre in disliked_genres:
#                     return disliked_genre_influence
#                 return 1.0
            
#             results['playlists_genre_multiplier'] = results['genre'].apply(playlists_genre_multiplier)
            
#             # Apply artist multipliers
#             def artist_multiplier(artist):
#                 if artist in liked_artists:
#                     return liked_artist_influence
#                 elif artist in disliked_artists:
#                     return disliked_artist_influence
#                 return 1.0
            
#             results['artist_multiplier'] = results['artist'].apply(artist_multiplier)
            
#             # Calculate final similarity
#             results['similarity'] = (
#                 results['similarity'] * 
#                 results['playlists_genre_multiplier'] * 
#                 results['artist_multiplier']
#             )

#             if all(k in user_prefs for k in ['year_min', 'year_max', 'year_strictness']):
#                 year_min = user_prefs['year_min']
#                 year_max = user_prefs['year_max']
#                 year_strictness = user_prefs['year_strictness']
#                 penalty_rate = 0.01 * year_strictness  # 0.01 to 0.1 based on strictness
                
#                 def year_multiplier(year):
#                     if year_min <= year <= year_max:
#                         return 1.0
#                     elif year < year_min:
#                         distance = year_min - year
#                     else:
#                         distance = year - year_max
                    
#                     multiplier = max(0.1, 1.0 - (distance * penalty_rate))
#                     return multiplier
                
#                 results['year_multiplier'] = results['year'].apply(year_multiplier)
#                 results['similarity'] = results['similarity'] * results['year_multiplier']

#             if all(k in user_prefs for k in ['tempo_min', 'tempo_max', 'tempo_strictness']):
#                 tempo_min = user_prefs['tempo_min']
#                 tempo_max = user_prefs['tempo_max']
#                 tempo_strictness = user_prefs['tempo_strictness']
#                 penalty_rate = 0.01 * tempo_strictness
                
#                 def tempo_multiplier(tempo):
#                     if tempo_min <= tempo <= tempo_max:
#                         return 1.0
#                     elif tempo < tempo_min:
#                         distance = tempo_min - tempo
#                     else:
#                         distance = tempo - tempo_max
                    
#                     multiplier = max(0.1, 1.0 - (distance * penalty_rate))
#                     return multiplier
                
#                 results['tempo_multiplier'] = results['original_tempo'].apply(tempo_multiplier)
#                 results['similarity'] = results['similarity'] * results['tempo_multiplier']

#             if all(k in user_prefs for k in ['duration_min', 'duration_max', 'duration_strictness']):
#                 duration_min = user_prefs['duration_min']
#                 duration_max = user_prefs['duration_max']
#                 duration_strictness = user_prefs['duration_strictness']
#                 penalty_rate = 0.01 * duration_strictness
                
#                 def duration_multiplier(duration):
#                     if duration_min <= duration <= duration_max:
#                         return 1.0
#                     elif duration < duration_min:
#                         distance = duration_min - duration
#                     else:
#                         distance = duration - duration_max
                    
#                     multiplier = max(0.1, 1.0 - (distance * penalty_rate))
#                     return multiplier
                
#                 results['duration_multiplier'] = results['original_duration'].apply(duration_multiplier)
#                 results['similarity'] = results['similarity'] * results['duration_multiplier']

#             return self._format_results(
#                 results.sort_values('similarity', ascending=False).head(20)
#             )
            
#         except Exception as e:
#             print(f"Recommendation error: {str(e)}")
#             return self._format_results(self.df.sample(min(10, len(self.df))))

#     def refined_recommendations(self, initial_tracks, adjustments):
#         """Refine recommendations based on user feedback"""
#         track_ids = [t['track_id'] for t in initial_tracks if 'track_id' in t]
#         if not track_ids:
#             return self.initial_recommendations(adjustments)
            
#         # Get features of liked tracks
#         liked_features = self.content_features.loc[
#             self.df['id'].isin(track_ids)
#         ].mean(axis=0)
        
#         # Apply user adjustments
#         for feature, adjustment in adjustments.items():
#             if feature in liked_features.index:
#                 liked_features[feature] = adjustment
                
#         # Find similar tracks
#         distances, indices = self.item_item_model.kneighbors([liked_features])
        
#         # Exclude already recommended tracks
#         new_indices = [i for i in indices[0] if i not in track_ids][:10]
#         results = self.df.iloc[new_indices]
#         return self._format_results(results)

#     def _format_results(self, df):
#         """Format results for frontend"""
#         columns_to_keep = [
#             'id', 'artist', 'track', 'album', 'genre',
#             'popularity', 'duration', 'tempo', 'year',
#             'mode', 'key', 'signature',
#             'acousticness', 'danceability', 'energy', 'valence',
#             'liveness', 'instrumentalness', 'speechiness', 'loudness'
#         ]
        
#         # Replace normalized values with originals
#         for col in self.display_columns:
#             if f'original_{col}' in df.columns:
#                 df[col] = df[f'original_{col}']
        
#         return df[columns_to_keep].to_dict('records')

#     def get_track_details(self, track_id):
#         """Get complete track details from database"""
#         with closing(self._get_db_connection()) as conn:
#             query = "SELECT * FROM tracks WHERE id = ?"
#             track = pd.read_sql(query, conn, params=(track_id,))
#             if not track.empty:
#                 return track.iloc[0].to_dict()
#         return None

# ======================================================
# stable kNN

class MusicRecommender:
    def __init__(self, outer_dataframe):
        self.df = outer_dataframe
        # Define which columns need to keep original values
        self.display_columns = ['loudness', 'tempo', 'popularity', 'duration', 'year']
        self.feature_columns = [
            'acousticness', 'danceability', 'energy', 'instrumentalness',
            'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
            'popularity', 'duration'
        ]
        self._preprocess_data()
        self._fit_models()

    def _preprocess_data(self):
        """Prepare data for recommendation"""
        # Handle missing values
        self.df = self.df.dropna(subset=self.feature_columns)
        
        # Create copies of original values for display columns
        for col in self.display_columns:
            self.df[f'original_{col}'] = self.df[col].copy()
        
        # Normalize features
        self.scaler = MinMaxScaler()
        self.df[self.feature_columns] = self.scaler.fit_transform(
            self.df[self.feature_columns]
        )
        
        # Prepare genre features if available
        if 'genre' in self.df.columns:
            self.df['genre'] = self.df['genre'].fillna('NoData')
            self.genre_dummies = pd.get_dummies(self.df['genre'], prefix='genre')
        
    def _fit_models(self):
        start_time = time.time()
        """Train recommendation models"""
        # Content-based similarity matrix
        self.content_features = self.df[self.feature_columns]
        if hasattr(self, 'genre_dummies'):
            self.content_features = pd.concat(
                [self.content_features, self.genre_dummies], axis=1
            )
        
        # Item-item collaborative model
        self.item_item_model = NearestNeighbors(
            n_neighbors=50, 
            metric='cosine', 
            algorithm='brute'
        )
        self.item_item_model.fit(self.content_features)
        print(f"Model training completed in {time.time() - start_time:.2f} seconds")

    def _apply_multipliers(self, results, user_prefs):
        """Apply all preference multipliers in optimized way"""
        # Prepare all multiplier functions
        multipliers = []
        
        # Genre strictness multiplier
        if 'genre_strictness' in user_prefs:
            genre_strictness = user_prefs['genre_strictness']
            genre_penalty = 0.07 * genre_strictness
            selected_genres = [key[6:] for key in user_prefs if key.startswith('genre_')]
            
            def genre_multiplier(genre):
                if genre in selected_genres:
                    return 1.0
                return max(0.1, 1.0 - genre_penalty)
            
            results['genre_multiplier'] = results['genre'].apply(genre_multiplier)
            multipliers.append('genre_multiplier')
        
        # Playlist influence multipliers
        liked_genres = set(track.get('genre') for track in user_prefs.get('liked_tracks', []) if track.get('genre'))
        disliked_genres = set(track.get('genre') for track in user_prefs.get('disliked_tracks', []) if track.get('genre'))
        liked_artists = set(track.get('artist') for track in user_prefs.get('liked_tracks', []) if track.get('artist'))
        disliked_artists = set(track.get('artist') for track in user_prefs.get('disliked_tracks', []) if track.get('artist'))
        
        # Genre influence
        if liked_genres or disliked_genres:
            liked_influence = 1.0 + (0.02 * user_prefs.get('liked_genre_influence', 5))
            disliked_influence = 1.0 - (0.01 * user_prefs.get('disliked_genre_influence', 5))
            
            def genre_influence(genre):
                if genre in liked_genres:
                    return liked_influence
                elif genre in disliked_genres:
                    return disliked_influence
                return 1.0
            
            results['genre_influence'] = results['genre'].apply(genre_influence)
            multipliers.append('genre_influence')
        
        # Artist influence
        if liked_artists or disliked_artists:
            liked_artist = 1.0 + (0.02 * user_prefs.get('liked_artist_influence', 5))
            disliked_artist = 1.0 - (0.01 * user_prefs.get('disliked_artist_influence', 5))
            
            def artist_influence(artist):
                if artist in liked_artists:
                    return liked_artist
                elif artist in disliked_artists:
                    return disliked_artist
                return 1.0
            
            results['artist_influence'] = results['artist'].apply(artist_influence)
            multipliers.append('artist_influence')
        
        # Range filters (year, tempo, duration)
        range_filters = [
            ('year', 'year', 'original_year'),
            ('tempo', 'tempo', 'original_tempo'),
            ('duration', 'duration_ms', 'original_duration')
        ]
        
        for prefix, min_key, max_key in range_filters:
            if all(k in user_prefs for k in [f'{prefix}_min', f'{prefix}_max', f'{prefix}_strictness']):
                min_val = user_prefs[f'{prefix}_min']
                max_val = user_prefs[f'{prefix}_max']
                strictness = user_prefs[f'{prefix}_strictness']
                penalty_rate = 0.01 * strictness
                
                def range_multiplier(val, min_v=min_val, max_v=max_val, rate=penalty_rate):
                    if min_v <= val <= max_v:
                        return 1.0
                    elif val < min_v:
                        distance = min_v - val
                    else:
                        distance = val - max_v
                    return max(0.1, 1.0 - (distance * rate))
                
                col_name = f'{prefix}_multiplier'
                results[col_name] = results[max_key].apply(range_multiplier)
                multipliers.append(col_name)
        
        # Apply all multipliers in one operation
        if multipliers:
            results['similarity'] = results['similarity'] * results[multipliers].prod(axis=1)
        
        return results

    def initial_recommendations(self, user_prefs):
        try:
            start_time = time.time()
            # Start with all songs
            results = self.df.copy()
            
            # Calculate similarity for audio features
            audio_features = [
                'popularity', 'loudness', 'acousticness', 'danceability',
                'energy', 'liveness', 'instrumentalness', 'speechiness', 'valence'
            ]
            
            # Filter to only features present in both request and dataset
            valid_features = [f for f in audio_features if f in user_prefs and f in results.columns]
            
            if not valid_features:
                return self._format_results(results.sample(min(10, len(results))))
            
            # Create user preference vector
            pref_vector = [user_prefs[f] for f in valid_features]
            features = results[valid_features]

            # Calculate similarity
            similarities = cosine_similarity([pref_vector], features)[0]
            results['similarity'] = similarities

            results = self._apply_multipliers(results, user_prefs)

            print(f"Recommendation generated in {time.time() - start_time:.2f} seconds")
            return self._format_results(
                results.sort_values('similarity', ascending=False).head(20)
            )
        
        except Exception as e:
            print(f"Recommendation error: {str(e)}")
            # Return some results even if error occurs
            return self._format_results(self.df.sample(min(10, len(self.df))))

    def _format_results(self, df):
        """Select only relevant columns for the frontend and restore original values"""
        columns_to_keep = [
            'id', 'artist', 'track', 'album', 'genre',
            'popularity', 'duration', 'tempo', 'year',
            'mode', 'key', 'signature',
            'acousticness', 'danceability', 'energy', 'valence',
            'liveness', 'instrumentalness', 'speechiness', 'loudness',
            'original_tempo', 'original_popularity', 'original_loudness', 'original_duration', 'similarity'
        ]
        
        # Add the original values for display columns
        for col in self.display_columns:
            if f'original_{col}' in df.columns:
                columns_to_keep.append(f'original_{col}')
                # Rename to original column name for frontend
                df = df.rename(columns={f'original_{col}': col})
        
        return df[[col for col in columns_to_keep if col in df.columns]]

# ======================================================
# kNN + MF(weighed ALS)

# class MusicRecommender:
#     def __init__(self, outer_dataframe):
#         self.df = outer_dataframe
#         # Define which columns need to keep original values
#         self.display_columns = ['loudness', 'tempo', 'popularity', 'duration', 'year']
#         self.feature_columns = [
#             'acousticness', 'danceability', 'energy', 'instrumentalness',
#             'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
#             'popularity', 'duration'
#         ]
#         self._preprocess_data()
#         self._fit_models()

#     def _preprocess_data(self):
#         """Prepare data for recommendation"""
#         # Handle missing values
#         self.df = self.df.dropna(subset=self.feature_columns)
        
#         # Create copies of original values for display columns
#         for col in self.display_columns:
#             self.df[f'original_{col}'] = self.df[col].copy()
        
#         # Normalize features
#         self.scaler = MinMaxScaler()
#         self.df[self.feature_columns] = self.scaler.fit_transform(
#             self.df[self.feature_columns]
#         )
        
#         # Prepare genre features if available
#         if 'genre' in self.df.columns:
#             self.df['genre'] = self.df['genre'].fillna('NoData')
#             self.genre_dummies = pd.get_dummies(self.df['genre'], prefix='genre', sparse=True)
        
#         # Create synthetic user-item interactions based on audio features
#         self._create_synthetic_interactions()

#     def _create_synthetic_interactions(self):
#         """Create implicit feedback matrix from audio features"""
#         # Scale features to create "implicit ratings" (0-100)
#         interaction_scores = (self.df[self.feature_columns] * 100).astype('int32')
        
#         # Create sparse user-item matrix (treating each feature as a "user")
#         rows, cols, data = [], [], []
#         for item_idx in range(len(self.df)):
#             for feat_idx, score in enumerate(interaction_scores.iloc[item_idx]):
#                 if score > 0:  # Only store positive interactions
#                     rows.append(feat_idx)
#                     cols.append(item_idx)
#                     data.append(score)
        
#         self.interaction_matrix = csr_matrix(
#             (data, (rows, cols)),
#             shape=(len(self.feature_columns), len(self.df))
#         )

#     def _fit_models(self):
#         """Train all recommendation models"""
#         start_time = time.time()
        
#         # Content-based similarity matrix
#         self.content_features = self.df[self.feature_columns]
#         if hasattr(self, 'genre_dummies'):
#             self.content_features = pd.concat(
#                 [self.content_features, self.genre_dummies], axis=1
#             )
        
#         # Item-item collaborative model
#         self.item_item_model = NearestNeighbors(
#             n_neighbors=50, 
#             metric='cosine', 
#             algorithm='brute'
#         )
#         self.item_item_model.fit(self.content_features)
        
#         # Weighted ALS model
#         self.als_model = AlternatingLeastSquares(
#             factors=64,
#             regularization=0.1,
#             iterations=15,
#             use_gpu=False,
#             calculate_training_loss=True
#         )
        
#         # Apply BM25 weighting to interactions
#         weighted_interactions = self._bm25_weight(self.interaction_matrix)
#         self.als_model.fit(weighted_interactions)
        
#         print(f"Model training completed in {time.time() - start_time:.2f} seconds")

#     def _bm25_weight(self, interactions, K1=1.2, B=0.75):
#         """Apply BM25 weighting to interaction matrix"""
#         # Calculate document frequencies
#         df = np.bincount(interactions.indices)
        
#         # Calculate IDF
#         N = interactions.shape[1]
#         idf = np.log((N - df + 0.5) / (df + 0.5))
        
#         # Calculate document lengths
#         doc_len = np.array(interactions.sum(axis=0)).squeeze()
#         avg_len = doc_len.mean()
        
#         # Apply BM25 weighting
#         rows, cols = interactions.nonzero()
#         data = interactions.data
        
#         weights = data * (K1 + 1) / (
#             data + K1 * (1 - B + B * doc_len[cols] / avg_len)
#         ) * idf[cols]
        
#         return csr_matrix((weights, (rows, cols)), shape=interactions.shape)

#     def _apply_multipliers(self, results, user_prefs):
#         """Apply all preference multipliers in optimized way"""
#         # Prepare all multiplier functions
#         multipliers = []
        
#         # Genre strictness multiplier
#         if 'genre_strictness' in user_prefs:
#             genre_strictness = user_prefs['genre_strictness']
#             genre_penalty = 0.07 * genre_strictness
#             selected_genres = [key[6:] for key in user_prefs if key.startswith('genre_')]
            
#             def genre_multiplier(genre):
#                 if genre in selected_genres:
#                     return 1.0
#                 return max(0.1, 1.0 - genre_penalty)
            
#             results['genre_multiplier'] = results['genre'].apply(genre_multiplier)
#             multipliers.append('genre_multiplier')
        
#         # Playlist influence multipliers
#         liked_genres = set(track.get('genre') for track in user_prefs.get('liked_tracks', []) if track.get('genre'))
#         disliked_genres = set(track.get('genre') for track in user_prefs.get('disliked_tracks', []) if track.get('genre'))
#         liked_artists = set(track.get('artist') for track in user_prefs.get('liked_tracks', []) if track.get('artist'))
#         disliked_artists = set(track.get('artist') for track in user_prefs.get('disliked_tracks', []) if track.get('artist'))
        
#         # Genre influence
#         if liked_genres or disliked_genres:
#             liked_influence = 1.0 + (0.02 * user_prefs.get('liked_genre_influence', 5))
#             disliked_influence = 1.0 - (0.01 * user_prefs.get('disliked_genre_influence', 5))
            
#             def genre_influence(genre):
#                 if genre in liked_genres:
#                     return liked_influence
#                 elif genre in disliked_genres:
#                     return disliked_influence
#                 return 1.0
            
#             results['genre_influence'] = results['genre'].apply(genre_influence)
#             multipliers.append('genre_influence')
        
#         # Artist influence
#         if liked_artists or disliked_artists:
#             liked_artist = 1.0 + (0.02 * user_prefs.get('liked_artist_influence', 5))
#             disliked_artist = 1.0 - (0.01 * user_prefs.get('disliked_artist_influence', 5))
            
#             def artist_influence(artist):
#                 if artist in liked_artists:
#                     return liked_artist
#                 elif artist in disliked_artists:
#                     return disliked_artist
#                 return 1.0
            
#             results['artist_influence'] = results['artist'].apply(artist_influence)
#             multipliers.append('artist_influence')
        
#         # Range filters (year, tempo, duration)
#         range_filters = [
#             ('year', 'year', 'original_year'),
#             ('tempo', 'tempo', 'original_tempo'),
#             ('duration', 'duration_ms', 'original_duration')
#         ]
        
#         for prefix, min_key, max_key in range_filters:
#             if all(k in user_prefs for k in [f'{prefix}_min', f'{prefix}_max', f'{prefix}_strictness']):
#                 min_val = user_prefs[f'{prefix}_min']
#                 max_val = user_prefs[f'{prefix}_max']
#                 strictness = user_prefs[f'{prefix}_strictness']
#                 penalty_rate = 0.01 * strictness
                
#                 def range_multiplier(val, min_v=min_val, max_v=max_val, rate=penalty_rate):
#                     if min_v <= val <= max_v:
#                         return 1.0
#                     elif val < min_v:
#                         distance = min_v - val
#                     else:
#                         distance = val - max_v
#                     return max(0.1, 1.0 - (distance * rate))
                
#                 col_name = f'{prefix}_multiplier'
#                 results[col_name] = results[max_key].apply(range_multiplier)
#                 multipliers.append(col_name)
        
#         # Apply all multipliers in one operation
#         if multipliers:
#             results['similarity'] = results['similarity'] * results[multipliers].prod(axis=1)
        
#         return results

#     def initial_recommendations(self, user_prefs):
#         try:
#             start_time = time.time()
            
#             # Start with all songs
#             results = self.df.copy()
            
#             # Calculate similarity for audio features
#             audio_features = [
#                 'popularity', 'loudness', 'acousticness', 'danceability',
#                 'energy', 'liveness', 'instrumentalness', 'speechiness', 'valence'
#             ]
            
#             # Filter to only features present in both request and dataset
#             valid_features = [f for f in audio_features if f in user_prefs and f in results.columns]
            
#             if not valid_features:
#                 return self._format_results(results.sample(min(10, len(results))))
            
#             # Create user preference vector
#             pref_vector = [user_prefs[f] for f in valid_features]
#             features = results[valid_features]

#             # Calculate content-based similarity
#             content_similarities = cosine_similarity([pref_vector], features)[0]
            
#             # Get ALS recommendations
#             als_scores = self._get_als_scores(user_prefs, valid_features)
            
#             # Combine scores (60% content, 40% ALS)
#             results['similarity'] = (0.6 * content_similarities) + (0.4 * als_scores)
            
#             # Apply preference multipliers
#             results = self._apply_multipliers(results, user_prefs)

#             print(f"Recommendation generated in {time.time() - start_time:.2f} seconds")
#             return self._format_results(
#                 results.sort_values('similarity', ascending=False).head(20))
            
#         except Exception as e:
#             print(f"Recommendation error: {str(e)}")
#             return self._format_results(self.df.sample(min(10, len(self.df))))

#     def _get_als_scores(self, user_prefs, valid_features):
#         """Get recommendations from ALS model"""
#         # Create user vector based on preferences
#         user_vector = np.zeros(len(self.feature_columns))
        
#         # Map user preferences to feature indices
#         feature_indices = {f: i for i, f in enumerate(self.feature_columns) if f in valid_features}
#         for f in valid_features:
#             if f in feature_indices:
#                 user_vector[feature_indices[f]] = user_prefs[f]
        
#         # Get item scores from ALS model
#         user_factors = self.als_model.user_factors
#         item_factors = self.als_model.item_factors
        
#         # Calculate scores (dot product of user vector with item factors)
#         scores = user_vector @ user_factors @ item_factors.T
        
#         # Normalize scores to 0-1 range
#         return (scores - scores.min()) / (scores.max() - scores.min())

#     def _format_results(self, df):
#         """Select only relevant columns for the frontend and restore original values"""
#         columns_to_keep = [
#             'id', 'artist', 'track', 'album', 'genre',
#             'popularity', 'duration', 'tempo', 'year',
#             'mode', 'key', 'signature',
#             'acousticness', 'danceability', 'energy', 'valence',
#             'liveness', 'instrumentalness', 'speechiness', 'loudness',
#             'original_tempo', 'original_popularity', 'original_loudness', 'original_duration', 'similarity'
#         ]
        
#         # Add the original values for display columns
#         for col in self.display_columns:
#             if f'original_{col}' in df.columns:
#                 columns_to_keep.append(f'original_{col}')
#                 # Rename to original column name for frontend
#                 df = df.rename(columns={f'original_{col}': col})
        
#         return df[[col for col in columns_to_keep if col in df.columns]]
