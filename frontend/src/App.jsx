import { useState, useEffect } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme, Button, Box } from '@mui/material';
import PreferenceForm from './components/PreferenceForm';
import Recommendations from './components/Recommendations';
import Playlists from './components/Playlists';
import Header from './components/Header';
import { getInitialRecommendations, searchTracks, addSong } from './api';
import { PreferencesProvider } from './contexts/PreferencesContext';
import SearchResults from './components/SearchResults';
import AddSong from './components/AddSong';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#1db954' },
    background: { default: '#121212', paper: '#181818' },
  },
});

// Local storage keys
const STORAGE_KEYS = {
  PREFERENCES: 'musicRecommender_preferences',
  LIKED: 'musicRecommender_liked',
  DISLIKED: 'musicRecommender_disliked'
};

export default function App() {
  const [step, setStep] = useState('form');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('recommendations');
  const [preferences, setPreferences] = useState(() => {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.PREFERENCES)) || {};
  });
  const [likedTracks, setLikedTracks] = useState(() => {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.LIKED)) || [];
  });
  const [dislikedTracks, setDislikedTracks] = useState(() => {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.DISLIKED)) || [];
  });
  const [searchResults, setSearchResults] = useState([]);
  const [searchMode, setSearchMode] = useState(false);
  const [showAddSong, setShowAddSong] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Save to localStorage whenever state changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.PREFERENCES, JSON.stringify(preferences));
  }, [preferences]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.LIKED, JSON.stringify(likedTracks));
  }, [likedTracks]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.DISLIKED, JSON.stringify(dislikedTracks));
  }, [dislikedTracks]);

  const handleSearch = async (query) => {
    setIsSearchLoading(true);
    try {
      const response = await searchTracks(query);
      setSearchResults(response.data.results);
      setSearchMode(true);
      setActiveTab('recommendations');
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearchLoading(false);
    }
  };

  const handleAddSong = async (songData) => {
    setLoading(true);
    try {
      const response = await addSong(songData);
      setSnackbarMessage(`Song: ${songData.artist} - ${songData.track} was successfully added`);
      setSnackbarOpen(true);
      return response.data;
    } catch (error) {
      setSnackbarMessage('Failed to add song. Please try again.');
      setSnackbarOpen(true);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitPreferences = async (prefs) => {
    setLoading(true);
    try {
      const newPreferences = { ...prefs, lastUpdated: Date.now() };
      setPreferences(newPreferences);
      const response = await getInitialRecommendations({
        ...newPreferences
      });
      setRecommendations(response.data.tracks);
      setStep('results');
      setActiveTab('recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleTrackAction = (track, action, notDuplicated) => {
    if (action === 'like' && notDuplicated) {
      setLikedTracks(prev => [...prev, track]);
    } else if (action === 'dislike' && notDuplicated) {
      setDislikedTracks(prev => [...prev, track]);
    }
  };

  const resetUserData = () => {
    if (window.confirm('Are you sure you want to reset all your preferences and playlists?')) {
      localStorage.removeItem(STORAGE_KEYS.PREFERENCES);
      localStorage.removeItem(STORAGE_KEYS.LIKED);
      localStorage.removeItem(STORAGE_KEYS.DISLIKED);
      setPreferences({});
      setLikedTracks([]);
      setDislikedTracks([]);
      setStep('form');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <PreferencesProvider>
        <CssBaseline />
        <Header 
          onReset={resetUserData} 
          onSearch={handleSearch} 
        />
        
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            <Button
              variant={activeTab === 'recommendations' && !showAddSong ? 'contained' : 'outlined'}
              onClick={() => {
                setActiveTab('recommendations');
                setShowAddSong(false);
              }}
            >
              Recommendations
            </Button>
            <Button
              variant={activeTab === 'playlists' ? 'contained' : 'outlined'}
              onClick={() => {
                setActiveTab('playlists');
                setShowAddSong(false);
              }}
            >
              My Playlists
            </Button>
            <Button
              variant={showAddSong ? 'contained' : 'outlined'}
              onClick={() => {
                setShowAddSong(true);
                setActiveTab('recommendations');
              }}
            >
              Add New Song
            </Button>
          </Box>

      {activeTab === 'recommendations' ? (
        showAddSong ? (
          <AddSong onAddSong={handleAddSong} />
        ) : searchMode ? (
          <SearchResults 
            results={searchResults}
            onAction={handleTrackAction}
            likedIds={likedTracks.map(t => t.id)}
            dislikedIds={dislikedTracks.map(t => t.id)}
            onBack={() => setSearchMode(false)}
          />
        ) : step === 'form' ? (
          <PreferenceForm 
            initialValues={preferences}
            onSubmit={handleSubmitPreferences} 
            loading={loading}
          />
        ) : (
          <Recommendations 
            tracks={recommendations} 
            onAction={handleTrackAction}
            likedIds={likedTracks.map(t => t.id)}
            dislikedIds={dislikedTracks.map(t => t.id)}
            onBack={() => setStep('form')}
          />
        )
      ) : (
        <Playlists 
          likedTracks={likedTracks}
          dislikedTracks={dislikedTracks}
          onRemove={(track, list) => {
            if (list === 'liked') {
              setLikedTracks(prev => prev.filter(t => t.id !== track.id));
            } else {
              setDislikedTracks(prev => prev.filter(t => t.id !== track.id));
            }
          }}
        />
      )}
      </Container>
      </PreferencesProvider>
    </ThemeProvider>
  );
}