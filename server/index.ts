import express from "express";
import { createGoalsRouter, GoalStore } from "./goals.js";

const app = express();
app.use(express.json());

const store = new GoalStore();

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", uptime: process.uptime() });
});

app.use("/api/goals", createGoalsRouter(store));

export { app };

const PORT = Number(process.env.API_PORT ?? 3001);

// Only listen when run directly (not when imported by tests).
if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  app.listen(PORT, () => {
    console.log(`[steadfast] API listening on http://localhost:${PORT}`);
  });
}
