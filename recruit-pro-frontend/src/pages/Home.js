import React, { useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Box,
  LinearProgress,
  Alert,
  Chip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  Savings as SavingsIcon,
  Person as PersonIcon,
  CheckCircle as CheckIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';

function Home() {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [messages, setMessages] = useState([]);

  const stats = [
    { label: 'Faster Hiring', value: '89%', icon: <SpeedIcon />, color: '#03A9B1' },
    { label: 'Match Accuracy', value: '94%', icon: <TrendingUpIcon />, color: '#9C27B0' },
    { label: 'Cost Reduction', value: '76%', icon: <SavingsIcon />, color: '#4CAF50' },
  ];

  const agents = [
    { icon: '📄', name: 'CV Extractor Agent', description: 'Parses resumes to extract candidate information' },
    { icon: '🔍', name: 'Matching Agent', description: 'Uses embeddings to calculate similarity scores' },
    { icon: '✅', name: 'Shortlisting Agent', description: 'Filters candidates based on match scores' },
    { icon: '📅', name: 'Interview Scheduler Agent', description: 'Sends personalized invitation emails' },
  ];

  const benefits = [
    { icon: '⚡', name: 'Higher Match Precision', value: 94, description: 'AI-driven matching increases accuracy by 94%' },
    { icon: '💰', name: 'Cost Efficiency', value: 76, description: 'Reduce recruitment costs by 76% on average' },
    { icon: '📈', name: 'Enhanced Productivity', value: 82, description: 'HR team productivity improved by 82%' },
    { icon: '👤', name: 'Candidate Experience', value: 91, description: '91% improvement in candidate satisfaction' },
  ];

  const workflowSteps = [
    { icon: '📥', name: 'Data Ingestion', description: 'Upload job descriptions and candidate resumes' },
    { icon: '🧠', name: 'AI Processing', description: 'Extract structured data and insights' },
    { icon: '🔗', name: 'Smart Matching', description: 'Match candidates to jobs with AI algorithms' },
    { icon: '✓', name: 'Shortlisting', description: 'Filter top candidates for each position' },
    { icon: '📨', name: 'Automated Outreach', description: 'Schedule interviews with qualified candidates' },
  ];

  const addMessage = (type, text) => {
    const newMessage = {
      id: Date.now(),
      type,
      text,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const runPipeline = async () => {
    setIsRunning(true);
    setProgress(0);
    setMessages([]);

    const steps = [
      'Initializing database...',
      'Processing job descriptions...',
      'Processing resumes...',
      'Matching candidates...',
      'Shortlisting candidates...',
      'Sending emails...',
    ];

    for (let i = 0; i < steps.length; i++) {
      setCurrentStep(steps[i]);
      setProgress(((i + 1) / steps.length) * 100);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Add success message for each step
      addMessage('success', `Step ${i + 1} completed: ${steps[i]}`);
    }

    addMessage('success', 'Full pipeline execution completed! Navigate to specific pages to see results.');
    setIsRunning(false);
    setCurrentStep('');
  };

  return (
    <Container maxWidth="xl">
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700, color: '#000000' }}>
          Recruit Pro
        </Typography>
        <Typography variant="h5" color="text.secondary" sx={{ mb: 4, color: '#1a1a1a' }}>
          Next generation AI-powered recruiting solution
        </Typography>

        {/* Stats */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {stats.map((stat, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{ textAlign: 'center', p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                  <Box sx={{ color: stat.color, mr: 1 }}>{stat.icon}</Box>
                  <Typography variant="h3" sx={{ fontWeight: 700, color: stat.color }}>
                    {stat.value}
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ color: '#1a1a1a', fontWeight: 600 }}>
                  {stat.label}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Run Pipeline Button */}
        <Button
          variant="contained"
          size="large"
          startIcon={<PlayIcon />}
          onClick={runPipeline}
          disabled={isRunning}
          sx={{
            py: 2,
            px: 4,
            fontSize: '1.1rem',
            fontWeight: 600,
            background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
            },
          }}
        >
          {isRunning ? 'Running Pipeline...' : '🚀 Run Full Pipeline'}
        </Button>
      </Box>

      {/* Progress Section */}
      {isRunning && (
        <Card sx={{ mb: 4, p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Pipeline Progress
          </Typography>
          <Typography variant="body1" sx={{ mb: 2, color: '#1a1a1a' }}>
            {currentStep}
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={progress} 
            sx={{ 
              height: 8, 
              borderRadius: 4,
              backgroundColor: 'rgba(3, 169, 177, 0.2)',
              '& .MuiLinearProgress-bar': {
                background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              },
            }} 
          />
          <Typography variant="body2" sx={{ mt: 1, color: '#666' }}>
            {Math.round(progress)}% Complete
          </Typography>
        </Card>
      )}

      {/* Messages */}
      {messages.length > 0 && (
        <Box sx={{ mb: 4 }}>
          {messages.map((message) => (
            <Alert
              key={message.id}
              severity={message.type}
              sx={{ 
                mb: 1,
                '& .MuiAlert-message': {
                  color: '#000000',
                  fontWeight: 600,
                },
              }}
            >
              {message.text}
            </Alert>
          ))}
        </Box>
      )}

      {/* System Components */}
      <Typography variant="h4" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 3 }}>
        AI-Powered Recruitment System
      </Typography>

      <Grid container spacing={4} sx={{ mb: 6 }}>
        <Grid item xs={12} md={6}>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            System Agents
          </Typography>
          <Grid container spacing={2}>
            {agents.map((agent, index) => (
              <Grid item xs={12} key={index}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Typography variant="h4" sx={{ mr: 2 }}>{agent.icon}</Typography>
                      <Typography variant="h6" sx={{ color: '#000000', fontWeight: 600 }}>
                        {agent.name}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ color: '#1a1a1a' }}>
                      {agent.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Key Benefits
          </Typography>
          <Grid container spacing={2}>
            {benefits.map((benefit, index) => (
              <Grid item xs={12} key={index}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h4" sx={{ mr: 2 }}>{benefit.icon}</Typography>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" sx={{ color: '#000000', fontWeight: 600 }}>
                          {benefit.name}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#1a1a1a', mb: 1 }}>
                          {benefit.description}
                        </Typography>
                        <LinearProgress 
                          variant="determinate" 
                          value={benefit.value} 
                          sx={{ 
                            height: 6, 
                            borderRadius: 3,
                            backgroundColor: 'rgba(3, 169, 177, 0.2)',
                            '& .MuiLinearProgress-bar': {
                              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
                            },
                          }} 
                        />
                        <Typography variant="caption" sx={{ color: '#666' }}>
                          {benefit.value}%
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>

      {/* How It Works */}
      <Typography variant="h4" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 3 }}>
        How It Works
      </Typography>
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {workflowSteps.map((step, index) => (
          <Grid item xs={12} sm={6} md={2.4} key={index}>
            <Card sx={{ textAlign: 'center', p: 2, height: '100%' }}>
              <Typography variant="h3" sx={{ mb: 1 }}>{step.icon}</Typography>
              <Typography variant="h6" sx={{ color: '#000000', fontWeight: 600, mb: 1 }}>
                {step.name}
              </Typography>
              <Typography variant="body2" sx={{ color: '#1a1a1a' }}>
                {step.description}
              </Typography>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Call to Action */}
      <Card sx={{ 
        p: 4, 
        textAlign: 'center',
        background: 'linear-gradient(135deg, rgba(3, 169, 177, 0.1), rgba(156, 39, 176, 0.1))',
        border: '2px solid rgba(3, 169, 177, 0.2)',
      }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
          Ready to transform your recruitment process?
        </Typography>
        <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
          Start using our AI-powered system to find the perfect candidates faster and more efficiently.
        </Typography>
        <Button
          variant="contained"
          size="large"
          startIcon={<PlayIcon />}
          onClick={runPipeline}
          disabled={isRunning}
          sx={{
            py: 2,
            px: 4,
            fontSize: '1.1rem',
            fontWeight: 600,
            background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
            },
          }}
        >
          {isRunning ? 'Running Pipeline...' : '🚀 Run Full Pipeline'}
        </Button>
      </Card>
    </Container>
  );
}

export default Home; 