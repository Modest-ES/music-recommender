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
          <Typography variant="h5">Результаты поиска</Typography>
          <Button onClick={onBack} variant="outlined">Вернуться к рекомендациям</Button>
        </Box>
  
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
                <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>Информация о треке</TableCell>
                    <TableCell>Параметры аудио</TableCell>
                    <TableCell>Действия</TableCell>
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
                                Альбом: {track.album}, {formatDuration(track.duration)}, Жанр: {track.genre}, Популярность: {track.popularity}%
                            </Typography>
                            
                            {/* Line 3: Key, mode, signature, tempo, loudness */}
                            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                Тональность: {track.key} {track.mode}, Размер такта: {track.signature}, {track.tempo} BPM, {track.loudness.toFixed(2)} dB
                            </Typography>
                        </Box>
                    </TableCell>
                    
                    {/* Radar Chart Column */}
                    <TableCell sx={{ width: '200px' }}>
                        <RadarChart features={{
                            А: track.acousticness,
                            Т: track.danceability,
                            Э: track.energy,
                            И: track.instrumentalness,
                            Р: track.speechiness,
                            Ж: track.liveness,
                            П: track.valence
                        }} />
                    </TableCell>
                    
                    {/* Remove button column */}
                    <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                            <Tooltip title="Нравится">
                                <IconButton 
                                color={likedIds.includes(track.id) ? 'primary' : 'default'}
                                onClick={() => onAction(track, 'like', !likedIds.includes(track.id) && !dislikedIds.includes(track.id))}
                                >
                                <ThumbUp />
                                </IconButton>
                            </Tooltip>
                            <Tooltip title="Не нравится">
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