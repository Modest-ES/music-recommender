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
      setSnackbarMessage(`Song: ${formValues.artist} - ${formValues.track} was successfully added`);
      setSnackbarSeverity('success');
      setFormValues(defaultValues);
    } catch (error) {
      setSnackbarMessage('Failed to add song. Please try again.');
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
      <Typography variant="h5" gutterBottom>Add New Song</Typography>
      
      {/* Required Fields */}
      <TextField
        fullWidth
        label="Track Name"
        name="track"
        value={formValues.track}
        onChange={handleInputChange}
        margin="normal"
        required
      />
      <TextField
        fullWidth
        label="Artist"
        name="artist"
        value={formValues.artist}
        onChange={handleInputChange}
        margin="normal"
        required
      />
      <TextField
        fullWidth
        label="Genre"
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
        label="Album"
        name="album"
        value={formValues.album}
        onChange={handleInputChange}
        margin="normal"
      />
      
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Year"
          name="year"
          type="number"
          value={formValues.year}
          onChange={handleNumberInputChange}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Duration (seconds)"
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
          label="Tempo (BPM)"
          name="tempo"
          type="number"
          value={formValues.tempo}
          onChange={handleNumberInputChange}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Popularity (0-100)"
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
      <Typography variant="h6" gutterBottom>Audio Features</Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          fullWidth
          label="Acousticness (0.0-1.0)"
          name="acousticness"
          type="number"
          value={formValues.acousticness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Danceability (0.0-1.0)"
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
          label="Energy (0.0-1.0)"
          name="energy"
          type="number"
          value={formValues.energy}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Liveness (0.0-1.0)"
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
          label="Speechiness (0.0-1.0)"
          name="speechiness"
          type="number"
          value={formValues.speechiness}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Instrumentalness (0.0-1.0)"
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
          label="Valence (0.0-1.0)"
          name="valence"
          type="number"
          value={formValues.valence}
          onChange={handleNumberInputChange}
          margin="normal"
          inputProps={{ step: "0.01", min: 0, max: 1 }}
        />
        <TextField
          fullWidth
          label="Loudness (dB)"
          name="loudness"
          type="number"
          value={formValues.loudness}
          onChange={handleNumberInputChange}
          margin="normal"
        />
      </Box>
      
      <Divider sx={{ my: 3 }} />
      
      {/* Musical Properties */}
      <Typography variant="h6" gutterBottom>Musical Properties</Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <FormControl fullWidth margin="normal">
          <InputLabel>Key</InputLabel>
          <Select
            name="key"
            value={formValues.key}
            onChange={handleInputChange}
            label="Key"
          >
            {keys.map((key) => (
              <MenuItem key={key} value={key}>{key}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <FormControl fullWidth margin="normal">
          <InputLabel>Mode</InputLabel>
          <Select
            name="mode"
            value={formValues.mode}
            onChange={handleInputChange}
            label="Mode"
          >
            {modes.map((mode) => (
              <MenuItem key={mode} value={mode}>{mode}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <FormControl fullWidth margin="normal">
          <InputLabel>Time Signature</InputLabel>
          <Select
            name="signature"
            value={formValues.signature}
            onChange={handleInputChange}
            label="Time Signature"
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
        {isSubmitting ? 'Adding...' : 'Add Song'}
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