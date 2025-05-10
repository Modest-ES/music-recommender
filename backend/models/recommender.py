import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

class MusicRecommender:
    def __init__(self, outer_dataframe):
        self.df = outer_dataframe
        # Define which columns need to keep original values
        self.display_columns = ['loudness', 'tempo', 'popularity', 'duration']
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
            self.df['genre'] = self.df['genre'].fillna('Unknown')
            self.genre_dummies = pd.get_dummies(self.df['genre'], prefix='genre')
        
    def _fit_models(self):
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

    def initial_recommendations(self, user_prefs):
        try:
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

            # Get genre strictness (default to 5 if not specified)
            genre_strictness = user_prefs['genre_strictness']
            genre_penalty = 0.07 * genre_strictness  # 0.07 to 0.7 based on strictness

            # Apply genre multiplier (but don't filter)
            if 'genre_strictness' in user_prefs:
                selected_genres = [key[6:] for key in user_prefs if key.startswith('genre_')]
                def genre_multiplier(genre):
                    if genre in selected_genres:
                        return 1.0
                    return max(0.1, 1.0 - genre_penalty)  # Minimum multiplier of 0.1
                results['genre_multiplier'] = results['genre'].apply(genre_multiplier)
                results['similarity'] = results['similarity'] * results['genre_multiplier']

            # Calculate influence multipliers
            liked_genre_influence = 1.0 + (0.02 * user_prefs.get('liked_genre_influence', 5))
            disliked_genre_influence = 1.0 - (0.01 * user_prefs.get('disliked_genre_influence', 5))
            liked_artist_influence = 1.0 + (0.02 * user_prefs.get('liked_artist_influence', 5))
            disliked_artist_influence = 1.0 - (0.01 * user_prefs.get('disliked_artist_influence', 5))
            
            # Get liked/disliked genres and artists
            liked_genres = set(track['genre'] for track in user_prefs.get('liked_tracks', []) if 'genre' in track)
            disliked_genres = set(track['genre'] for track in user_prefs.get('disliked_tracks', []) if 'genre' in track)
            liked_artists = set(track['artist'] for track in user_prefs.get('liked_tracks', []) if 'artist' in track)
            disliked_artists = set(track['artist'] for track in user_prefs.get('disliked_tracks', []) if 'artist' in track)
            
            # Apply genre multipliers
            def playlists_genre_multiplier(genre):
                if genre in liked_genres:
                    return liked_genre_influence
                elif genre in disliked_genres:
                    return disliked_genre_influence
                return 1.0
            
            results['playlists_genre_multiplier'] = results['genre'].apply(playlists_genre_multiplier)
            
            # Apply artist multipliers
            def artist_multiplier(artist):
                if artist in liked_artists:
                    return liked_artist_influence
                elif artist in disliked_artists:
                    return disliked_artist_influence
                return 1.0
            
            results['artist_multiplier'] = results['artist'].apply(artist_multiplier)
            
            # Calculate final similarity
            results['similarity'] = (
                results['similarity'] * 
                results['playlists_genre_multiplier'] * 
                results['artist_multiplier']
            )

            if all(k in user_prefs for k in ['year_min', 'year_max', 'year_strictness']):
                year_min = user_prefs['year_min']
                year_max = user_prefs['year_max']
                year_strictness = user_prefs['year_strictness']
                penalty_rate = 0.01 * year_strictness  # 0.01 to 0.1 based on strictness
                
                def year_multiplier(year):
                    if year_min <= year <= year_max:
                        return 1.0
                    elif year < year_min:
                        distance = year_min - year
                    else:
                        distance = year - year_max
                    
                    multiplier = max(0.1, 1.0 - (distance * penalty_rate))
                    return multiplier
                
                results['year_multiplier'] = results['year'].apply(year_multiplier)
                results['similarity'] = results['similarity'] * results['year_multiplier']

            if all(k in user_prefs for k in ['tempo_min', 'tempo_max', 'tempo_strictness']):
                tempo_min = user_prefs['tempo_min']
                tempo_max = user_prefs['tempo_max']
                tempo_strictness = user_prefs['tempo_strictness']
                penalty_rate = 0.01 * tempo_strictness
                
                def tempo_multiplier(tempo):
                    if tempo_min <= tempo <= tempo_max:
                        return 1.0
                    elif tempo < tempo_min:
                        distance = tempo_min - tempo
                    else:
                        distance = tempo - tempo_max
                    
                    multiplier = max(0.1, 1.0 - (distance * penalty_rate))
                    return multiplier
                
                results['tempo_multiplier'] = results['original_tempo'].apply(tempo_multiplier)
                results['similarity'] = results['similarity'] * results['tempo_multiplier']

            if all(k in user_prefs for k in ['duration_min', 'duration_max', 'duration_strictness']):
                duration_min = user_prefs['duration_min']
                duration_max = user_prefs['duration_max']
                duration_strictness = user_prefs['duration_strictness']
                penalty_rate = 0.01 * duration_strictness
                
                def duration_multiplier(duration):
                    if duration_min <= duration <= duration_max:
                        return 1.0
                    elif duration < duration_min:
                        distance = duration_min - duration
                    else:
                        distance = duration - duration_max
                    
                    multiplier = max(0.1, 1.0 - (distance * penalty_rate))
                    return multiplier
                
                results['duration_multiplier'] = results['original_duration'].apply(duration_multiplier)
                results['similarity'] = results['similarity'] * results['duration_multiplier']

            return self._format_results(
                results.sort_values('similarity', ascending=False).head(20)
            )
        
        except Exception as e:
            print(f"Recommendation error: {str(e)}")
            # Return some results even if error occurs
            return self._format_results(self.df.sample(min(10, len(self.df))))

    def refined_recommendations(self, initial_tracks, adjustments):
        """Refine recommendations based on user feedback"""
        # Get indices of initial tracks
        track_ids = [t['track_id'] for t in initial_tracks if 'track_id' in t]
        if not track_ids:
            return self.initial_recommendations(adjustments)
            
        # Get features of liked tracks
        liked_features = self.content_features.loc[
            self.df['track_id'].isin(track_ids)
        ].mean(axis=0)
        
        # Apply user adjustments
        for feature, adjustment in adjustments.items():
            if feature in liked_features.index:
                liked_features[feature] = adjustment
                
        # Find similar tracks to adjusted preferences
        distances, indices = self.item_item_model.kneighbors([liked_features])
        
        # Exclude already recommended tracks
        new_indices = [i for i in indices[0] if i not in track_ids][:10]
        results = self.df.iloc[new_indices]
        return self._format_results(results)

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