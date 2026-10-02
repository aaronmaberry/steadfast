"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const engage = require("./dailyEngage");

test("share URL and local comments stay on the device adapter", async function () {
  assert.equal(
    engage.buildDailyShareUrl("https://www.walksteadfast.com", "2026-10-02"),
    "https://www.walksteadfast.com/daily?day=2026-10-02"
  );
  const storage = engage.memoryStorage();
  engage.setAdapter(engage.createStorageAdapter(storage));
  assert.deepEqual(await engage.getComments("2026-10-02"), []);
  const saved = await engage.addComment("2026-10-02", {
    name: "Aaron",
    text: "I will stay on the row."
  });
  assert.equal((await engage.getComments("2026-10-03")).length, 0);
  assert.equal((await engage.reportComment("2026-10-02", saved.id)).reported, true);
  const raw = JSON.parse(storage.getItem("steadfast.daily.comments"));
  assert.equal(Array.isArray(raw["2026-10-02"]), true);
  assert.equal(raw["2026-10-02"].length, 1);
  engage.setAdapter(null);
});

test("the adapter ships with no seeded comments", function () {
  const source = require("node:fs").readFileSync(require("node:path").join(__dirname, "dailyEngage.js"), "utf8");
  assert.equal(/sample comment|lorem|Great word/i.test(source), false);
});
