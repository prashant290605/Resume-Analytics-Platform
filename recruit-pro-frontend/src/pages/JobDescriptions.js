import React, { useState } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Box,
  Grid,
  TextField,
  Alert,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Upload as UploadIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  CheckCircle as CheckIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

function JobDescriptions() {
  const [jobDescriptions, setJobDescriptions] = useState([
    {
      id: 1,
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      type: 'Full-time',
      experience: '5+ years',
      skills: ['Python', 'React', 'AWS', 'Docker'],
      description: 'We are looking for a Senior Software Engineer to join our team...',
      status: 'Active',
      createdAt: '2024-01-15',
    },
    {
      id: 2,
      title: 'Data Scientist',
      company: 'DataFlow Analytics',
      location: 'New York, NY',
      type: 'Full-time',
      experience: '3+ years',
      skills: ['Python', 'Machine Learning', 'SQL', 'TensorFlow'],
      description: 'Join our data science team to build innovative ML solutions...',
      status: 'Active',
      createdAt: '2024-01-10',
    },
  ]);

  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [newJob, setNewJob] = useState({
    title: '',
    company: '',
    location: '',
    type: '',
    experience: '',
    skills: '',
    description: '',
  });

  const addMessage = (type, text) => {
    const newMessage = {
      id: Date.now(),
      type,
      text,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    setIsUploading(true);
    setMessages([]);

    // Simulate file processing
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate extracting job descriptions from file
      const extractedJobs = [
        {
          id: Date.now() + i,
          title: `Job from ${file.name}`,
          company: 'Extracted Company',
          location: 'Remote',
          type: 'Full-time',
          experience: '2+ years',
          skills: ['Python', 'JavaScript'],
          description: `Job description extracted from ${file.name}`,
          status: 'Active',
          createdAt: new Date().toISOString().split('T')[0],
        }
      ];

      setJobDescriptions(prev => [...prev, ...extractedJobs]);
      addMessage('success', `Successfully processed ${file.name} - extracted ${extractedJobs.length} job descriptions`);
    }

    setIsUploading(false);
    addMessage('success', `All files processed successfully! Total job descriptions: ${jobDescriptions.length + files.length}`);
  };

  const handleAddJob = () => {
    if (newJob.title && newJob.company) {
      const job = {
        id: Date.now(),
        ...newJob,
        skills: newJob.skills.split(',').map(skill => skill.trim()),
        status: 'Active',
        createdAt: new Date().toISOString().split('T')[0],
      };
      setJobDescriptions(prev => [...prev, job]);
      setNewJob({
        title: '',
        company: '',
        location: '',
        type: '',
        experience: '',
        skills: '',
        description: '',
      });
      setOpenDialog(false);
      addMessage('success', `Job description "${job.title}" added successfully`);
    }
  };

  const handleEditJob = (job) => {
    setSelectedJob(job);
    setNewJob({
      title: job.title,
      company: job.company,
      location: job.location,
      type: job.type,
      experience: job.experience,
      skills: job.skills.join(', '),
      description: job.description,
    });
    setOpenDialog(true);
  };

  const handleDeleteJob = (jobId) => {
    setJobDescriptions(prev => prev.filter(job => job.id !== jobId));
    addMessage('success', 'Job description deleted successfully');
  };

  const handleViewJob = (job) => {
    setSelectedJob(job);
    setOpenDialog(true);
  };

  return (
    <Container maxWidth="xl">
      <Typography variant="h3" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 4 }}>
        Job Descriptions Management
      </Typography>

      {/* Upload Section */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
            Upload Job Descriptions
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#1a1a1a' }}>
            Upload CSV files containing job descriptions or add them manually.
          </Typography>

          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadIcon />}
              disabled={isUploading}
              sx={{
                background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
                },
              }}
            >
              {isUploading ? 'Processing...' : 'Upload CSV Files'}
              <input
                type="file"
                multiple
                accept=".csv"
                hidden
                onChange={handleFileUpload}
              />
            </Button>

            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={() => {
                setSelectedJob(null);
                setNewJob({
                  title: '',
                  company: '',
                  location: '',
                  type: '',
                  experience: '',
                  skills: '',
                  description: '',
                });
                setOpenDialog(true);
              }}
              sx={{ borderColor: '#03A9B1', color: '#03A9B1' }}
            >
              Add Manually
            </Button>
          </Box>

          {isUploading && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" sx={{ color: '#1a1a1a' }}>
                Processing files... Please wait.
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

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

      {/* Statistics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <Typography variant="h4" sx={{ color: '#03A9B1', fontWeight: 700 }}>
              {jobDescriptions.length}
            </Typography>
            <Typography variant="body1" sx={{ color: '#1a1a1a', fontWeight: 600 }}>
              Total Jobs
            </Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <Typography variant="h4" sx={{ color: '#4CAF50', fontWeight: 700 }}>
              {jobDescriptions.filter(job => job.status === 'Active').length}
            </Typography>
            <Typography variant="body1" sx={{ color: '#1a1a1a', fontWeight: 600 }}>
              Active Jobs
            </Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <Typography variant="h4" sx={{ color: '#9C27B0', fontWeight: 700 }}>
              {jobDescriptions.filter(job => job.type === 'Full-time').length}
            </Typography>
            <Typography variant="body1" sx={{ color: '#1a1a1a', fontWeight: 600 }}>
              Full-time
            </Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <Typography variant="h4" sx={{ color: '#FF9800', fontWeight: 700 }}>
              {jobDescriptions.filter(job => job.type === 'Remote').length}
            </Typography>
            <Typography variant="body1" sx={{ color: '#1a1a1a', fontWeight: 600 }}>
              Remote Jobs
            </Typography>
          </Card>
        </Grid>
      </Grid>

      {/* Job Descriptions Table */}
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ color: '#000000', fontWeight: 600, mb: 3 }}>
            Job Descriptions
          </Typography>

          <TableContainer component={Paper} sx={{ boxShadow: 'none' }}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: 'rgba(3, 169, 177, 0.1)' }}>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Title</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Company</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Location</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Type</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Experience</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Skills</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Status</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#000000' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {jobDescriptions.map((job) => (
                  <TableRow key={job.id} hover>
                    <TableCell sx={{ color: '#1a1a1a', fontWeight: 500 }}>
                      {job.title}
                    </TableCell>
                    <TableCell sx={{ color: '#1a1a1a' }}>{job.company}</TableCell>
                    <TableCell sx={{ color: '#1a1a1a' }}>{job.location}</TableCell>
                    <TableCell>
                      <Chip 
                        label={job.type} 
                        size="small" 
                        sx={{ 
                          backgroundColor: job.type === 'Full-time' ? '#4CAF50' : '#FF9800',
                          color: 'white',
                          fontWeight: 600,
                        }} 
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#1a1a1a' }}>{job.experience}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                        {job.skills.slice(0, 3).map((skill, index) => (
                          <Chip 
                            key={index} 
                            label={skill} 
                            size="small" 
                            variant="outlined"
                            sx={{ fontSize: '0.7rem' }}
                          />
                        ))}
                        {job.skills.length > 3 && (
                          <Chip 
                            label={`+${job.skills.length - 3}`} 
                            size="small" 
                            sx={{ fontSize: '0.7rem' }}
                          />
                        )}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={job.status} 
                        size="small" 
                        sx={{ 
                          backgroundColor: job.status === 'Active' ? '#4CAF50' : '#f44336',
                          color: 'white',
                          fontWeight: 600,
                        }} 
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <IconButton 
                          size="small" 
                          onClick={() => handleViewJob(job)}
                          sx={{ color: '#03A9B1' }}
                        >
                          <ViewIcon />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          onClick={() => handleEditJob(job)}
                          sx={{ color: '#9C27B0' }}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          onClick={() => handleDeleteJob(job.id)}
                          sx={{ color: '#f44336' }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle sx={{ color: '#000000', fontWeight: 600 }}>
          {selectedJob ? 'Edit Job Description' : 'Add New Job Description'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Job Title"
                value={newJob.title}
                onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Company"
                value={newJob.company}
                onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Location"
                value={newJob.location}
                onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Job Type"
                value={newJob.type}
                onChange={(e) => setNewJob({ ...newJob, type: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Experience Required"
                value={newJob.experience}
                onChange={(e) => setNewJob({ ...newJob, experience: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Skills (comma-separated)"
                value={newJob.skills}
                onChange={(e) => setNewJob({ ...newJob, skills: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Job Description"
                value={newJob.description}
                onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
                sx={{ '& .MuiInputLabel-root': { color: '#666' } }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)} sx={{ color: '#666' }}>
            Cancel
          </Button>
          <Button 
            onClick={handleAddJob}
            variant="contained"
            sx={{
              background: 'linear-gradient(45deg, #03A9B1 30%, #9C27B0 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #028a91 30%, #7b1fa2 90%)',
              },
            }}
          >
            {selectedJob ? 'Update' : 'Add Job'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default JobDescriptions; 