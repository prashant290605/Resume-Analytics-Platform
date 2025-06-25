import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import {
  Home as HomeIcon,
  Description as JobIcon,
  Person as ResumeIcon,
  Link as MatchIcon,
  Star as ShortlistIcon,
  Email as EmailIcon,
  Storage as DatabaseIcon,
  Info as AboutIcon,
} from '@mui/icons-material';

const navItems = [
  { path: '/', label: 'Home', icon: <HomeIcon /> },
  { path: '/job-descriptions', label: 'Job Descriptions', icon: <JobIcon /> },
  { path: '/resumes', label: 'Resumes', icon: <ResumeIcon /> },
  { path: '/matching', label: 'Matching', icon: <MatchIcon /> },
  { path: '/shortlisting', label: 'Shortlisting', icon: <ShortlistIcon /> },
  { path: '/emails', label: 'Emails', icon: <EmailIcon /> },
  { path: '/database', label: 'Database', icon: <DatabaseIcon /> },
  { path: '/about', label: 'About', icon: <AboutIcon /> },
];

function Navbar() {
  const location = useLocation();

  return (
    <AppBar position="static" elevation={0} sx={{ backgroundColor: 'white', borderBottom: '1px solid rgba(0, 0, 0, 0.1)' }}>
      <Container maxWidth="xl">
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              textDecoration: 'none',
              color: 'primary.main',
              fontWeight: 700,
              fontSize: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
          >
            🤖 Recruit Pro
          </Typography>

          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={Link}
                to={item.path}
                startIcon={item.icon}
                sx={{
                  color: location.pathname === item.path ? 'primary.main' : '#666',
                  backgroundColor: location.pathname === item.path ? 'rgba(3, 169, 177, 0.1)' : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(3, 169, 177, 0.1)',
                    color: 'primary.main',
                  },
                  fontWeight: location.pathname === item.path ? 600 : 500,
                  textTransform: 'none',
                  borderRadius: 2,
                  px: 2,
                  py: 1,
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Navbar; 