import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Paper, List, ListItem, ListItemText, CircularProgress, Alert, Box } from '@mui/material';
import {
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  withCredentials: true
});

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    recentAnalyses: [],
    systemStatus: 'operational'
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await api.get('/api/v1/analysis');
        if (response.data && response.data.analysis) {
          setStats({
            totalAnalyses: 1, // This should come from backend
            recentAnalyses: [response.data.analysis],
            systemStatus: 'operational'
          });
        }
      } catch (err) {
        console.error('Dashboard error:', err);
        setError(err.response?.data?.detail || 'Error fetching dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom color="primary">
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Recent Analyses */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', minHeight: 240 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <TimelineIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Recent Analyses</Typography>
            </Box>
            {stats.recentAnalyses.length > 0 ? (
              <List>
                {stats.recentAnalyses.map((analysis, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={analysis.patient_info?.name || 'Unknown Patient'}
                      secondary={`Analyzed on ${new Date().toLocaleDateString()}`}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="textSecondary">No recent analyses</Typography>
            )}
          </Paper>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', minHeight: 240 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <AssessmentIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Quick Stats</Typography>
            </Box>
            <List>
              <ListItem>
                <ListItemText
                  primary="Total Analyses"
                  secondary={stats.totalAnalyses}
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Success Rate"
                  secondary="100%"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Average Processing Time"
                  secondary="< 30 seconds"
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>

        {/* System Status */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={2}>
              {stats.systemStatus === 'operational' ? (
                <CheckCircleIcon sx={{ mr: 1, color: 'success.main' }} />
              ) : (
                <ErrorIcon sx={{ mr: 1, color: 'error.main' }} />
              )}
              <Typography variant="h6">System Status</Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Typography variant="subtitle2" color="textSecondary">
                  Backend API
                </Typography>
                <Typography color="success.main">Operational</Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="subtitle2" color="textSecondary">
                  PDF Processing
                </Typography>
                <Typography color="success.main">Operational</Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="subtitle2" color="textSecondary">
                  AI Recommendations
                </Typography>
                <Typography color="success.main">Operational</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard; 