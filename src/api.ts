export interface Goal {
  id: string;
  title: string;
  cadence: "daily" | "weekly";
  streak: number;
  completedToday: boolean;
  createdAt: string;
}

async function parse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body?.error) message = body.error;
    } catch {
      // ignore non-JSON error bodies
    }
    throw new Error(message);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  async listGoals(): Promise<Goal[]> {
    const data = await parse<{ goals: Goal[] }>(await fetch("/api/goals"));
    return data.goals;
  },

  async createGoal(input: {
    title: string;
    cadence: Goal["cadence"];
  }): Promise<Goal> {
    const data = await parse<{ goal: Goal }>(
      await fetch("/api/goals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      }),
    );
    return data.goal;
  },

  async toggleGoal(id: string): Promise<Goal> {
    const data = await parse<{ goal: Goal }>(
      await fetch(`/api/goals/${id}/toggle`, { method: "POST" }),
    );
    return data.goal;
  },

  async deleteGoal(id: string): Promise<void> {
    await parse<void>(await fetch(`/api/goals/${id}`, { method: "DELETE" }));
  },
};
