import React from 'react';
import { Container, Typography, Card, CardContent, Button, Box } from '@mui/material';
import { Email as EmailIcon } from '@mui/icons-material';

function Emails() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Email Management
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Automated Email System
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Send personalized interview invitations and follow-up emails to shortlisted candidates.
          </Typography>
          
          <Button
            variant="contained"
            startIcon={<EmailIcon />}
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            Send Emails
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Emails; 