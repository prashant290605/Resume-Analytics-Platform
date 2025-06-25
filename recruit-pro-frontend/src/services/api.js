import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// Health check
export const healthCheck = () => api.get('/api/health');

// Get statistics
export const getStats = () => api.get('/api/stats');

// Job Descriptions
export const getJobDescriptions = () => api.get('/api/job-descriptions');
export const uploadJobDescriptions = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/upload/job-descriptions', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Resumes
export const getResumes = () => api.get('/api/resumes');
export const uploadResumes = (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });
  return api.post('/api/upload/resumes', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Matching
export const getMatches = () => api.get('/api/matches');
export const runMatching = () => api.post('/api/matching/run');

// Shortlisting
export const getShortlisted = () => api.get('/api/shortlisted');
export const runShortlisting = (threshold = 0.7) => {
  const formData = new FormData();
  formData.append('threshold', threshold);
  return api.post('/api/shortlisting/run', formData);
};

// Emails
export const sendEmails = (simulate = true) => {
  const formData = new FormData();
  formData.append('simulate', simulate);
  return api.post('/api/emails/send', formData);
};

// Pipeline
export const runFullPipeline = (simulateEmails = true, shortlistThreshold = 0.7) => {
  const formData = new FormData();
  formData.append('simulate_emails', simulateEmails);
  formData.append('shortlist_threshold', shortlistThreshold);
  return api.post('/api/pipeline/run', formData);
};

// Database
export const clearDatabase = () => api.delete('/api/clear');

export default api; 