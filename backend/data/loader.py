import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data():
    df = pd.read_parquet('data/songs_2m_parquet.parquet')
    
    # Normalization
    scaler = MinMaxScaler()
    numerical_features = ['tempo', 'loudness', 'duration', 'popularity', 
                         'acousticness', 'danceability', 'energy', 
                         'valence', 'liveness', 'speechiness', 'instrumentalness']
    df[numerical_features] = scaler.fit_transform(df[numerical_features])
    
    return df