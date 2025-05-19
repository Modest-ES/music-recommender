# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from models.recommender import MusicRecommender
# from models.search import MusicSearcher
# from models.song_manager import SongManager
# import pandas as pd
# import os
# import sqlite3
# from contextlib import closing

# app = Flask(__name__)
# CORS(app, resources={
#     r"/api/*": {
#         "origins": [
#             "http://localhost:5173",    # Vite dev server
#             "http://127.0.0.1:5173",   # Vite dev alternative
#             "http://localhost",         # Docker frontend (port 80)
#             "http://127.0.0.1",        # Docker frontend alternative
#         ]
#     }
# })

# @app.route('/')
# def home():
#     return "Music Recommender API"

# ===============================================================================
# parquet data pathing

# Initialize the central DataFrame
# DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'songs_2m_parquet.parquet')
# central_df = pd.read_parquet(DATA_PATH)

# recommender = MusicRecommender(central_df)
# searcher = MusicSearcher(central_df)
# song_manager = SongManager(central_df)

# ===============================================================================
# sqlite data pathing

# DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'tracksdb.db')

# def get_db():
#     """Helper function to get database connection"""
#     return sqlite3.connect(DB_PATH)

# Initialize services with database connection
# recommender = MusicRecommender(DB_PATH)
# searcher = MusicSearcher(DB_PATH)
# song_manager = SongManager(DB_PATH)

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     with closing(get_db()) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT COUNT(*) FROM tracks")
#         count = cursor.fetchone()[0]
#     return jsonify({
#         "status": "healthy", 
#         "data_source": "SQLite",
#         "track_count": count
#     })

# =====================================================================
# the rest (online version)

# @app.route('/health')
# def health_check():
#     return jsonify({"status": "healthy"}), 200

# @app.route('/api/recommend/initial', methods=['POST'])
# def initial_recommend():
#     try:
#         data = request.json
#         # Get recommendations (your existing logic)
#         results = recommender.initial_recommendations(data)
                
#         return jsonify({
#             "tracks": results.head(25).to_dict('records'),  # Return top 25
#             "message": "Recommendations generated successfully"
#         })
        
#     except Exception as e:
#         print(f"Recommendation error: {str(e)}")
#         return jsonify({
#             "error": "Could not generate recommendations",
#             "details": str(e)
#         }), 500

# @app.route('/api/search', methods=['POST'])
# def search_tracks():
#     try:
#         data = request.json
#         query = data.get('query', '')
        
#         results = searcher.search(
#             query=query
#         )
        
#         return jsonify({
#             'results': results,
#             'message': 'Search completed successfully'
#         })
        
#     except Exception as e:
#         print(f"Search error: {str(e)}")
#         return jsonify({
#             "error": "Could not perform search",
#             "details": str(e)
#         }), 500

# @app.route('/api/songs', methods=['POST'])
# def add_song():
#     """
#     Add new song endpoint that uses the SongManager class
#     """
#     try:
#         song_data = request.json
#         result, status_code = song_manager.add_song(song_data)
#         return jsonify(result), status_code
#     except Exception as e:
#         print(f"Endpoint error: {str(e)}")
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# ============================================================================
# offline version

# import os
# import sys
# import webbrowser
# import threading
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from models.recommender import MusicRecommender
# from models.search import MusicSearcher
# from models.song_manager import SongManager
# import pandas as pd
# import sqlite3
# from contextlib import closing
# import mimetypes

# # Add this at the top with other imports
# mimetypes.add_type('application/javascript', '.js')
# mimetypes.add_type('text/css', '.css')

# # Determine if we're running in PyInstaller bundle
# def resource_path(relative_path):
#     """Get absolute path to resource, works for dev and for PyInstaller"""
#     if getattr(sys, 'frozen', False):
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # Create Flask app
# app = Flask(__name__, static_folder=None)
# CORS(app, resources={
#     r"/api/*": {
#         "origins": [
#             "http://localhost:5173",    # Vite dev server
#             "http://127.0.0.1:5173",   # Vite dev alternative
#             "http://localhost:5000",    # exex server
#             "http://127.0.0.1:5000",   # exe alternative
#             "http://localhost",         # Docker frontend (port 80)
#             "http://127.0.0.1",        # Docker frontend alternative
#         ]
#     }
# })

# # Initialize the central DataFrame
# DATA_PATH = resource_path(os.path.join('data', 'songs_2m_parquet.parquet'))
# central_df = pd.read_parquet(DATA_PATH)

# # Initialize components
# recommender = MusicRecommender(central_df)
# searcher = MusicSearcher(central_df)
# song_manager = SongManager(central_df)

# # Frontend routes
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     static_folder = app.static_folder or resource_path('static')
    
#     if path.startswith('api/'):
#         return jsonify({"error": "API route not found"}), 404
    
#     # Serve static files with proper MIME types
#     if path and os.path.exists(os.path.join(static_folder, path)):
#         # Set correct MIME type based on file extension
#         if path.endswith('.js'):
#             mimetype = 'application/javascript'
#         elif path.endswith('.css'):
#             mimetype = 'text/css'
#         else:
#             mimetype = None
            
