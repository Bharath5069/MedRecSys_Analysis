import React from 'react';
import { Container, Typography, Paper } from '@mui/material';
import PDFUploader from './PDFUploader';
import AnalysisHistory from './AnalysisHistory';

const Upload = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom color="primary">
        Upload Medical Document
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Upload PDF
        </Typography>
        <PDFUploader />
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analysis History
        </Typography>
        <AnalysisHistory />
      </Paper>
    </Container>
  );
};

export default Upload;