import { Activity, BrainCircuit, Files, MailCheck, PlayCircle } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import ResultsTable from "../components/ResultsTable";
import StatCard from "../components/StatCard";
import UploadPanel from "../components/UploadPanel";
import { createBatch, getBatchResults, getDashboard, getDefaultJds, getJobs, getResults, runScreening, uploadJob, uploadResumes } from "../lib/api";

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [defaultJds, setDefaultJds] = useState([]);
  const [results, setResults] = useState({ candidates: [] });
  const [selectedRoleMode, setSelectedRoleMode] = useState("custom");
  const [selectedDefaultRole, setSelectedDefaultRole] = useState("");
  const [jobTitle, setJobTitle] = useState("Senior Software Engineer");
  const [jobDescription, setJobDescription] = useState("");
  const [jobFile, setJobFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [currentBatchId, setCurrentBatchId] = useState(null);
  const [batchMode, setBatchMode] = useState("new");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [threshold, setThreshold] = useState(70);
  const [isUploading, setIsUploading] = useState(false);
  const [isScreening, setIsScreening] = useState(false);
  const [search, setSearch] = useState("");
  const [shortlistedOnly, setShortlistedOnly] = useState(false);
  const [sortBy, setSortBy] = useState("score");
  const [message, setMessage] = useState("Upload a role and candidate resumes to start screening.");

  const refresh = async () => {
    const [dashboardData, jobsData, resultsData, defaultRoles] = await Promise.all([getDashboard(), getJobs(), getResults(), getDefaultJds()]);
    setDashboard(dashboardData);
    setJobs(jobsData);
    setResults(resultsData);
    setDefaultJds(defaultRoles);
    if (!selectedDefaultRole && defaultRoles[0]?.id) {
      setSelectedDefaultRole(defaultRoles[0].id);
    }
    if (!selectedJobId && jobsData[0]?.id) {
      setSelectedJobId(jobsData[0].id);
    }
  };

  useEffect(() => {
    refresh().catch(() => {
      setMessage("Backend unavailable. Start the FastAPI server to use the dashboard.");
    });
  }, []);

  useEffect(() => {
    if (selectedRoleMode === "custom") {
      return;
    }
    const role = defaultJds.find((item) => item.id === (selectedRoleMode === "custom" ? selectedDefaultRole : selectedRoleMode));
    if (!role) {
      return;
    }
    setSelectedDefaultRole(role.id);
    setJobTitle(role.title);
    setJobDescription(role.description);
    setJobFile(null);
  }, [selectedRoleMode, defaultJds]);

  useEffect(() => {
    if (selectedRoleMode === "custom") {
      return;
    }
    const role = defaultJds.find((item) => item.id === selectedDefaultRole);
    if (!role) {
      return;
    }
    setJobTitle(role.title);
    setJobDescription(role.description);
    setJobFile(null);
  }, [selectedDefaultRole, selectedRoleMode, defaultJds]);

  const filteredCandidates = useMemo(() => {
    const text = search.trim().toLowerCase();
    const items = results.candidates.filter((candidate) => {
      const matchesSearch =
        !text ||
        candidate.name.toLowerCase().includes(text) ||
        candidate.skills.some((skill) => skill.toLowerCase().includes(text));
      const matchesShortlist = !shortlistedOnly || candidate.shortlisted;
      return matchesSearch && matchesShortlist;
    });

    const sorted = [...items];
    sorted.sort((left, right) => {
      if (sortBy === "name") return left.name.localeCompare(right.name);
      if (sortBy === "experience") return right.years_experience - left.years_experience;
      return right.score - left.score;
    });
    return sorted;
  }, [results.candidates, search, shortlistedOnly, sortBy]);

  const handleJobUpload = async () => {
    setIsUploading(true);
    setMessage("Saving job description and extracting structured requirements...");
    try {
      const response = await uploadJob({ title: jobTitle, description: jobDescription, file: jobFile });
      setSelectedJobId(response.id);
      setJobDescription("");
      setJobFile(null);
      setMessage(`Saved ${response.title}. Required skills extracted successfully.`);
      await refresh();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to save the job description.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleCreateBatch = async () => {
    try {
      const batch = await createBatch(`Hiring Batch ${new Date().toLocaleString()}`);
      setCurrentBatchId(batch.id);
      setBatchMode("current");
      setMessage(`Started hiring batch ${batch.id}.`);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to create a hiring batch.");
    }
  };

  const handleResumeUpload = async () => {
    setIsUploading(true);
    setMessage("Uploading PDF resumes and parsing candidate profiles...");
    try {
      let activeBatchId = currentBatchId;
      if (batchMode === "new" || !activeBatchId) {
        const batch = await createBatch(`Hiring Batch ${new Date().toLocaleString()}`);
        activeBatchId = batch.id;
        setCurrentBatchId(batch.id);
      }

      await uploadResumes(resumeFiles, (event) => {
        const total = event.total || 1;
        setUploadProgress(Math.round((event.loaded / total) * 100));
      }, activeBatchId);
      setResumeFiles([]);
      setUploadProgress(100);
      setMessage(`Resumes uploaded and parsed successfully for batch ${activeBatchId}.`);
      await refresh();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to upload resumes.");
    } finally {
      setIsUploading(false);
      window.setTimeout(() => setUploadProgress(0), 1200);
    }
  };

  const handleRunScreening = async () => {
    if (!selectedJobId) {
      setMessage("Create or select a job description before running screening.");
      return;
    }

    setIsScreening(true);
    setMessage("Running screening, generating embeddings, scoring candidates, and preparing interview drafts...");
    try {
      const response = await runScreening({
        job_id: selectedJobId,
        batch_id: currentBatchId,
        threshold,
        generate_emails: true,
      });
      if (response.batch_id) {
        setCurrentBatchId(response.batch_id);
      }
      const resultPayload = response.batch_id ? await getBatchResults(response.batch_id) : await getResults(response.screening_id);
      setResults(resultPayload);
      setMessage(`Screening complete for ${response.job_title}. ${response.shortlisted_count} candidates shortlisted.`);
      await refresh();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Screening run failed.");
    } finally {
      setIsScreening(false);
    }
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(20,184,126,0.22),_transparent_35%),radial-gradient(circle_at_top_right,_rgba(14,165,233,0.18),_transparent_28%),linear-gradient(180deg,_#020617_0%,_#0f172a_100%)] px-4 py-6 text-ink sm:px-6 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="rounded-[2.25rem] border border-white/10 bg-slate-900/60 px-6 py-7 shadow-panel backdrop-blur lg:px-8">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-sm font-semibold uppercase tracking-[0.32em] text-brand-200">Resume Analytics Platform</p>
              <h1 className="mt-4 font-display text-4xl text-white sm:text-5xl">AI-powered hiring intelligence that feels ready for real recruiters.</h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                Upload resumes, parse role requirements, rank every applicant with semantic and skills-aware scoring, and move directly into shortlist-ready outreach.
              </p>
            </div>
            <div className="rounded-[1.75rem] border border-white/10 bg-slate-950/55 px-5 py-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Current status</p>
              <p className="mt-3 max-w-sm text-sm leading-6 text-slate-300">{message}</p>
            </div>
          </div>
        </header>

        <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard eyebrow="Processed" value={dashboard?.total_resumes ?? 0} label="Total resumes parsed" tone="emerald" />
          <StatCard eyebrow="Shortlisted" value={dashboard?.shortlisted_candidates ?? 0} label="Candidates above threshold" tone="amber" />
          <StatCard eyebrow="Average score" value={`${dashboard?.average_match_score?.toFixed?.(1) ?? "0.0"}%`} label="Across all screening runs" tone="cyan" />
          <StatCard eyebrow="Runs" value={dashboard?.screenings_run ?? 0} label={dashboard?.embedding_provider ? `Provider: ${dashboard.embedding_provider}` : "Awaiting first run"} tone="rose" />
        </section>

        <section className="mt-8">
          <UploadPanel
            defaultJds={defaultJds}
            selectedRoleMode={selectedRoleMode}
            setSelectedRoleMode={setSelectedRoleMode}
            selectedDefaultRole={selectedDefaultRole}
            setSelectedDefaultRole={setSelectedDefaultRole}
            jobTitle={jobTitle}
            setJobTitle={setJobTitle}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            jobFile={jobFile}
            setJobFile={setJobFile}
            resumeFiles={resumeFiles}
            setResumeFiles={setResumeFiles}
            currentBatchId={currentBatchId}
            batchMode={batchMode}
            setBatchMode={setBatchMode}
            onCreateBatch={handleCreateBatch}
            uploadProgress={uploadProgress}
            onSubmitJob={handleJobUpload}
            onSubmitResumes={handleResumeUpload}
            uploading={isUploading}
          />
        </section>

        <section className="mt-8 grid gap-6 xl:grid-cols-[1.1fr,0.9fr]">
          <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel backdrop-blur">
            <div className="flex items-start justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-cyan-100">
                  <Activity size={14} />
                  Processing view
                </div>
                <h2 className="mt-4 font-display text-3xl text-white">Run Screening</h2>
                <p className="mt-2 text-sm text-slate-400">Use the latest job intake and resume pool to score, shortlist, and generate interview-ready email drafts.</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-right">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Latest job</p>
                <p className="mt-2 text-sm font-semibold text-white">{dashboard?.latest_job_title || "No role uploaded"}</p>
              </div>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
                <div className="flex items-center gap-3 text-white">
                  <Files size={18} className="text-brand-300" />
                  <span className="font-semibold">Role selection</span>
                </div>
                <select
                  value={selectedJobId ?? ""}
                  onChange={(event) => setSelectedJobId(Number(event.target.value))}
                  className="mt-4 w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 text-sm text-white outline-none"
                >
                  <option value="">Choose a job description</option>
                  {jobs.map((job) => (
                    <option key={job.id} value={job.id}>
                      {job.title}
                    </option>
                  ))}
                </select>
              </div>

              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
                <div className="flex items-center gap-3 text-white">
                  <BrainCircuit size={18} className="text-cyan-300" />
                  <span className="font-semibold">Shortlist threshold</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={threshold}
                  onChange={(event) => setThreshold(Number(event.target.value))}
                  className="mt-5 w-full accent-brand-400"
                />
                <p className="mt-3 text-sm text-slate-300">{threshold}% match score cutoff</p>
              </div>

              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
                <div className="flex items-center gap-3 text-white">
                  <MailCheck size={18} className="text-amber-300" />
                  <span className="font-semibold">Interview drafts</span>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-400">Shortlisted candidates receive a generated interview invitation draft in their detail view.</p>
              </div>
            </div>

            <button
              onClick={handleRunScreening}
              disabled={isScreening}
              className="mt-6 inline-flex items-center gap-3 rounded-2xl bg-white px-5 py-3 font-semibold text-slate-950 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <PlayCircle size={18} />
              {isScreening ? "Running screening..." : "Run Screening"}
            </button>
          </div>

          <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Workflow</p>
            <div className="mt-6 space-y-5">
              {[
                "Upload one job description by text or file.",
                "Batch upload real PDF resumes.",
                "Run AI screening with shortlist threshold controls.",
                "Sort results and inspect each candidate breakdown.",
              ].map((step, index) => (
                <div key={step} className="flex items-start gap-4">
                  <div className="mt-0.5 flex h-9 w-9 items-center justify-center rounded-2xl bg-white/5 text-sm font-semibold text-white">
                    {index + 1}
                  </div>
                  <p className="text-sm leading-7 text-slate-300">{step}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-8">
          <ResultsTable
            candidates={filteredCandidates}
            screeningId={results.screening_id}
            search={search}
            setSearch={setSearch}
            shortlistedOnly={shortlistedOnly}
            setShortlistedOnly={setShortlistedOnly}
            sortBy={sortBy}
            setSortBy={setSortBy}
          />
        </section>
      </div>
    </main>
  );
}
