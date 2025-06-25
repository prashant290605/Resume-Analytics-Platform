import React from 'react';
import { Container, Typography, Card, CardContent, Button, Box } from '@mui/material';
import { PlayArrow as PlayIcon } from '@mui/icons-material';

function Matching() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Candidate Matching
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            AI-Powered Candidate Matching
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Use AI algorithms to match candidates with job descriptions based on skills and experience.
          </Typography>
          
          <Button
            variant="contained"
            startIcon={<PlayIcon />}
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            Start Matching
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Matching; 