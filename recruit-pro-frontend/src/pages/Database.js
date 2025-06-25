import React from 'react';
import { Container, Typography, Card, CardContent, Button, Box } from '@mui/material';
import { Storage as StorageIcon } from '@mui/icons-material';

function Database() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Database Management
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Database Operations
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            View and manage database connections, data, and system status.
          </Typography>
          
          <Button
            variant="contained"
            startIcon={<StorageIcon />}
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            View Database
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Database; 