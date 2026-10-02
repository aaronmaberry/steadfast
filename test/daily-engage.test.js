"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const engage = require("../daily-engage");

const AVG_SILENT = 202;
const AVG_CHALLENGE = 105;
const AVG_PRAYER = 44;
const DATES = ["2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06"];
const QUESTIONS = {
  "2026-10-02": "What good are you most tempted to drop today?",
  "2026-10-03": "What has been living in you this week that your house has had to carry?",
  "2026-10-04": "What keeps you from staying long enough for one person to find you?",
  "2026-10-05": "Which have you been skipping: justice, mercy, or a humble walk?",
  "2026-10-06": "Who will you ask today where you are dull?"
};
const VERSES = {
  "2026-10-02": ["Galatians 6:9", "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up."],
  "2026-10-03": ["Proverbs 4:23", "Above all else, guard your heart, for everything you do flows from it."],
  "2026-10-04": ["Hebrews 10:24-25", "Let us consider how we may spur one another on toward love and good deeds, not giving up meeting together."],
  "2026-10-05": ["Micah 6:8", "And what does the Lord require of you? To act justly and to love mercy and to walk humbly with your God."],
  "2026-10-06": ["Proverbs 27:17", "As iron sharpens iron, so one person sharpens another."]
};

function words(value) {
  return String(value || "").trim().split(/\s+/).filter(Boolean).length;
}

test("share URL uses the daily deep link", function () {
  assert.equal(
    engage.buildDailyShareUrl("https://www.walksteadfast.com", "2026-10-02"),
    "https://www.walksteadfast.com/daily?day=2026-10-02"
  );
  assert.equal(
    engage.buildDailyShareUrl("https://www.walksteadfast.com/", "2026-10-06"),
    "https://www.walksteadfast.com/daily?day=2026-10-06"
  );
  assert.throws(function () {
    engage.buildDailyShareUrl("https://www.walksteadfast.com", "10/02/2026");
  });
});

test("day parser accepts a query param or a hash", function () {
  assert.equal(engage.parseDailyDay("?day=2026-10-02", ""), "2026-10-02");
  assert.equal(engage.parseDailyDay("", "#day=2026-10-03"), "2026-10-03");
  assert.equal(engage.parseDailyDay("", "#2026-10-04"), "2026-10-04");
  assert.equal(engage.parseDailyDay("?day=2026-10-02", "#day=2026-10-03"), "2026-10-02");
  assert.equal(engage.parseDailyDay("", "#nope"), null);
});

test("local like and comments stay on the device store, per date", async function () {
  const storage = engage.memoryStorage();
  const adapter = engage.createStorageAdapter(storage);
  engage.setAdapter(adapter);
  assert.equal(await engage.getLike("2026-10-02"), false);
  assert.equal(await engage.setLike("2026-10-02", true), true);
  assert.equal(await engage.setLike("2026-10-03", false), false);
  assert.equal(await engage.getLike("2026-10-02"), true);
  assert.equal(await engage.getLike("2026-10-03"), false);
  assert.deepEqual(await engage.getComments("2026-10-02"), []);
  await engage.setDisplayName("  Aaron  ");
  assert.equal(await engage.getDisplayName(), "Aaron");
  const saved = await engage.addComment("2026-10-02", {
    name: "Aaron",
    text: "The row is still mine."
  });
  assert.equal(saved.name, "Aaron");
  assert.equal(saved.text, "The row is still mine.");
  assert.equal(saved.reported, false);
  assert.equal(typeof saved.id, "string");
  assert.equal(typeof saved.createdAt, "number");
  const list = await engage.getComments("2026-10-02");
  assert.equal(list.length, 1);
  assert.equal(list[0].text, "The row is still mine.");
  assert.deepEqual(await engage.getComments("2026-10-03"), []);
  const reported = await engage.reportComment("2026-10-02", saved.id);
  assert.equal(reported.reported, true);
  assert.equal((await engage.getComments("2026-10-02"))[0].reported, true);
  assert.equal(await engage.reportComment("2026-10-02", "missing"), null);
  await assert.rejects(function () {
    return engage.addComment("2026-10-02", { name: "  ", text: "Hello" });
  });
  await assert.rejects(function () {
    return engage.addComment("2026-10-02", { name: "Aaron", text: "   " });
  });
  const rawLikes = JSON.parse(storage.getItem("steadfast.daily.likes"));
  assert.equal(rawLikes["2026-10-02"], true);
  assert.equal(Object.hasOwn(rawLikes, "2026-10-03"), false);
  const rawComments = JSON.parse(storage.getItem("steadfast.daily.comments"));
  assert.equal(rawComments["2026-10-02"][0].name, "Aaron");
  engage.setAdapter(null);
});

test("relative time uses short labels", function () {
  const now = Date.UTC(2026, 9, 2, 15, 0, 0);
  assert.equal(engage.formatRelativeTime(now - 20 * 1000, now), "just now");
  assert.equal(engage.formatRelativeTime(now - 5 * 60 * 1000, now), "5m ago");
  assert.equal(engage.formatRelativeTime(now - 2 * 60 * 60 * 1000, now), "2h ago");
  assert.equal(engage.formatRelativeTime(now - 3 * 24 * 60 * 60 * 1000, now), "3d ago");
  assert.equal(engage.formatRelativeTime(now - 14 * 24 * 60 * 60 * 1000, now), "2w ago");
  assert.equal(engage.formatRelativeTime(Date.UTC(2026, 7, 12, 12, 0, 0), now), "Aug 12");
});

test("October 2 through 6 keep their verses and the longer section lengths", function () {
  const feed = JSON.parse(fs.readFileSync(path.join(__dirname, "../app/daily.json"), "utf8"));
  DATES.forEach(function (date) {
    const item = feed.items.find(function (entry) { return entry.date === date; });
    assert.ok(item, date);
    assert.equal(item.verseRef, VERSES[date][0]);
    assert.equal(item.verse, VERSES[date][1]);
    assert.equal(item.body, item.carryBody);
    assert.equal(item.discussionQuestion, QUESTIONS[date]);
    assert.equal(Object.hasOwn(item, "comments"), false);
    const question = item.discussionQuestion;
    assert.equal(/[—–]| - /.test(question), false, date + " question dash");
    assert.equal(/not just/i.test(question), false);
    assert.equal(/\breal man\b/i.test(question), false);
    const silent = words(item.silentBody);
    const challenge = words(item.carryBody);
    const prayer = words(item.prayer);
    assert.ok(silent >= AVG_SILENT * 2 && silent <= AVG_SILENT * 3, date + " silent " + silent);
    assert.ok(challenge >= AVG_CHALLENGE * 2 && challenge <= AVG_CHALLENGE * 3, date + " challenge " + challenge);
    assert.ok(prayer >= AVG_PRAYER * 2 && prayer <= AVG_PRAYER * 3, date + " prayer " + prayer);
    const prose = [item.silentBody, item.carryBody, item.prayer].join("\n");
    assert.equal(/[—–]| - /.test(prose), false, date + " dash");
    assert.equal(/not just/i.test(prose), false);
    assert.equal(/\breal man\b/i.test(prose), false);
  });
});
