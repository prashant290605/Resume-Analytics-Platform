import React from 'react';
import { Container, Typography, Card, CardContent, Button, Box } from '@mui/material';
import { Upload as UploadIcon } from '@mui/icons-material';

function Resumes() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Resume Management
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Upload and Manage Resumes
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Upload candidate resumes in PDF format for AI processing and matching.
          </Typography>
          
          <Button
            variant="contained"
            startIcon={<UploadIcon />}
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            Upload Resumes
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Resumes; 