"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const feedLib = require("./dailyFeed");

const DATES = ["2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06"];
const QUESTIONS = {
  "2026-10-02": "What good are you most tempted to drop today?",
  "2026-10-03": "What has been living in you this week that your house has had to carry?",
  "2026-10-04": "What keeps you from staying long enough for one person to find you?",
  "2026-10-05": "Which have you been skipping: justice, mercy, or a humble walk?",
  "2026-10-06": "Who will you ask today where you are dull?"
};

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

test("October 2 through 6 use the longer reading and a real discussion question", function () {
  DATES.forEach(function (date) {
    const item = feedLib.feed.items.find(function (entry) { return entry.date === date; });
    assert.equal(item.body, item.carryBody);
    assert.ok(words(item.silentBody) >= 404, date);
    assert.equal(item.discussionQuestion, QUESTIONS[date]);
    assert.equal(Object.hasOwn(item, "comments"), false);
    assert.equal(/[—–]| - /.test(item.discussionQuestion), false);
    assert.equal(/\breal man\b/i.test(item.discussionQuestion), false);
    const blocks = feedLib.readingBlocks(item);
    assert.equal(blocks.includes(item.discussionQuestion), false);
    assert.equal(blocks[1], item.verseRef + " NIV");
  });
});
