"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const engage = require("./dailyEngage");

test("share URL and the local like stay on the device adapter", async function () {
  assert.equal(
    engage.buildDailyShareUrl("https://www.walksteadfast.com", "2026-10-02"),
    "https://www.walksteadfast.com/daily?day=2026-10-02"
  );
  const storage = engage.memoryStorage();
  engage.setAdapter(engage.createStorageAdapter(storage));
  assert.equal(await engage.getLike("2026-10-02"), false);
  assert.equal(await engage.setLike("2026-10-02", true), true);
  assert.equal(await engage.getLike("2026-10-03"), false);
  assert.equal(await engage.setLike("2026-10-02", false), false);
  const raw = JSON.parse(storage.getItem("steadfast.daily.likes"));
  assert.equal(Object.hasOwn(raw, "2026-10-02"), false);
  engage.setAdapter(null);
});

test("the like adapter ships with no comment store", function () {
  const source = require("node:fs").readFileSync(require("node:path").join(__dirname, "dailyEngage.js"), "utf8");
  assert.equal(/getComments|addComment|discussionQuestion|sample comment|lorem|Great word/i.test(source), false);
});
