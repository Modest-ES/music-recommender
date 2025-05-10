import { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Slider,
  Typography,
  Paper,
  CircularProgress,
  ToggleButton,
  ToggleButtonGroup,
  Divider,
  Chip
} from '@mui/material';

export default function RefinementControls({
  initialPrefs,
  currentTracks,
  onSubmit,
  onCancel,
  loading
}) {
  // Convert current track features to average values for initial refinement values
  const getAverages = () => {
    if (!currentTracks || currentTracks.length === 0) return {};
    
    const features = [
      'acousticness', 'danceability', 'energy', 'instrumentalness',
      'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
      'popularity'
    ];
    
    const averages = {};
    features.forEach(feature => {
      const validValues = currentTracks
        .map(track => track[feature])
        .filter(val => val !== undefined);
      
      if (validValues.length > 0) {
        averages[feature] = validValues.reduce((a, b) => a + b, 0) / validValues.length;
      }
    });
    
    return averages;
  };

  // Convert dataset values to 0-100 scale for sliders
  const scaleToSlider = (value, min, max) => {
    return ((value - min) / (max - min)) * 100;
  };

  // Initialize state with averaged values from current recommendations
  const [adjustments, setAdjustments] = useState(() => {
    const avgFeatures = getAverages();
    return {
      // Audio features
      popularity: scaleToSlider(avgFeatures.popularity || 50, 0, 100),
      loudness: scaleToSlider(avgFeatures.loudness || -20, -60, 0),
      acousticness: scaleToSlider(avgFeatures.acousticness || 0.5, 0, 1),
      danceability: scaleToSlider(avgFeatures.danceability || 0.5, 0, 1),
      energy: scaleToSlider(avgFeatures.energy || 0.5, 0, 1),
      liveness: scaleToSlider(avgFeatures.liveness || 0.5, 0, 1),
      instrumentalness: scaleToSlider(avgFeatures.instrumentalness || 0.5, 0, 1),
      speechiness: scaleToSlider(avgFeatures.speechiness || 0.5, 0, 1),
      valence: scaleToSlider(avgFeatures.valence || 0.5, 0, 1),
      
      // Ranges
      tempoRange: [
        Math.min(...currentTracks.map(t => t.tempo)) || 90,
        Math.max(...currentTracks.map(t => t.tempo)) || 120
      ],
      
      // Musical attributes
      selectedKeys: [],
      selectedModes: [],
      selectedSignatures: [],
      
      // Keep original genre preferences
      selectedGenres: initialPrefs.selectedGenres || []
    };
  });

  const keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const modes = ['Major', 'Minor'];
  const signatures = ['1/4', '3/4', '4/4', '5/4'];

  const handleSliderChange = (key) => (e, value) => {
    setAdjustments({...adjustments, [key]: value});
  };

  const handleRangeChange = (key) => (e, newValue) => {
    setAdjustments({...adjustments, [key]: newValue});
  };

  const handleAttributeToggle = (attribute, value) => {
    setAdjustments(prev => ({
      ...prev,
      [attribute]: prev[attribute].includes(value)
        ? prev[attribute].filter(item => item !== value)
        : [...prev[attribute], value]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert slider values back to dataset ranges
    const scaledAdjustments = {
      // Audio features
      popularity: (adjustments.popularity / 100) * 100, // 0-100
      loudness: -60 + (adjustments.loudness / 100) * 60, // -60 to 0 dB
      acousticness: adjustments.acousticness / 100,
      danceability: adjustments.danceability / 100,
      energy: adjustments.energy / 100,
      liveness: adjustments.liveness / 100,
      instrumentalness: adjustments.instrumentalness / 100,
      speechiness: adjustments.speechiness / 100,
      valence: adjustments.valence / 100,
      
      // Ranges
      tempo_min: adjustments.tempoRange[0],
      tempo_max: adjustments.tempoRange[1],
      
      // Musical attributes
      ...(adjustments.selectedKeys.length > 0 && { key: adjustments.selectedKeys }),
      ...(adjustments.selectedModes.length > 0 && { mode: adjustments.selectedModes }),
      ...(adjustments.selectedSignatures.length > 0 && { signature: adjustments.selectedSignatures }),
      
      // Preserve original genre preferences
      ...Object.fromEntries(
        adjustments.selectedGenres.map(g => [`genre_${g.toLowerCase()}`, 1])
      )
    };
    
    onSubmit(scaledAdjustments);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        Refine Your Recommendations
      </Typography>
      
      <Typography variant="subtitle1" gutterBottom>
        Based on your current recommendations, adjust these parameters:
      </Typography>

      {/* Audio Feature Sliders */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
          Audio Features
        </Typography>
        <Divider sx={{ mb: 2 }} />
        
        {[
          { name: 'popularity', label: 'Popularity', value: adjustments.popularity.toFixed(0), min: 0, max: 100 },
          { name: 'loudness', label: 'Loudness (dB)', value: (-60 + (adjustments.loudness / 100) * 60).toFixed(1), min: 0, max: 100 },
          { name: 'acousticness', label: 'Acousticness', value: (adjustments.acousticness / 100).toFixed(2), min: 0, max: 100 },
          { name: 'danceability', label: 'Danceability', value: (adjustments.danceability / 100).toFixed(2), min: 0, max: 100 },
          { name: 'energy', label: 'Energy', value: (adjustments.energy / 100).toFixed(2), min: 0, max: 100 },
          { name: 'liveness', label: 'Liveness', value: (adjustments.liveness / 100).toFixed(2), min: 0, max: 100 },
          { name: 'instrumentalness', label: 'Instrumentalness', value: (adjustments.instrumentalness / 100).toFixed(2), min: 0, max: 100 },
          { name: 'speechiness', label: 'Speechiness', value: (adjustments.speechiness / 100).toFixed(2), min: 0, max: 100 },
          { name: 'valence', label: 'Valence (Positivity)', value: (adjustments.valence / 100).toFixed(2), min: 0, max: 100 }
        ].map(({ name, label, value, min, max }) => (
          <Box key={name} sx={{ mb: 3 }}>
            <Typography gutterBottom>
              {label}: <strong>{value}</strong>
            </Typography>
            <Slider
              value={adjustments[name]}
              onChange={handleSliderChange(name)}
              min={min}
              max={max}
              valueLabelDisplay="auto"
            />
          </Box>
        ))}
      </Box>

      {/* Tempo Range */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Tempo Range: {adjustments.tempoRange[0].toFixed(0)} - {adjustments.tempoRange[1].toFixed(0)} BPM
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Slider
          value={adjustments.tempoRange}
          onChange={handleRangeChange('tempoRange')}
          min={60}
          max={250}
          valueLabelDisplay="auto"
        />
      </Box>

      {/* Musical Attributes */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Musical Attributes
        </Typography>
        <Divider sx={{ mb: 2 }} />
        
        {/* Key */}
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 1 }}>
          Key
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          {keys.map((key) => (
            <Chip
              key={key}
              label={key}
              clickable
              color={adjustments.selectedKeys.includes(key) ? 'primary' : 'default'}
              onClick={() => handleAttributeToggle('selectedKeys', key)}
            />
          ))}
          <Chip
            label="No Preference"
            clickable
            color={adjustments.selectedKeys.length === 0 ? 'primary' : 'default'}
            onClick={() => setAdjustments({...adjustments, selectedKeys: []})}
          />
        </Box>

        {/* Mode */}
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Mode
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          {modes.map((mode) => (
            <Chip
              key={mode}
              label={mode}
              clickable
              color={adjustments.selectedModes.includes(mode) ? 'primary' : 'default'}
              onClick={() => handleAttributeToggle('selectedModes', mode)}
            />
          ))}
          <Chip
            label="No Preference"
            clickable
            color={adjustments.selectedModes.length === 0 ? 'primary' : 'default'}
            onClick={() => setAdjustments({...adjustments, selectedModes: []})}
          />
        </Box>

        {/* Time Signature */}
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Time Signature
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          {signatures.map((sig) => (
            <Chip
              key={sig}
              label={sig}
              clickable
              color={adjustments.selectedSignatures.includes(sig) ? 'primary' : 'default'}
              onClick={() => handleAttributeToggle('selectedSignatures', sig)}
            />
          ))}
          <Chip
            label="No Preference"
            clickable
            color={adjustments.selectedSignatures.length === 0 ? 'primary' : 'default'}
            onClick={() => setAdjustments({...adjustments, selectedSignatures: []})}
          />
        </Box>
      </Box>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="outlined"
          onClick={onCancel}
          disabled={loading}
          sx={{ width: '48%' }}
        >
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading}
          sx={{ width: '48%' }}
        >
          {loading ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            'Apply Refinements'
          )}
        </Button>
      </Box>
    </Paper>
  );
}