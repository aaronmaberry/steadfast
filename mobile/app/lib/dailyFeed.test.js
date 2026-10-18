"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const feedLib = require("./dailyFeed");

const DATES = ["2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06"];

function words(value) {
  return String(value || "").trim().split(/\s+/).filter(Boolean).length;
}

test("the daily screen reads the site feed and picks the Chicago day", function () {
  assert.equal(feedLib.feed.items.length > 5, true);
  const today = feedLib.pickDailyItem(feedLib.feed.items, "2026-10-02");
  assert.equal(today.date, "2026-10-02");
  assert.equal(today.silentTitle, "Keep sowing when the field is quiet");
  const later = feedLib.pickDailyItem(feedLib.feed.items, "2026-10-06");
  assert.equal(later.date, "2026-10-06");
});

test("October 2 through 6 use the longer reading and have no comment fields", function () {
  DATES.forEach(function (date) {
    const item = feedLib.feed.items.find(function (entry) { return entry.date === date; });
    assert.equal(item.body, item.carryBody);
    assert.ok(words(item.silentBody) >= 404, date);
    assert.equal(Object.hasOwn(item, "discussionQuestion"), false);
    assert.equal(Object.hasOwn(item, "teamReflection"), false);
    assert.equal(Object.hasOwn(item, "comments"), false);
    const prose = [item.silentBody, item.carryBody, item.prayer].join("\n");
    assert.equal(/[—–]| - /.test(prose), false);
    assert.equal(/\breal man\b/i.test(prose), false);
    assert.equal(/not just/i.test(prose), false);
    const blocks = feedLib.readingBlocks(item);
    assert.equal(blocks[1], item.verseRef + " NIV");
  });
});
