import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 60000,
});

const getLikedTracks = () => {
  return JSON.parse(localStorage.getItem('musicRecommender_liked') || '[]');
};

const getDislikedTracks = () => {
  return JSON.parse(localStorage.getItem('musicRecommender_disliked') || '[]');
};

export const getInitialRecommendations = (preferences) => {
  const likedTracks = getLikedTracks();
  const dislikedTracks = getDislikedTracks();

  return api.post('/recommend/initial', {
    ...preferences,
    liked_tracks: likedTracks,
    disliked_tracks: dislikedTracks,
    exclude_ids: likedTracks.concat(dislikedTracks).map((track) => track.id),
  });
};

export const searchTracks = (query) => {
  const likedTracks = getLikedTracks();
  const dislikedTracks = getDislikedTracks();

  return api.post('/search', {
    query,
    liked_tracks: likedTracks,
    disliked_tracks: dislikedTracks,
    exclude_ids: likedTracks.concat(dislikedTracks).map((track) => track.id),
  });
};

export const addSong = (songData) => {
  return api.post('/songs', {
    ...songData,
  });
};

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  },
);
