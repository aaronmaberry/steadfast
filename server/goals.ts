import { Router } from "express";
import { randomUUID } from "node:crypto";

export interface Goal {
  id: string;
  title: string;
  cadence: "daily" | "weekly";
  streak: number;
  completedToday: boolean;
  createdAt: string;
}

export type NewGoalInput = {
  title: unknown;
  cadence?: unknown;
};

const CADENCES = ["daily", "weekly"] as const;

function seedGoals(): Goal[] {
  const now = new Date().toISOString();
  return [
    {
      id: randomUUID(),
      title: "Read for 20 minutes",
      cadence: "daily",
      streak: 5,
      completedToday: true,
      createdAt: now,
    },
    {
      id: randomUUID(),
      title: "Run 5km",
      cadence: "weekly",
      streak: 2,
      completedToday: false,
      createdAt: now,
    },
  ];
}

/**
 * In-memory store. Kept intentionally simple so the dev environment runs with
 * zero external services; swap for a real database when persistence is needed.
 */
export class GoalStore {
  private goals: Goal[];

  constructor(initial?: Goal[]) {
    this.goals = initial ?? seedGoals();
  }

  list(): Goal[] {
    return [...this.goals].sort((a, b) =>
      a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : 0,
    );
  }

  create(input: NewGoalInput): Goal {
    const title = typeof input.title === "string" ? input.title.trim() : "";
    if (!title) {
      throw new ValidationError("A goal title is required.");
    }
    const cadence = CADENCES.includes(input.cadence as (typeof CADENCES)[number])
      ? (input.cadence as Goal["cadence"])
      : "daily";

    const goal: Goal = {
      id: randomUUID(),
      title,
      cadence,
      streak: 0,
      completedToday: false,
      createdAt: new Date().toISOString(),
    };
    this.goals.push(goal);
    return goal;
  }

  toggle(id: string): Goal | undefined {
    const goal = this.goals.find((g) => g.id === id);
    if (!goal) return undefined;
    goal.completedToday = !goal.completedToday;
    goal.streak = Math.max(0, goal.streak + (goal.completedToday ? 1 : -1));
    return goal;
  }

  remove(id: string): boolean {
    const before = this.goals.length;
    this.goals = this.goals.filter((g) => g.id !== id);
    return this.goals.length < before;
  }
}

export class ValidationError extends Error {}

export function createGoalsRouter(store: GoalStore): Router {
  const router = Router();

  router.get("/", (_req, res) => {
    res.json({ goals: store.list() });
  });

  router.post("/", (req, res) => {
    try {
      const goal = store.create(req.body ?? {});
      res.status(201).json({ goal });
    } catch (err) {
      if (err instanceof ValidationError) {
        res.status(400).json({ error: err.message });
        return;
      }
      throw err;
    }
  });

  router.post("/:id/toggle", (req, res) => {
    const goal = store.toggle(req.params.id);
    if (!goal) {
      res.status(404).json({ error: "Goal not found." });
      return;
    }
    res.json({ goal });
  });

  router.delete("/:id", (req, res) => {
    const removed = store.remove(req.params.id);
    if (!removed) {
      res.status(404).json({ error: "Goal not found." });
      return;
    }
    res.status(204).end();
  });

  return router;
}
