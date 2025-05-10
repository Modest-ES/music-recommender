from flask import Flask, request, jsonify
from flask_cors import CORS
from models.recommender import MusicRecommender
from models.search import MusicSearcher
from models.song_manager import SongManager
import pandas as pd
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
    }
})

@app.route('/')
def home():
    return "Music Recommender API"

# Initialize the central DataFrame
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'songs_2m_parquet.parquet')
central_df = pd.read_parquet(DATA_PATH)

recommender = MusicRecommender(central_df)
searcher = MusicSearcher(central_df)
song_manager = SongManager(central_df)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "data_source": os.path.basename(DATA_PATH)})

@app.route('/api/recommend/initial', methods=['POST'])
def initial_recommend():
    try:
        data = request.json
        # Get recommendations (your existing logic)
        results = recommender.initial_recommendations(data)
                
        return jsonify({
            "tracks": results.head(25).to_dict('records'),  # Return top 25
            "message": "Recommendations generated successfully"
        })
        
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        return jsonify({
            "error": "Could not generate recommendations",
            "details": str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search_tracks():
    try:
        data = request.json
        query = data.get('query', '')
        
        results = searcher.search(
            query=query
        )
        
        return jsonify({
            'results': results,
            'message': 'Search completed successfully'
        })
        
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({
            "error": "Could not perform search",
            "details": str(e)
        }), 500

@app.route('/api/songs', methods=['POST'])
def add_song():
    """
    Add new song endpoint that uses the SongManager class
    """
    try:
        song_data = request.json
        result, status_code = song_manager.add_song(song_data)
        return jsonify(result), status_code
    except Exception as e:
        print(f"Endpoint error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)