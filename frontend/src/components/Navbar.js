import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          GenMediPlan
        </Typography>
        <Box>
          <Button color="inherit" onClick={() => navigate('/')}>
            Dashboard
          </Button>
          <Button color="inherit" onClick={() => navigate('/upload')}>
            Upload
          </Button>
          <Button color="inherit" onClick={() => navigate('/analysis')}>
            Analysis
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;