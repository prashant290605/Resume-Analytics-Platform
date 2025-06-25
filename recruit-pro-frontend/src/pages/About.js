import React from 'react';
import { Container, Typography, Card, CardContent, Box } from '@mui/material';

function About() {
  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        About Recruit Pro
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            AI-Powered Recruitment Platform
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Recruit Pro is a next-generation recruitment platform that leverages artificial intelligence 
            to streamline the hiring process. Our system uses advanced algorithms to match candidates 
            with job descriptions, automate shortlisting, and facilitate communication.
          </Typography>
          
          <Typography variant="h6" gutterBottom sx={{ color: '#000000', fontWeight: 600, mt: 3 }}>
            Key Features:
          </Typography>
          <Box component="ul" sx={{ color: '#1a1a1a' }}>
            <li>AI-powered candidate matching</li>
            <li>Automated resume parsing</li>
            <li>Intelligent shortlisting</li>
            <li>Personalized email automation</li>
            <li>Comprehensive database management</li>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
}

export default About; 