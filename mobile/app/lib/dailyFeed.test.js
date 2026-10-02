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
const REFLECTIONS = {
  "2026-10-02": "The quiet field is not a verdict on the work. Name the small good you are most tempted to drop, and do it once more before dark. The harvest date belongs to God. You keep the next faithful step.",
  "2026-10-03": "What lives in you walks out the door with you, and the people in your house meet it first. Name one thing that has been taking space this week, in words plain enough that you cannot decorate them. Ask the Lord to take it, and close the door you have been leaving open.",
  "2026-10-04": "You cannot spur a brother you never stay long enough to find. Take your seat today, and stay ten minutes after the gathering ends. Tell one person, by name, one specific good you have seen in him.",
  "2026-10-05": "God has already shown what is good, and a longer list will not hide the part you skip. Name that one out loud before you decorate it. Do one concrete act of it before dark, where the people who live with you can see it.",
  "2026-10-06": "A brother who is only allowed to encourage you will not put an edge on you. Ask one man where you are dull, and let him finish the whole answer. Say thank you before you say anything else."
};

function sentences(value) {
  return String(value || "").split(/(?<=[.!?])\s+/).map(function (part) { return part.trim(); }).filter(Boolean);
}

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
    assert.equal(item.teamReflection, REFLECTIONS[date]);
    const reflectionSentences = sentences(item.teamReflection);
    assert.ok(reflectionSentences.length >= 2 && reflectionSentences.length <= 4, date + " sentences " + reflectionSentences.length);
    assert.equal(Object.hasOwn(item, "comments"), false);
    const teamCopy = item.discussionQuestion + "\n" + item.teamReflection;
    assert.equal(/[—–]| - /.test(teamCopy), false);
    assert.equal(/\breal man\b/i.test(teamCopy), false);
    assert.equal(/not just/i.test(teamCopy), false);
    const blocks = feedLib.readingBlocks(item);
    assert.equal(blocks.includes(item.discussionQuestion), false);
    assert.equal(blocks.includes(item.teamReflection), false);
    assert.equal(blocks[1], item.verseRef + " NIV");
  });
});
