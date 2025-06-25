import React from 'react';
import { Container, Typography, Card, CardContent, Button, Box } from '@mui/material';
import { Star as StarIcon } from '@mui/icons-material';

function Shortlisting() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Candidate Shortlisting
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            AI-Powered Shortlisting
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Automatically shortlist top candidates based on match scores and criteria.
          </Typography>
          
          <Button
            variant="contained"
            startIcon={<StarIcon />}
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            Start Shortlisting
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Shortlisting; 