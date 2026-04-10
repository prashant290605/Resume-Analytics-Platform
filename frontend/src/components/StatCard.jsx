export default function StatCard({ eyebrow, value, label, tone = "emerald" }) {
  const tones = {
    emerald: "from-brand-400/30 to-brand-500/5 border-brand-300/20",
    amber: "from-amber-400/20 to-amber-500/5 border-amber-300/20",
    cyan: "from-cyan-400/20 to-cyan-500/5 border-cyan-300/20",
    rose: "from-rose-400/20 to-rose-500/5 border-rose-300/20",
  };

  return (
    <div
      className={`rounded-3xl border bg-slate-900/80 p-6 shadow-panel backdrop-blur ${tones[tone]}`}
    >
      <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">{eyebrow}</p>
      <div className="mt-5 flex items-end justify-between gap-4">
        <div>
          <p className="font-display text-4xl text-white">{value}</p>
          <p className="mt-2 text-sm text-slate-300">{label}</p>
        </div>
      </div>
    </div>
  );
}
