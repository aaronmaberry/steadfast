"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const { buildSharePayload, shareDetail } = require("./shareDetail");

test("share payload keeps the title and the link when both exist", function () {
  assert.deepEqual(
    buildSharePayload("Keep sowing when the field is quiet", "https://www.walksteadfast.com/daily?day=2026-10-02"),
    {
      title: "Keep sowing when the field is quiet",
      message: "Keep sowing when the field is quiet\nhttps://www.walksteadfast.com/daily?day=2026-10-02",
      url: "https://www.walksteadfast.com/daily?day=2026-10-02"
    }
  );
});

test("share payload drops a missing link", function () {
  assert.deepEqual(buildSharePayload("Name the drift in your own house.", "  "), {
    title: "Name the drift in your own house.",
    message: "Name the drift in your own house."
  });
});

test("shareDetail hands the payload to the native share sheet", async function () {
  let seen = null;
  const status = await shareDetail("Let a man correct you", "https://www.walksteadfast.com/daily?day=2026-10-06", function (payload) {
    seen = payload;
    return { action: "sharedAction" };
  });
  assert.equal(status, "shared");
  assert.equal(seen.url, "https://www.walksteadfast.com/daily?day=2026-10-06");
  assert.equal(seen.title, "Let a man correct you");
});

test("a dismissed share sheet does not fall through to copy", async function () {
  const status = await shareDetail("Daily Walk", "https://www.walksteadfast.com/daily?day=2026-10-02", function () {
    return { action: "dismissedAction" };
  });
  assert.equal(status, "dismissed");
});

test("detail screens mount the floating close and share header", function () {
  const fs = require("node:fs");
  const path = require("node:path");
  const header = fs.readFileSync(path.join(__dirname, "../components/DetailHeader.js"), "utf8");
  const reader = fs.readFileSync(path.join(__dirname, "../screens/DailyReader.js"), "utf8");
  const session = fs.readFileSync(path.join(__dirname, "../screens/SessionDetail.js"), "utf8");
  assert.match(header, /width: 44/);
  assert.match(header, /borderWidth: 1/);
  assert.match(header, /position: 'absolute'/);
  assert.match(reader, /DetailHeader/);
  assert.match(session, /DetailHeader/);
  assert.equal(reader.includes("styles.scrim"), false);
  assert.equal(reader.includes("scrimBand"), false);
  assert.equal(session.includes("styles.scrim"), false);
});
