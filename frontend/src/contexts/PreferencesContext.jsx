// contexts/PreferencesContext.jsx
import { createContext, useState, useEffect, useContext } from 'react';

const defaultPreferences = {
  likedGenreInfluence: 5,
  dislikedGenreInfluence: 5, 
  likedArtistInfluence: 5,
  dislikedArtistInfluence: 5,
  selectedGenres: [],
  genreStrictness: 5,
  yearRange: [1900, 2025],
  yearStrictness: 5,
  tempoRange: [90, 150],
  tempoStrictness: 5,
  duration: [150, 210],
  durationStrictness: 5,
  selectedKeys: [],
  selectedModes: [],
  selectedSignatures: [],
  popularity: 50,
  loudness: 50,
  acousticness: 50,
  danceability: 50,
  energy: 50,
  liveness: 50,
  instrumentalness: 50,
  speechiness: 50,
  valence: 50
};

const validatePreferences = (savedPrefs) => {
  // If no saved preferences or invalid format, return defaults
  if (!savedPrefs || typeof savedPrefs !== 'object') {
    return defaultPreferences;
  }

  // Create a new object with default values
  const validatedPrefs = { ...defaultPreferences };

  // Only copy properties that exist in defaults and have the correct type
  Object.keys(defaultPreferences).forEach(key => {
    if (key in savedPrefs) {
      // Validate array fields
      if (Array.isArray(defaultPreferences[key])) {
        if (Array.isArray(savedPrefs[key])) {
          validatedPrefs[key] = savedPrefs[key];
        }
      } 
      // Validate number fields
      else if (typeof defaultPreferences[key] === 'number') {
        if (typeof savedPrefs[key] === 'number') {
          validatedPrefs[key] = savedPrefs[key];
        }
      }
      // Validate null fields
      else if (defaultPreferences[key] === null) {
        if (savedPrefs[key] === null) {
          validatedPrefs[key] = null;
        }
      }
    }
  });

  return validatedPrefs;
};

const PreferencesContext = createContext();

export const PreferencesProvider = ({ children }) => {
  const [preferences, setPreferences] = useState(defaultPreferences);

  useEffect(() => {
    // Load and validate preferences on initial mount
    try {
      const saved = localStorage.getItem('musicRecommender_preferences');
      const parsed = saved ? JSON.parse(saved) : null;
      const validated = validatePreferences(parsed);
      
      setPreferences(validated);
      // Save validated version back to localStorage
      localStorage.setItem('musicRecommender_preferences', JSON.stringify(validated));
    } catch (error) {
      console.error('Error loading preferences:', error);
      // Reset to defaults if error occurs
      localStorage.setItem('musicRecommender_preferences', JSON.stringify(defaultPreferences));
    }
  }, []);

  const updatePreferences = (newPreferences) => {
    const validated = validatePreferences(newPreferences);
    setPreferences(validated);
    localStorage.setItem('musicRecommender_preferences', JSON.stringify(validated));
  };

  const resetPreferences = () => {
    setPreferences(defaultPreferences);
    localStorage.setItem('musicRecommender_preferences', JSON.stringify(defaultPreferences));
  };

  return (
    <PreferencesContext.Provider value={{ preferences, updatePreferences, resetPreferences }}>
      {children}
    </PreferencesContext.Provider>
  );
};

export const usePreferences = () => useContext(PreferencesContext);