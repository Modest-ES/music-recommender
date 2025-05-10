import { useState, useEffect } from 'react';
import { 
  Button, Box, Typography, Slider, Chip, Divider,
  ToggleButton, ToggleButtonGroup, Tooltip, CircularProgress
} from '@mui/material';
import { usePreferences } from '../contexts/PreferencesContext';

const genres = [
  'rock', 'pop', 'electronic', 'classical', 'soundtrack', 
  'hip-hop', 'instrumental', 'world', 'jazz', 'singer-songwriter', 
  'house', 'reggae', 'dance', 'blues', 'folk', 
  'country', 'latin', 'opera', 'ambient', 'disco',
  'religious', 'comedy', 'soul', 'ska', 'funk', 
  'emo', 'samba', 'hardcore', 'indie', 'garage', 
  'industrial', 'goth', 'salsa', 'children', 'tango',
  'rnb', 'trip-hop', 'romance', 'standards', 'miscellaneous', 
  'historic', 'vocal', 'lounge', 'cabaret', 'experimental'
];

const durationOptions = [
  { label: 'Короткие (<2.5 мин)', value: [0, 150] },
  { label: 'Средне-короткие (2.5-3.5 мин)', value: [150, 210] },
  { label: 'Средне-длинные (3.5-5 мин)', value: [210, 300] },
  { label: 'Длинные (>5 мин)', value: [300, 1200] }
];

const keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const modes = ['Major', 'Minor'];
const signatures = ['1/4', '3/4', '4/4', '5/4'];

