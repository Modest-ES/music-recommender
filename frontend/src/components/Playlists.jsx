import { 
    Tabs, Tab, Box, Typography, Table, TableBody, 
    TableCell, TableContainer, TableHead, TableRow, Paper, IconButton 
  } from '@mui/material';
  import { Delete } from '@mui/icons-material';
  import { RadarChart } from './RadarChart';
  import { useState } from 'react';
  
  function TabPanel(props) {
    const { children, value, index, ...other } = props;
    return (
      <div {...other}>
        {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
      </div>
    );
  }
  
  export default function Playlists({ likedTracks, dislikedTracks, onRemove }) {
    const [tabValue, setTabValue] = useState(0);

    const formatDuration = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };
  
    return (
      <Box>
        <Typography variant="h5" gutterBottom>Плейлисты</Typography>
        
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label={`Понравились (${likedTracks.length})`} />
          <Tab label={`Не понравились (${dislikedTracks.length})`} />
        </Tabs>
        
        <TabPanel value={tabValue} index={0}>
          <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Информация о треке</TableCell>
                        <TableCell>Параметры аудио</TableCell>
                        <TableCell>Удалить</TableCell>
                    </TableRow>
                </TableHead>
              <TableBody>
                {likedTracks.map((track) => (
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
                                    Тональность: {track.key} {track.mode}, Размер такта {track.signature}, {track.tempo} BPM, {track.loudness.toFixed(2)} dB
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
                            <IconButton onClick={() => onRemove(track, 'liked')}>
                                <Delete color="error" />
                            </IconButton>
                        </TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>Информация о треке</TableCell>
                    <TableCell>Параметры аудио</TableCell>
                    <TableCell>Удалить</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dislikedTracks.map((track) => (
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
                                    Тональность: {track.key} {track.mode}, Размер такта {track.signature}, {track.tempo} BPM, {track.loudness.toFixed(2)} dB
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
                            <IconButton onClick={() => onRemove(track, 'disliked')}>
                                <Delete color="error" />
                            </IconButton>
                        </TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>
      </Box>
    );
  }