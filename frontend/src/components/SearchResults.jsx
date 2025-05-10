import { 
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
    Paper, Typography, Button, Box, IconButton, Tooltip 
  } from '@mui/material';
import { ThumbUp, ThumbDown } from '@mui/icons-material';
import { RadarChart } from './RadarChart';
  
  export default function SearchResults({ results, onAction, likedIds, dislikedIds, onBack }) {

    const formatDuration = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    return (
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h5">Search Results</Typography>
          <Button onClick={onBack} variant="outlined">Back to Recommendations</Button>
        </Box>
  
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
                <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>Track Info</TableCell>
                    <TableCell>Audio Features</TableCell>
                    <TableCell>Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
              {results.map((track) => (
                <TableRow key={track.id}>
                    <TableCell>{track.id}</TableCell>
                    {/* Song data column */}
                    <TableCell>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            {/* Line 1: Artist - Track (Year) */}
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                {track.artist} - {track.track} ({track.year})
                            </Typography>
                            
                            {/* Line 2: Album, duration, genre, popularity */}
                            <Typography variant="body2">
                                Album: {track.album}, {formatDuration(track.duration)}, Genre: {track.genre}, Popularity: {track.popularity}%
                            </Typography>
                            
                            {/* Line 3: Key, mode, signature, tempo, loudness */}
                            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                Key: {track.key} {track.mode}, {track.signature} time, {track.tempo} BPM, {track.loudness.toFixed(2)} dB
                            </Typography>
                        </Box>
                    </TableCell>
                    
                    {/* Radar Chart Column */}
                    <TableCell sx={{ width: '200px' }}>
                        <RadarChart features={{
                            A: track.acousticness,
                            D: track.danceability,
                            E: track.energy,
                            I: track.instrumentalness,
                            S: track.speechiness,
                            L: track.liveness,
                            V: track.valence
                        }} />
                    </TableCell>
                    
                    {/* Remove button column */}
                    <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                            <Tooltip title="Like">
                                <IconButton 
                                color={likedIds.includes(track.id) ? 'primary' : 'default'}
                                onClick={() => onAction(track, 'like', !likedIds.includes(track.id) && !dislikedIds.includes(track.id))}
                                >
                                <ThumbUp />
                                </IconButton>
                            </Tooltip>
                            <Tooltip title="Dislike">
                                <IconButton 
                                color={dislikedIds.includes(track.id) ? 'error' : 'default'}
                                onClick={() => onAction(track, 'dislike', !likedIds.includes(track.id) && !dislikedIds.includes(track.id))}
                                >
                                <ThumbDown />
                                </IconButton>
                            </Tooltip>
                        </Box>
                    </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    );
  }