export default function PreferenceForm({ onSubmit, loading }) {
  const { preferences, updatePreferences } = usePreferences();
  const [localPrefs, setLocalPrefs] = useState(preferences);

  // Convert 0-100 slider values to dataset ranges
  const scaleToRange = (value, min, max) => {
    return min + (value / 100) * (max - min);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submission = {
      // Genre and strictness
      ...Object.fromEntries(
        localPrefs.selectedGenres.map(g => [`genre_${g.toLowerCase()}`, 1])
      ),
      genre_strictness: localPrefs.genreStrictness,

      liked_genre_influence: localPrefs.likedGenreInfluence,
      disliked_genre_influence: localPrefs.dislikedGenreInfluence,
      liked_artist_influence: localPrefs.likedArtistInfluence,
      disliked_artist_influence: localPrefs.dislikedArtistInfluence,
      
      // Year range and strictness
      year_min: localPrefs.yearRange[0],
      year_max: localPrefs.yearRange[1],
      year_strictness: localPrefs.yearStrictness,
      
      // Tempo range and strictness
      tempo_min: localPrefs.tempoRange[0],
      tempo_max: localPrefs.tempoRange[1],
      tempo_strictness: localPrefs.tempoStrictness,
      
      // Duration and strictness
      ...(localPrefs.duration && {
        duration_min: localPrefs.duration[0],
        duration_max: localPrefs.duration[1]
      }),
      duration_strictness: localPrefs.durationStrictness,
      
      // Key
      ...(localPrefs.selectedKeys.length > 0 && {
        key: localPrefs.selectedKeys
      }),
      
      // Mode
      ...(localPrefs.selectedModes.length > 0 && {
        mode: localPrefs.selectedModes
      }),
      
      // Signature
      ...(localPrefs.selectedSignatures.length > 0 && {
        signature: localPrefs.selectedSignatures
      }),
      
      // Audio features (scaled to dataset ranges)
      popularity: scaleToRange(localPrefs.popularity, 0, 100),
      loudness: scaleToRange(localPrefs.loudness, -60, 0),
      acousticness: scaleToRange(localPrefs.acousticness, 0, 1),
      danceability: scaleToRange(localPrefs.danceability, 0, 1),
      energy: scaleToRange(localPrefs.energy, 0, 1),
      liveness: scaleToRange(localPrefs.liveness, 0, 1),
      instrumentalness: scaleToRange(localPrefs.instrumentalness, 0, 1),
      speechiness: scaleToRange(localPrefs.speechiness, 0, 1),
      valence: scaleToRange(localPrefs.valence, 0, 1)
    };
    
    updatePreferences(localPrefs);
    onSubmit(submission);
  };

  useEffect(() => {
    setLocalPrefs(preferences);
  }, [preferences]);

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      {/* Genre Selection */}
      <Typography variant="h6" gutterBottom>Выберите жанры</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
        {genres.map((genre) => (
          <Chip
            key={genre}
            label={genre}
            clickable
            color={localPrefs.selectedGenres.includes(genre) ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({
              ...localPrefs,
              selectedGenres: localPrefs.selectedGenres.includes(genre)
                ? localPrefs.selectedGenres.filter(g => g !== genre)
                : [...localPrefs.selectedGenres, genre]
            })}
          />
        ))}
      </Box>
      {/* Genre Strictness */}
      <Typography variant="subtitle1" gutterBottom>
        Влияние жанра: {localPrefs.genreStrictness}
      </Typography>
      <Slider
        value={localPrefs.genreStrictness}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, genreStrictness: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      <Divider sx={{ my: 3 }} />

      {/* Liked Genre Influence */}

      <Typography variant="subtitle1" gutterBottom>
        Влияние понравившихся жанров: {localPrefs.likedGenreInfluence}
      </Typography>
      <Slider
        value={localPrefs.likedGenreInfluence}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, likedGenreInfluence: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />

      {/* Disliked Genre Influence */}

      <Typography variant="subtitle1" gutterBottom>
        Влияние не понравившихся жанров: {localPrefs.dislikedGenreInfluence}
      </Typography>
      <Slider
        value={localPrefs.dislikedGenreInfluence}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, dislikedGenreInfluence: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />

      {/* Liked Artist Influence */}

      <Typography variant="subtitle1" gutterBottom>
        Влияние понравившихся исполнителей: {localPrefs.likedArtistInfluence}
      </Typography>
      <Slider
        value={localPrefs.likedArtistInfluence}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, likedArtistInfluence: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />

      {/* Disliked Artist Influence */}

      <Typography variant="subtitle1" gutterBottom>
        Влияние не понравившихся исполнителей: {localPrefs.dislikedArtistInfluence}
      </Typography>
      <Slider
        value={localPrefs.dislikedArtistInfluence}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, dislikedArtistInfluence: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      <Divider sx={{ my: 3 }} />

      {/* Year Range */}
      <Typography variant="h6" gutterBottom>
        Год выпуска трека: {localPrefs.yearRange[0]} - {localPrefs.yearRange[1]}
      </Typography>
      <Slider
        value={localPrefs.yearRange}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, yearRange: newValue})}
        min={1900}
        max={2025}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      {/* Year Strictness */}
      <Typography variant="subtitle1" gutterBottom>
        Влияние года выпуска: {localPrefs.yearStrictness}
      </Typography>
      <Slider
        value={localPrefs.yearStrictness}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, yearStrictness: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      <Divider sx={{ my: 3 }} />

      {/* Tempo Range */}
      <Typography variant="h6" gutterBottom>
        Темп (ударов в минуту / BPM): {localPrefs.tempoRange[0]} - {localPrefs.tempoRange[1]}
      </Typography>
      <Slider
        value={localPrefs.tempoRange}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, tempoRange: newValue})}
        min={60}
        max={250}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      {/* Tempo strictness */}
      <Typography variant="subtitle1" gutterBottom>
        Влияние темпа: {localPrefs.tempoStrictness}
      </Typography>
      <Slider
        value={localPrefs.tempoStrictness}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, tempoStrictness: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      <Divider sx={{ my: 3 }} />

      {/* Duration */}
      <Typography variant="h6" gutterBottom>Длина трека</Typography>
      <ToggleButtonGroup
        value={localPrefs.duration}
        exclusive
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, duration: newValue})}
        sx={{ mb: 3 }}
      >
        {durationOptions.map((opt) => (
          <ToggleButton 
            key={opt.label} 
            value={opt.value}
            selected={JSON.stringify(localPrefs.duration) === JSON.stringify(opt.value)}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'primary.main',
                color: 'primary.contrastText',
                '&:hover': {
                  backgroundColor: 'primary.dark'
                }
              }
            }}
          >
            {opt.label}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
      {/* Duration Strictness */}
      <Typography variant="subtitle1" gutterBottom>
        Влияние длины трека: {localPrefs.durationStrictness}
      </Typography>
      <Slider
        value={localPrefs.durationStrictness}
        onChange={(e, newValue) => setLocalPrefs({...localPrefs, durationStrictness: newValue})}
        min={1}
        max={10}
        marks={[
          { value: 1, label: 'Слабое' },
          { value: 5, label: 'Среднее' },
          { value: 10, label: 'Сильное' }
        ]}
        valueLabelDisplay="auto"
        sx={{ mb: 3 }}
      />
      <Divider sx={{ my: 3 }} />

      {/* Key */}
      <Typography variant="h6" gutterBottom>Тональность (нота)</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
        {keys.map((key) => (
          <Chip
            key={key}
            label={key}
            clickable
            color={localPrefs.selectedKeys.includes(key) ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({
              ...localPrefs,
              selectedKeys: localPrefs.selectedKeys.includes(key)
                ? localPrefs.selectedKeys.filter(k => k !== key)
                : [...localPrefs.selectedKeys, key]
            })}
          />
        ))}
        <Tooltip title="Очистить значение тональности (ноты)">
          <Chip
            label="Нет предпочтений"
            clickable
            color={localPrefs.selectedKeys.length === 0 ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({...localPrefs, selectedKeys: []})}
          />
        </Tooltip>
      </Box>
      <Divider sx={{ my: 3 }} />

      {/* Mode */}
      <Typography variant="h6" gutterBottom>Тональность (мажор/минор)</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
        {modes.map((mode) => (
          <Chip
            key={mode}
            label={mode}
            clickable
            color={localPrefs.selectedModes.includes(mode) ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({
              ...localPrefs,
              selectedModes: localPrefs.selectedModes.includes(mode)
                ? localPrefs.selectedModes.filter(m => m !== mode)
                : [...localPrefs.selectedModes, mode]
            })}
          />
        ))}
        <Tooltip title="Очистить значение тональности (мажор/минор)">
          <Chip
            label="Нет предпочтений"
            clickable
            color={localPrefs.selectedModes.length === 0 ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({...localPrefs, selectedModes: []})}
          />
        </Tooltip>
      </Box>
      <Divider sx={{ my: 3 }} />

      {/* Signature */}
      <Typography variant="h6" gutterBottom>Размер такта</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
        {signatures.map((sig) => (
          <Chip
            key={sig}
            label={sig}
            clickable
            color={localPrefs.selectedSignatures.includes(sig) ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({
              ...localPrefs,
              selectedSignatures: localPrefs.selectedSignatures.includes(sig)
                ? localPrefs.selectedSignatures.filter(s => s !== sig)
                : [...localPrefs.selectedSignatures, sig]
            })}
          />
        ))}
        <Tooltip title="Очистить значение размера такта">
          <Chip
            label="Нет предпочтений"
            clickable
            color={localPrefs.selectedSignatures.length === 0 ? 'primary' : 'default'}
            onClick={() => setLocalPrefs({...localPrefs, selectedSignatures: []})}
          />
        </Tooltip>
      </Box>
      <Divider sx={{ my: 3 }} />

      {[
        { name: 'popularity', label: 'Популярность (%)', value: localPrefs.popularity.toFixed(0) },
        { name: 'loudness', label: 'Средняя громкость (dB)', value: (-60 + (localPrefs.loudness / 100) * 60).toFixed(1) },
        { name: 'acousticness', label: 'Акустичность', value: (localPrefs.acousticness / 100).toFixed(2) },
        { name: 'danceability', label: 'Танцевальность', value: (localPrefs.danceability / 100).toFixed(2) },
        { name: 'energy', label: 'Энергичность', value: (localPrefs.energy / 100).toFixed(2) },
        { name: 'liveness', label: 'Живость', value: (localPrefs.liveness / 100).toFixed(2) },
        { name: 'instrumentalness', label: 'Инструментальность', value: (localPrefs.instrumentalness / 100).toFixed(2) },
        { name: 'speechiness', label: 'Разговорность', value: (localPrefs.speechiness / 100).toFixed(2) },
        { name: 'valence', label: 'Позитивность', value: (localPrefs.valence / 100).toFixed(2) }
      ].map(({ name, label, value }) => (
        <Box key={name} mb={3}>
          <Typography gutterBottom>
            {label}: <strong>{value}</strong>
          </Typography>
          <Slider
            value={localPrefs[name]}
            onChange={(e, val) => setLocalPrefs({...localPrefs, [name]: val})}
            min={0}
            max={100}
            valueLabelDisplay="auto"
          />
        </Box>
      ))}

      <Button
        type="submit"
        variant="contained"
        size="large"
        disabled={loading}
        fullWidth
        sx={{ mt: 4, py: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : 'Получить рекомендации'}
      </Button>
    </Box>
  );
}