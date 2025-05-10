import { AppBar, Toolbar, Typography, Button, InputBase, IconButton, CircularProgress } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useState } from 'react';

export default function Header({ onReset, onSearch }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (e) => {
    e?.preventDefault();
    if (searchQuery.trim()) {
      setIsSearching(true);
      try {
        await onSearch(searchQuery);
      } finally {
        setIsSearching(false);
      }
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ mr: 2 }}>
          Рекомендательная система
        </Typography>
        
        <form onSubmit={handleSearch} style={{ 
          flexGrow: 1,
          display: 'flex',
          justifyContent: 'center'
        }}>
          <div style={{
            position: 'relative',
            borderRadius: '4px',
            backgroundColor: 'rgba(255, 255, 255, 0.15)',
            width: '100%',
            maxWidth: '600px',
            display: 'flex'
          }}>
            <div style={{
              padding: '0 16px',
              height: '100%',
              position: 'absolute',
              pointerEvents: 'none',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <SearchIcon />
            </div>
            <InputBase
              placeholder="Поиск по трекам или исполнителям..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                color: 'inherit',
                padding: '8px 8px 8px 48px',
                width: '100%'
              }}
            />
            <Button
              type="submit"
              color="inherit"
              disabled={isSearching || !searchQuery.trim()}
              style={{ minWidth: '80px' }}
            >
              {isSearching ? <CircularProgress size={24} color="inherit" /> : 'Искать'}
            </Button>
          </div>
        </form>
        
        <Button color="inherit" onClick={onReset} sx={{ ml: 2 }}>
          Очистить данные
        </Button>
      </Toolbar>
    </AppBar>
  );
}