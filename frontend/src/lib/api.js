import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
});

export const getDashboard = async () => (await api.get("/dashboard")).data;
export const getJobs = async () => (await api.get("/jobs")).data;
export const getDefaultJds = async () => (await api.get("/default-jds")).data;
export const getResults = async (screeningId) =>
  (await api.get("/results", { params: screeningId ? { screening_id: screeningId } : {} })).data;
export const getBatchResults = async (batchId) => (await api.get(`/batch/${batchId}/results`)).data;
export const getCandidate = async (resumeId, screeningId) =>
  (await api.get(`/candidates/${resumeId}`, { params: { screening_id: screeningId } })).data;
export const createBatch = async (name) => (await api.post("/batch/create", { name })).data;

export const uploadJob = async ({ title, description, file }) => {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("description", description || "");
  if (file) {
    formData.append("file", file);
  }
  return (await api.post("/jobs", formData)).data;
};

export const uploadResumes = async (files, onUploadProgress, batchId = null) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const endpoint = batchId ? `/batch/${batchId}/upload` : "/resumes";
  return (
    await api.post(endpoint, formData, {
      onUploadProgress,
    })
  ).data;
};

export const runScreening = async (payload) => (await api.post("/screenings/run", payload)).data;

export default api;
