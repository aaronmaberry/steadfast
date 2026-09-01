import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import express from "express";
import { createGoalsRouter, GoalStore } from "./goals.js";

function makeApp() {
  const app = express();
  app.use(express.json());
  app.use("/api/goals", createGoalsRouter(new GoalStore([])));
  return app;
}

describe("goals API", () => {
  let app: ReturnType<typeof makeApp>;

  beforeEach(() => {
    app = makeApp();
  });

  it("starts empty", async () => {
    const res = await request(app).get("/api/goals");
    expect(res.status).toBe(200);
    expect(res.body.goals).toEqual([]);
  });

  it("creates a goal", async () => {
    const res = await request(app)
      .post("/api/goals")
      .send({ title: "Meditate", cadence: "daily" });
    expect(res.status).toBe(201);
    expect(res.body.goal).toMatchObject({
      title: "Meditate",
      cadence: "daily",
      streak: 0,
      completedToday: false,
    });
    expect(res.body.goal.id).toBeTruthy();
  });

  it("rejects an empty title", async () => {
    const res = await request(app).post("/api/goals").send({ title: "   " });
    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/title is required/i);
  });

  it("toggles completion and adjusts the streak", async () => {
    const created = await request(app)
      .post("/api/goals")
      .send({ title: "Stretch" });
    const id = created.body.goal.id;

    const toggled = await request(app).post(`/api/goals/${id}/toggle`);
    expect(toggled.status).toBe(200);
    expect(toggled.body.goal.completedToday).toBe(true);
    expect(toggled.body.goal.streak).toBe(1);

    const untoggled = await request(app).post(`/api/goals/${id}/toggle`);
    expect(untoggled.body.goal.completedToday).toBe(false);
    expect(untoggled.body.goal.streak).toBe(0);
  });

  it("deletes a goal", async () => {
    const created = await request(app)
      .post("/api/goals")
      .send({ title: "Journal" });
    const id = created.body.goal.id;

    const del = await request(app).delete(`/api/goals/${id}`);
    expect(del.status).toBe(204);

    const list = await request(app).get("/api/goals");
    expect(list.body.goals).toEqual([]);
  });

  it("returns 404 when toggling a missing goal", async () => {
    const res = await request(app).post("/api/goals/does-not-exist/toggle");
    expect(res.status).toBe(404);
  });
});
