import { FileText, UploadCloud } from "lucide-react";

export default function UploadPanel({
  defaultJds,
  selectedRoleMode,
  setSelectedRoleMode,
  selectedDefaultRole,
  setSelectedDefaultRole,
  jobTitle,
  setJobTitle,
  jobDescription,
  setJobDescription,
  jobFile,
  setJobFile,
  resumeFiles,
  setResumeFiles,
  currentBatchId,
  batchMode,
  setBatchMode,
  onCreateBatch,
  uploadProgress,
  onSubmitJob,
  onSubmitResumes,
  uploading,
}) {
  const addResumeFiles = (incomingFiles) => {
    const nextFiles = Array.from(incomingFiles || []);
    setResumeFiles((current) => [...current, ...nextFiles]);
  };

  return (
    <section className="grid gap-6 xl:grid-cols-[1.2fr,0.8fr]">
      <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-brand-400/15 p-3 text-brand-300">
            <FileText size={20} />
          </div>
          <div>
            <h2 className="font-display text-2xl text-white">Job Intake</h2>
            <p className="text-sm text-slate-400">Paste a job description or upload a file and extract recruiter-ready requirements.</p>
          </div>
        </div>

        <div className="mt-6 grid gap-4">
          <label className="grid gap-2">
            <span className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Choose a role (optional)</span>
            <select
              value={selectedRoleMode}
              onChange={(event) => setSelectedRoleMode(event.target.value)}
              className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-brand-300"
            >
              <option value="custom">Custom input</option>
              {defaultJds.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.title}
                </option>
              ))}
            </select>
          </label>
          {selectedRoleMode !== "custom" && (
            <label className="grid gap-2">
              <span className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Selected default role</span>
              <select
                value={selectedDefaultRole}
                onChange={(event) => setSelectedDefaultRole(event.target.value)}
                className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-brand-300"
              >
                {defaultJds.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.title}
                  </option>
                ))}
              </select>
            </label>
          )}
          <input
            className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-brand-300"
            value={jobTitle}
            onChange={(event) => setJobTitle(event.target.value)}
            placeholder="Role title"
          />
          <textarea
            className="min-h-40 rounded-3xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-brand-300"
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="Paste the full job description here"
          />
          <label className="flex cursor-pointer items-center gap-3 rounded-2xl border border-dashed border-white/15 bg-slate-950/40 px-4 py-4 text-sm text-slate-300">
            <UploadCloud size={18} className="text-brand-300" />
            <span>{jobFile ? jobFile.name : "Upload a TXT or PDF job brief"}</span>
            <input
              type="file"
              className="hidden"
              accept=".txt,.pdf"
              onChange={(event) => setJobFile(event.target.files?.[0] ?? null)}
            />
          </label>
          <button
            onClick={onSubmitJob}
            disabled={uploading}
            className="rounded-2xl bg-brand-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-brand-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Save Job Description
          </button>
        </div>
      </div>

      <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-cyan-400/15 p-3 text-cyan-300">
            <UploadCloud size={20} />
          </div>
          <div>
            <h2 className="font-display text-2xl text-white">Resume Uploads</h2>
            <p className="text-sm text-slate-400">Drag, drop, and batch upload real PDF resumes.</p>
          </div>
        </div>

        <div className="mt-6 rounded-3xl border border-white/10 bg-slate-950/45 p-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Hiring batch</p>
              <p className="mt-2 text-sm text-white">{currentBatchId ? `Current batch ID: ${currentBatchId}` : "No active batch selected"}</p>
            </div>
            <button
              onClick={onCreateBatch}
              disabled={uploading}
              className="rounded-2xl border border-brand-300/30 bg-brand-300/10 px-4 py-2 text-sm font-semibold text-brand-100 transition hover:bg-brand-300/20 disabled:opacity-50"
            >
              Start New Hiring Batch
            </button>
          </div>

          <label className="mt-4 grid gap-2">
            <span className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Upload target</span>
            <select
              value={batchMode}
              onChange={(event) => setBatchMode(event.target.value)}
              className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-brand-300"
            >
              <option value="current">Add to existing batch</option>
              <option value="new">Start new batch before upload</option>
            </select>
          </label>
        </div>

        <label
          className="mt-6 flex min-h-48 cursor-pointer flex-col items-center justify-center rounded-[1.75rem] border border-dashed border-white/15 bg-slate-950/60 px-6 text-center text-slate-300"
          onDragOver={(event) => event.preventDefault()}
          onDrop={(event) => {
            event.preventDefault();
            addResumeFiles(event.dataTransfer.files);
          }}
        >
          <UploadCloud size={30} className="text-brand-300" />
          <p className="mt-4 text-base font-semibold text-white">Drop multiple PDF resumes here</p>
          <p className="mt-2 text-sm text-slate-400">Or click to browse one or many candidate files</p>
          <input
            type="file"
            multiple
            accept=".pdf"
            className="hidden"
            onChange={(event) => addResumeFiles(event.target.files)}
          />
        </label>

        <div className="mt-4 max-h-36 space-y-2 overflow-auto pr-1">
          {resumeFiles.length === 0 ? (
            <p className="text-sm text-slate-500">No resumes queued yet.</p>
          ) : (
            resumeFiles.map((file, index) => (
              <div key={`${file.name}-${index}`} className="rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3 text-sm text-slate-200">
                {file.name}
              </div>
            ))
          )}
        </div>

        <div className="mt-5">
          <div className="mb-2 flex items-center justify-between text-xs uppercase tracking-[0.24em] text-slate-500">
            <span>Upload progress</span>
            <span>{uploadProgress}%</span>
          </div>
          <div className="h-2 rounded-full bg-slate-800">
            <div className="h-2 rounded-full bg-gradient-to-r from-cyan-300 to-brand-400 transition-all" style={{ width: `${uploadProgress}%` }} />
          </div>
        </div>

        <button
          onClick={onSubmitResumes}
          disabled={uploading || resumeFiles.length === 0}
          className="mt-5 w-full rounded-2xl bg-white px-5 py-3 font-semibold text-slate-950 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Upload Resumes
        </button>
      </div>
    </section>
  );
}
