import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  Box,
  Chip,
} from '@mui/material';
import {
  Person as PersonIcon,
  History as HistoryIcon,
  LocalHospital as HospitalIcon,
  Medication as MedicationIcon,
  MonitorHeart as VitalsIcon,
  Warning as AllergyIcon,
  Recommend as RecommendIcon,
} from '@mui/icons-material';
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  withCredentials: true
});

const Analysis = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await api.get('/api/v1/analysis');
        console.log('Raw API Response:', response.data);
        
        if (response.data && response.data.analysis) {
          const analysisData = response.data.analysis;
          console.log('Analysis Data:', analysisData);
          
          // Process treatment plan if it exists
          if (analysisData.treatment_plan) {
            console.log('Raw Treatment Plan:', analysisData.treatment_plan);
            
            // Ensure treatment_plan is properly structured
            const processedTreatmentPlan = {
              recommendations: typeof analysisData.treatment_plan.recommendations === 'string' 
                ? analysisData.treatment_plan.recommendations 
                : JSON.stringify(analysisData.treatment_plan.recommendations),
              confidence_score: typeof analysisData.treatment_plan.confidence_score === 'number'
                ? analysisData.treatment_plan.confidence_score
                : parseFloat(analysisData.treatment_plan.confidence_score) || 0,
              source_data: typeof analysisData.treatment_plan.source_data === 'string'
                ? analysisData.treatment_plan.source_data
                : JSON.stringify(analysisData.treatment_plan.source_data)
            };
            
            console.log('Processed Treatment Plan:', processedTreatmentPlan);
            analysisData.treatment_plan = processedTreatmentPlan;
          }
          
          setAnalysis(analysisData);
        } else {
          setError('Invalid analysis data format');
        }
      } catch (err) {
        console.error('Analysis error:', err);
        setError(err.response?.data?.detail || 'Error fetching analysis');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
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
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Alert severity="info">
          Please upload a medical document through the Upload page first.
        </Alert>
      </Container>
    );
  }

  if (!analysis || analysis.status === "No recent analysis available") {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="info" sx={{ mb: 2 }}>
          No analysis data available. Please upload a medical document first.
        </Alert>
      </Container>
    );
  }

  const {
    patient_info = {},
    medical_history = [],
    current_symptoms = [],
    medications = [],
    vitals = {},
    allergies = [],
    recommendations = {
      lifestyle_changes: [],
      follow_up: '',
      monitoring: []
    }
  } = analysis;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom color="primary">
        Healthcare Analysis Report
      </Typography>

      {/* Patient Information */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Patient Information</Typography>
            </Box>
            <Grid container spacing={2}>
              {Object.entries(patient_info).map(([key, value]) => (
                <Grid item xs={12} sm={6} md={3} key={key}>
                  <Typography variant="subtitle2" color="textSecondary">
                    {key.toUpperCase()}
                  </Typography>
                  <Typography variant="body1">{value || 'N/A'}</Typography>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Medical History and Current Symptoms */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box display="flex" alignItems="center" mb={2}>
              <HistoryIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Medical History</Typography>
            </Box>
            <List dense>
              {medical_history.map((item, index) => (
                <ListItem key={index}>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
              {medical_history.length === 0 && (
                <ListItem>
                  <ListItemText primary="No medical history found" />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box display="flex" alignItems="center" mb={2}>
              <HospitalIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Current Symptoms</Typography>
            </Box>
            <List dense>
              {current_symptoms.map((symptom, index) => (
                <ListItem key={index}>
                  <ListItemText primary={symptom} />
                </ListItem>
              ))}
              {current_symptoms.length === 0 && (
                <ListItem>
                  <ListItemText primary="No current symptoms found" />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        {/* Medications and Vitals */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box display="flex" alignItems="center" mb={2}>
              <MedicationIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Medications</Typography>
            </Box>
            <List dense>
              {medications.map((medication, index) => (
                <ListItem key={index}>
                  <ListItemText primary={medication} />
                </ListItem>
              ))}
              {medications.length === 0 && (
                <ListItem>
                  <ListItemText primary="No medications found" />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box display="flex" alignItems="center" mb={2}>
              <VitalsIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Vital Signs</Typography>
            </Box>
            <Grid container spacing={2}>
              {Object.entries(vitals).map(([key, value]) => (
                <Grid item xs={6} key={key}>
                  <Typography variant="subtitle2" color="textSecondary">
                    {key.replace('_', ' ').toUpperCase()}
                  </Typography>
                  <Typography variant="body1">{value || 'N/A'}</Typography>
                </Grid>
              ))}
              {Object.keys(vitals).length === 0 && (
                <Grid item xs={12}>
                  <Typography>No vital signs recorded</Typography>
                </Grid>
              )}
            </Grid>
          </Paper>
        </Grid>

        {/* Allergies */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <AllergyIcon sx={{ mr: 1, color: 'error.main' }} />
              <Typography variant="h6">Allergies</Typography>
            </Box>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {allergies.map((allergy, index) => (
                <Chip
                  key={index}
                  label={allergy}
                  color="error"
                  variant="outlined"
                />
              ))}
              {allergies.length === 0 && (
                <Typography>No allergies found</Typography>
              )}
            </Box>
          </Paper>
        </Grid>

        {/* Treatment Recommendations */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <RecommendIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">Treatment Recommendations</Typography>
            </Box>
            <Grid container spacing={3}>
              {/* Lifestyle Changes */}
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Lifestyle Changes
                </Typography>
                <List dense>
                  {recommendations.lifestyle_changes.map((change, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={change} />
                    </ListItem>
                  ))}
                  {recommendations.lifestyle_changes.length === 0 && (
                    <ListItem>
                      <ListItemText primary="No lifestyle changes recommended" />
                    </ListItem>
                  )}
                </List>
              </Grid>

              {/* Follow-up Plan */}
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Follow-up Plan
                </Typography>
                <Typography variant="body1">
                  {recommendations.follow_up || 'No specific follow-up plan provided'}
                </Typography>
              </Grid>

              {/* Monitoring Plan */}
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Monitoring Requirements
                </Typography>
                <List dense>
                  {recommendations.monitoring.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={item} />
                    </ListItem>
                  ))}
                  {recommendations.monitoring.length === 0 && (
                    <ListItem>
                      <ListItemText primary="No specific monitoring required" />
                    </ListItem>
                  )}
                </List>
              </Grid>

              {/* AI Treatment Plan */}
              {analysis.treatment_plan && (
                <Grid item xs={12}>
                  <Typography variant="subtitle1" color="primary" gutterBottom>
                    AI-Generated Treatment Plan
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.default' }}>
                    <Typography variant="body1" style={{ whiteSpace: 'pre-line' }}>
                      {typeof analysis.treatment_plan.recommendations === 'string' 
                        ? analysis.treatment_plan.recommendations 
                        : 'No specific recommendations provided'}
                    </Typography>
                    {typeof analysis.treatment_plan.confidence_score === 'number' && analysis.treatment_plan.confidence_score > 0 && (
                      <Box mt={2}>
                        <Typography variant="caption" color="textSecondary">
                          Confidence Score: {(analysis.treatment_plan.confidence_score * 100).toFixed(1)}%
                        </Typography>
                      </Box>
                    )}
                    {typeof analysis.treatment_plan.source_data === 'string' && analysis.treatment_plan.source_data && (
                      <Box mt={1}>
                        <Typography variant="caption" color="textSecondary">
                          Source: {analysis.treatment_plan.source_data}
                        </Typography>
                      </Box>
                    )}
                  </Paper>
                </Grid>
              )}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Analysis;