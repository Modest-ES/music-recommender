import { useState } from 'react';
import { 
  Box, Button, TextField, Typography, Snackbar, Alert,
  FormControl, InputLabel, Select, MenuItem, Divider
} from '@mui/material';

const defaultValues = {
  track: '',
  artist: '',
  genre: '',
  album: 'NoData',
  year: 0,
  duration: 0,
  tempo: 0,
  popularity: 0,
  acousticness: 0.0,
  energy: 0.0,
  danceability: 0.0,
  liveness: 0.0,
  speechiness: 0.0,
  instrumentalness: 0.0,
  valence: 0.0,
  loudness: -6.0,
  key: 'NoData',
  mode: 'NoData',
  signature: 'NoData'
};

const keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'NoData'];
const modes = ['Major', 'Minor', 'NoData'];
const signatures = ['1/4', '3/4', '4/4', '5/4', 'NoData'];

export default function AddSong({ onAddSong }) {
  const [formValues, setFormValues] = useState(defaultValues);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]: value
    });
  };

  const handleNumberInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]: value === '' ? '' : Number(value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onAddSong(formValues);
      setSnackbarMessage(`Трек: ${formValues.artist} - ${formValues.track} успешно добавлен`);
      setSnackbarSeverity('success');
      setFormValues(defaultValues);
    } catch (error) {
      setSnackbarMessage('Ошибка добавления трека');
      setSnackbarSeverity('error');
    } finally {
      setOpenSnackbar(true);
      setIsSubmitting(false);
    }
  };

  const isSubmitDisabled = !formValues.track.trim() || 
                         !formValues.artist.trim() || 
                         !formValues.genre.trim() || 
                         isSubmitting;

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>Добавить новый трек</Typography>
      
      {/* Required Fields */}
      <TextField
        fullWidth
        label="Название трека"
        name="track"
        value={formValues.track}
        onChange={handleInputChange}
        margin="normal"
        required
      />
      <TextField
        fullWidth
        label="Исполнитель(и)"
        name="artist"
        value={formValues.artist}
        onChange={handleInputChange}
        margin="normal"
        required
      />
      <TextField
        fullWidth
        label="Жанр"
        name="genre"
        value={formValues.genre}
        onChange={handleInputChange}
        margin="normal"
        required
      />
      
      <Divider sx={{ my: 3 }} />
      
      {/* Optional Fields */}
      <TextField
        fullWidth
        label="Альбом"
        name="album"
        value={formValues.album}
        onChange={handleInputChange}
        margin="normal"
      />
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Год выпуска"
          name="year"
          type="number"
          value={formValues.year}
          onChange={handleNumberInputChange}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Длина (в секундах))"
          name="duration"
          type="number"
          value={formValues.duration}
          onChange={handleNumberInputChange}
          margin="normal"
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Темп (ударов в минуту / BPM)"
          name="tempo"
          type="number"
          value={formValues.tempo}
          onChange={handleNumberInputChange}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Популярность (0-100)"
          name="popularity"
          type="number"
          value={formValues.popularity}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ min: 0, max: 100 }}
        />
      </Box>
      
      <Divider sx={{ my: 3 }} />
      
      {/* Audio Features */}
      <Typography variant="h6" gutterBottom>Параметры аудио</Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Акустичность (0.0-1.0)"
          name="acousticness"
          type="number"
          value={formValues.acousticness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Танцевальность (0.0-1.0)"
          name="danceability"
          type="number"
          value={formValues.danceability}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Энергичность (0.0-1.0)"
          name="energy"
          type="number"
          value={formValues.energy}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Живость (0.0-1.0)"
          name="liveness"
          type="number"
          value={formValues.liveness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Разговорность (0.0-1.0)"
          name="speechiness"
          type="number"
          value={formValues.speechiness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Инструментальность (0.0-1.0)"
          name="instrumentalness"
          type="number"
          value={formValues.instrumentalness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Позитивность (0.0-1.0)"
          name="valence"
          type="number"
          value={formValues.valence}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Громкость (dB)"
          name="loudness"
          type="number"
          value={formValues.loudness}
          onChange={handleNumberInputChange}
          margin="normal"
        />
      </Box>
      
      <Divider sx={{ my: 3 }} />
      
      {/* Musical Properties */}
      <Typography variant="h6" gutterBottom>Музыкальные характеристики</Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <FormControl fullWidth margin="normal">
          <InputLabel>Тональность (нота)</InputLabel>
          <Select
            name="key"
            value={formValues.key}
            onChange={handleInputChange}
            label="Тональность (нота)"
          >
            {keys.map((key) => (
              <MenuItem key={key} value={key}>{key}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <FormControl fullWidth margin="normal">
          <InputLabel>Тональность (мажор/минор)</InputLabel>
          <Select
            name="mode"
            value={formValues.mode}
            onChange={handleInputChange}
            label="Тональность (мажор/минор)"
          >
            {modes.map((mode) => (
              <MenuItem key={mode} value={mode}>{mode}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <FormControl fullWidth margin="normal">
          <InputLabel>Размер такта</InputLabel>
          <Select
            name="signature"
            value={formValues.signature}
            onChange={handleInputChange}
            label="Размер такта"
          >
            {signatures.map((sig) => (
              <MenuItem key={sig} value={sig}>{sig}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      
      <Button
        type="submit"
        variant="contained"
        size="large"
        disabled={isSubmitDisabled}
        fullWidth
        sx={{ mt: 4, py: 2 }}
      >
        {isSubmitting ? 'Загрузка...' : 'Добавить'}
      </Button>
      
      <Snackbar
        open={openSnackbar}
        autoHideDuration={5000}
        onClose={() => setOpenSnackbar(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setOpenSnackbar(false)} 
          severity={snackbarSeverity}
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}