#         return send_from_directory(static_folder, path, mimetype=mimetype)
    
#     if os.path.exists(os.path.join(static_folder, 'index.html')):
#         return send_from_directory(static_folder, 'index.html')
    
#     return "Frontend files not found", 404

# # API endpoints
# @app.route('/health')
# def health_check():
#     return jsonify({"status": "healthy"}), 200

# @app.route('/api/recommend/initial', methods=['POST'])
# def initial_recommend():
#     try:
#         data = request.json
#         results = recommender.initial_recommendations(data)
#         return jsonify({
#             "tracks": results.head(25).to_dict('records'),
#             "message": "Recommendations generated successfully"
#         })
#     except Exception as e:
#         print(f"Recommendation error: {str(e)}")
#         return jsonify({
#             "error": "Could not generate recommendations",
#             "details": str(e)
#         }), 500

# @app.route('/api/search', methods=['POST'])
# def search_tracks():
#     try:
#         data = request.json
#         query = data.get('query', '')
#         results = searcher.search(query=query)
#         return jsonify({
#             'results': results,
#             'message': 'Search completed successfully'
#         })
#     except Exception as e:
#         print(f"Search error: {str(e)}")
#         return jsonify({
#             "error": "Could not perform search",
#             "details": str(e)
#         }), 500

# @app.route('/api/songs', methods=['POST'])
# def add_song():
#     try:
#         song_data = request.json
#         result, status_code = song_manager.add_song(song_data)
#         return jsonify(result), status_code
#     except Exception as e:
#         print(f"Endpoint error: {str(e)}")
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500

# def open_browser():
#     webbrowser.open_new('http://localhost:5000/')

# if __name__ == '__main__':
#     # Set static folder path
#     app.static_folder = resource_path('static')
    
#     # Print debug info
#     print(f"Static folder: {app.static_folder}")
#     if os.path.exists(app.static_folder):
#         print(f"Static files: {os.listdir(app.static_folder)}")
    
#     # Start browser
#     threading.Timer(1, open_browser).start()
    
#     # Run app
#     app.run(
#         host='0.0.0.0',
#         port=5000,
#         threaded=True,
#         debug=False
#     )
# ==================================================================
# sqlite offline

import os
import sys
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.recommender import MusicRecommender
from models.search import MusicSearcher
from models.song_manager import SongManager
import pandas as pd
import sqlite3
from contextlib import closing
import mimetypes

# Add MIME types
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

def resource_path(relative_path):
    """Get absolute path to resource"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Create Flask app
app = Flask(__name__, static_folder=None)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5000", 
            "http://127.0.0.1:5000",
            "http://localhost",
            "http://127.0.0.1",
        ]
    }
})

def load_data_from_db():
    """Load data from SQLite database"""
    db_path = resource_path(os.path.join('data', 'tracksdb.db'))
    print("path")
    print(db_path)
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM songs"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Initialize components
try:
    print("Loading data from SQLite...")
    central_df = load_data_from_db()
    db_path = resource_path(os.path.join('data', 'tracksdb.db'))
    print("Initializing recommender components...")
    recommender = MusicRecommender(central_df)
    searcher = MusicSearcher(db_path)
    song_manager = SongManager(db_path)
except Exception as e:
    print(f"Initialization error: {str(e)}")
    class DummyComponent:
        def __getattr__(self, name):
            return lambda *args, **kwargs: {"error": "Initialization failed"}
    recommender = searcher = song_manager = DummyComponent()

# Frontend routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder = app.static_folder or resource_path('static')
    
    if path.startswith('api/'):
        return jsonify({"error": "API route not found"}), 404
    
    if path and os.path.exists(os.path.join(static_folder, path)):
        mimetype = None
        if path.endswith('.js'):
            mimetype = 'application/javascript'
        elif path.endswith('.css'):
            mimetype = 'text/css'
        return send_from_directory(static_folder, path, mimetype=mimetype)
    
    if os.path.exists(os.path.join(static_folder, 'index.html')):
        return send_from_directory(static_folder, 'index.html')
    
    return "Frontend files not found", 404

# API endpoints (remain the same as before)
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/recommend/initial', methods=['POST'])
def initial_recommend():
    try:
        data = request.json
        results = recommender.initial_recommendations(data)
        return jsonify({
            "tracks": results.head(25).to_dict('records'),
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
        results = searcher.search(query=query)
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
    try:
        song_data = request.json
        result, status_code = song_manager.add_song(song_data)
        # Update search index with new song
        if status_code == 200:  # Only if add was successful
            searcher.update_index_with_new_song(song_data)
        print("res song in app py")
        print(result)
        return jsonify(result), status_code
    except Exception as e:
        print(f"Endpoint error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

def open_browser():
    webbrowser.open_new('http://localhost:5000/')

if __name__ == '__main__':
    app.static_folder = resource_path('static')
    print(f"Static folder: {app.static_folder}")
    if os.path.exists(app.static_folder):
        print(f"Static files: {os.listdir(app.static_folder)}")
    
    threading.Timer(1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)