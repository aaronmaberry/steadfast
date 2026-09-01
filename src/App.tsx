import { useEffect, useMemo, useState } from "react";
import { api, type Goal } from "./api";

export function App() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [title, setTitle] = useState("");
  const [cadence, setCadence] = useState<Goal["cadence"]>("daily");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let active = true;
    api
      .listGoals()
      .then((data) => {
        if (active) setGoals(data);
      })
      .catch((err: unknown) => {
        if (active) setError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const stats = useMemo(() => {
    const total = goals.length;
    const done = goals.filter((g) => g.completedToday).length;
    const bestStreak = goals.reduce((max, g) => Math.max(max, g.streak), 0);
    return { total, done, bestStreak };
  }, [goals]);

  async function handleCreate(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    setSubmitting(true);
    setError(null);
    try {
      const goal = await api.createGoal({ title: trimmed, cadence });
      setGoals((prev) => [goal, ...prev]);
      setTitle("");
      setCadence("daily");
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggle(id: string) {
    try {
      const updated = await api.toggleGoal(id);
      setGoals((prev) => prev.map((g) => (g.id === id ? updated : g)));
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  async function handleDelete(id: string) {
    const snapshot = goals;
    setGoals((prev) => prev.filter((g) => g.id !== id));
    try {
      await api.deleteGoal(id);
    } catch (err) {
      setGoals(snapshot);
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  return (
    <div className="min-h-full bg-gradient-to-b from-slate-950 via-slate-950 to-slate-900">
      <div className="mx-auto flex min-h-full max-w-3xl flex-col gap-8 px-6 py-12">
        <header className="flex flex-col gap-2">
          <div className="flex items-center gap-3">
            <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 to-cyan-500 text-xl font-black text-slate-950 shadow-lg shadow-emerald-500/20">
              S
            </span>
            <div>
              <h1 className="text-2xl font-extrabold tracking-tight">
                Steadfast
              </h1>
              <p className="text-sm text-slate-400">
                Show up every day. Keep the streak alive.
              </p>
            </div>
          </div>
        </header>

        <section className="grid grid-cols-3 gap-4">
          <StatCard label="Goals" value={stats.total} />
          <StatCard label="Done today" value={`${stats.done}/${stats.total}`} />
          <StatCard label="Best streak" value={`${stats.bestStreak}🔥`} />
        </section>

        <form
          onSubmit={handleCreate}
          className="flex flex-col gap-3 rounded-2xl border border-slate-800 bg-slate-900/60 p-4 sm:flex-row sm:items-center"
        >
          <input
            aria-label="Goal title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Add a new goal…"
            className="flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-400/30"
          />
          <select
            aria-label="Cadence"
            value={cadence}
            onChange={(e) => setCadence(e.target.value as Goal["cadence"])}
            className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm outline-none transition focus:border-emerald-400"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
          <button
            type="submit"
            disabled={submitting || !title.trim()}
            className="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {submitting ? "Adding…" : "Add goal"}
          </button>
        </form>

        {error && (
          <div
            role="alert"
            className="rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200"
          >
            {error}
          </div>
        )}

        <section className="flex flex-col gap-3">
          {loading ? (
            <p className="text-center text-sm text-slate-500">Loading goals…</p>
          ) : goals.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-800 py-12 text-center text-slate-500">
              No goals yet. Add your first one above.
            </div>
          ) : (
            goals.map((goal) => (
              <GoalRow
                key={goal.id}
                goal={goal}
                onToggle={() => handleToggle(goal.id)}
                onDelete={() => handleDelete(goal.id)}
              />
            ))
          )}
        </section>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs uppercase tracking-wide text-slate-500">
        {label}
      </div>
    </div>
  );
}

function GoalRow({
  goal,
  onToggle,
  onDelete,
}: {
  goal: Goal;
  onToggle: () => void;
  onDelete: () => void;
}) {
  return (
    <div className="flex animate-fade-in items-center gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4 transition hover:border-slate-700">
      <button
        onClick={onToggle}
        aria-label={goal.completedToday ? "Mark incomplete" : "Mark complete"}
        aria-pressed={goal.completedToday}
        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition ${
          goal.completedToday
            ? "border-emerald-400 bg-emerald-400 text-slate-950"
            : "border-slate-600 text-transparent hover:border-emerald-400"
        }`}
      >
        ✓
      </button>
      <div className="flex-1">
        <div
          className={`font-medium ${goal.completedToday ? "text-slate-400 line-through" : ""}`}
        >
          {goal.title}
        </div>
        <div className="mt-0.5 flex items-center gap-2 text-xs text-slate-500">
          <span className="rounded-full bg-slate-800 px-2 py-0.5 capitalize">
            {goal.cadence}
          </span>
          <span>🔥 {goal.streak} streak</span>
        </div>
      </div>
      <button
        onClick={onDelete}
        aria-label={`Delete ${goal.title}`}
        className="rounded-lg px-2 py-1 text-slate-500 transition hover:bg-rose-500/10 hover:text-rose-300"
      >
        ✕
      </button>
    </div>
  );
}
