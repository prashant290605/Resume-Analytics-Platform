import { ArrowLeft, BriefcaseBusiness, CheckCircle2, Sparkles, XCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";

import { getCandidate } from "../lib/api";

export default function CandidateDetailPage() {
  const { resumeId } = useParams();
  const [searchParams] = useSearchParams();
  const screeningId = searchParams.get("screeningId");
  const [candidate, setCandidate] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!screeningId) {
      setError("Missing screening context.");
      return;
    }

    getCandidate(resumeId, screeningId)
      .then(setCandidate)
      .catch(() => setError("Unable to load candidate detail."));
  }, [resumeId, screeningId]);

  if (error) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">
        <div className="rounded-[2rem] border border-white/10 bg-slate-900/70 p-10 text-center shadow-panel">
          <p className="text-lg">{error}</p>
          <Link to="/" className="mt-6 inline-flex rounded-2xl bg-white px-5 py-3 font-semibold text-slate-950">
            Back to dashboard
          </Link>
        </div>
      </main>
    );
  }

  if (!candidate) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-300">
        Loading candidate profile...
      </main>
    );
  }

  const parsed = candidate.parsed_resume;
  const breakdown = candidate.match_breakdown;

  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,_#020617,_#0f172a)] px-4 py-6 text-ink sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <Link to="/" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white">
          <ArrowLeft size={16} />
          Back to dashboard
        </Link>

        <section className="mt-6 rounded-[2.25rem] border border-white/10 bg-slate-900/75 p-8 shadow-panel backdrop-blur">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Candidate profile</p>
              <h1 className="mt-3 font-display text-4xl text-white">{parsed.name}</h1>
              <p className="mt-3 text-slate-300">{parsed.email || "Email unavailable"}{parsed.phone ? ` • ${parsed.phone}` : ""}</p>
              <p className="mt-5 max-w-3xl text-sm leading-7 text-slate-300">{parsed.summary}</p>
            </div>
            <div className="min-w-72 rounded-[1.8rem] border border-brand-300/20 bg-brand-300/10 p-5">
              <p className="text-xs uppercase tracking-[0.24em] text-brand-100">Match score</p>
              <p className="mt-3 font-display text-5xl text-white">{candidate.score.toFixed(1)}%</p>
              <p className="mt-3 text-sm text-brand-50">{candidate.shortlisted ? "Shortlisted for next step" : "Below shortlist threshold"}</p>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[0.9fr,1.1fr]">
          <div className="space-y-6">
            <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel">
              <div className="flex items-center gap-3">
                <Sparkles size={18} className="text-brand-300" />
                <h2 className="font-display text-2xl text-white">Match Breakdown</h2>
              </div>
              <div className="mt-5 grid gap-3 sm:grid-cols-3">
                <Metric label="Semantic" value={`${breakdown.semantic_score.toFixed(1)}%`} />
                <Metric label="Skills" value={`${breakdown.skill_score.toFixed(1)}%`} />
                <Metric label="Experience" value={`${breakdown.experience_score.toFixed(1)}%`} />
              </div>
            </div>

            <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={18} className="text-brand-300" />
                <h2 className="font-display text-2xl text-white">Matched Skills</h2>
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                {breakdown.matched_skills?.length ? breakdown.matched_skills.map((skill) => (
                  <Tag key={skill} tone="green" label={skill} />
                )) : <p className="text-sm text-slate-500">No explicit skill matches detected.</p>}
              </div>
            </div>

            <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel">
              <div className="flex items-center gap-3">
                <XCircle size={18} className="text-rose-300" />
                <h2 className="font-display text-2xl text-white">Missing Skills</h2>
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                {breakdown.missing_skills?.length ? breakdown.missing_skills.map((skill) => (
                  <Tag key={skill} tone="rose" label={skill} />
                )) : <p className="text-sm text-slate-500">Role requirements are broadly covered.</p>}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel">
              <div className="flex items-center gap-3">
                <BriefcaseBusiness size={18} className="text-cyan-300" />
                <h2 className="font-display text-2xl text-white">Parsed Resume</h2>
              </div>
              <InfoBlock title="Education" body={parsed.education} />
              <InfoBlock title="Work experience" body={parsed.work_experience} />
              <InfoBlock title="Skills" body={parsed.skills.join(", ")} />
              <InfoBlock title="Certifications" body={(parsed.certifications || []).join(", ") || "No certifications detected"} />
            </div>

            <div className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Interview draft</p>
              <pre className="mt-4 whitespace-pre-wrap rounded-[1.5rem] bg-slate-950/60 p-5 text-sm leading-7 text-slate-200">
                {candidate.generated_email || "This candidate was not shortlisted, so no interview draft was generated."}
              </pre>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-slate-950/55 p-4">
      <p className="text-xs uppercase tracking-[0.22em] text-slate-500">{label}</p>
      <p className="mt-3 font-display text-3xl text-white">{value}</p>
    </div>
  );
}

function Tag({ label, tone }) {
  const tones = {
    green: "border-brand-300/25 bg-brand-300/10 text-brand-100",
    rose: "border-rose-300/20 bg-rose-300/10 text-rose-100",
  };
  return <span className={`rounded-full border px-3 py-1 text-xs ${tones[tone]}`}>{label}</span>;
}

function InfoBlock({ title, body }) {
  return (
    <div className="mt-5 rounded-[1.5rem] border border-white/10 bg-slate-950/55 p-5">
      <p className="text-xs uppercase tracking-[0.24em] text-slate-500">{title}</p>
      <p className="mt-3 text-sm leading-7 text-slate-300">{body || "No information extracted."}</p>
    </div>
  );
}
