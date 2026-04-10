import { ArrowUpDown, ChevronRight, Search, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

export default function ResultsTable({
  candidates,
  screeningId,
  search,
  setSearch,
  shortlistedOnly,
  setShortlistedOnly,
  sortBy,
  setSortBy,
}) {
  return (
    <section className="rounded-[2rem] border border-white/10 bg-slate-900/75 p-6 shadow-panel backdrop-blur">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-brand-300/20 bg-brand-300/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-brand-200">
            <Sparkles size={14} />
            Ranked candidates
          </div>
          <h2 className="mt-4 font-display text-3xl text-white">Screening Results</h2>
          <p className="mt-2 text-sm text-slate-400">Sort, filter, and inspect every candidate with a clear match breakdown.</p>
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          <label className="flex items-center gap-2 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-slate-300">
            <Search size={16} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              className="w-full bg-transparent text-sm outline-none"
              placeholder="Search candidates"
            />
          </label>
          <button
            onClick={() => setShortlistedOnly((current) => !current)}
            className={`rounded-2xl border px-4 py-3 text-sm font-semibold transition ${
              shortlistedOnly
                ? "border-brand-300/30 bg-brand-300/15 text-brand-100"
                : "border-white/10 bg-slate-950/60 text-slate-300"
            }`}
          >
            {shortlistedOnly ? "Showing shortlist" : "Show shortlisted only"}
          </button>
          <label className="flex items-center gap-2 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-slate-300">
            <ArrowUpDown size={16} />
            <select value={sortBy} onChange={(event) => setSortBy(event.target.value)} className="w-full bg-transparent text-sm outline-none">
              <option value="score">Sort by score</option>
              <option value="experience">Sort by experience</option>
              <option value="name">Sort by name</option>
            </select>
          </label>
        </div>
      </div>

      <div className="mt-6 overflow-hidden rounded-[1.6rem] border border-white/10">
        <div className="hidden grid-cols-[1.5fr,0.7fr,1.2fr,0.8fr,0.8fr] gap-4 bg-slate-950/80 px-6 py-4 text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 md:grid">
          <span>Candidate</span>
          <span>Score</span>
          <span>Skills</span>
          <span>Experience</span>
          <span>Action</span>
        </div>
        <div className="divide-y divide-white/5">
          {candidates.length === 0 ? (
            <div className="px-6 py-16 text-center text-sm text-slate-500">No candidates yet. Upload resumes and run screening to see ranked results.</div>
          ) : (
            candidates.map((candidate) => (
              <div key={candidate.resume_id} className="grid gap-4 px-6 py-5 md:grid-cols-[1.5fr,0.7fr,1.2fr,0.8fr,0.8fr] md:items-center">
                <div>
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-brand-400/30 to-cyan-300/20" />
                    <div>
                      <p className="font-semibold text-white">{candidate.name}</p>
                      <p className="text-sm text-slate-400">{candidate.email || "Email unavailable"}</p>
                    </div>
                  </div>
                  {candidate.shortlisted && (
                    <span className="mt-3 inline-flex rounded-full border border-brand-300/25 bg-brand-300/10 px-3 py-1 text-xs font-semibold text-brand-100">
                      Shortlisted
                    </span>
                  )}
                </div>
                <div>
                  <p className="font-display text-2xl text-white">{candidate.score.toFixed(1)}</p>
                  <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Match score</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {candidate.skills.slice(0, 5).map((skill) => (
                    <span key={`${candidate.resume_id}-${skill}`} className="rounded-full border border-cyan-300/15 bg-cyan-300/10 px-3 py-1 text-xs text-cyan-100">
                      {skill}
                    </span>
                  ))}
                </div>
                <div>
                  <p className="font-semibold text-white">{candidate.years_experience.toFixed(1)} yrs</p>
                  <p className="text-sm text-slate-400">Professional experience</p>
                </div>
                <div>
                  <Link
                    to={`/candidates/${candidate.resume_id}?screeningId=${screeningId}`}
                    className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white transition hover:bg-white/10"
                  >
                    View detail
                    <ChevronRight size={16} />
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
}
