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

test("local like and private note stay on the device store, per date", async function () {
  const storage = engage.memoryStorage();
  const adapter = engage.createStorageAdapter(storage);
  engage.setAdapter(adapter);
  assert.equal(await engage.getLike("2026-10-02"), false);
  assert.equal(await engage.setLike("2026-10-02", true), true);
  assert.equal(await engage.setLike("2026-10-03", false), false);
  assert.equal(await engage.getLike("2026-10-02"), true);
  assert.equal(await engage.getLike("2026-10-03"), false);
  assert.equal(await engage.setNote("2026-10-02", "Kept this on my phone."), "Kept this on my phone.");
  assert.equal(await engage.getNote("2026-10-02"), "Kept this on my phone.");
  assert.equal(await engage.getNote("2026-10-03"), "");
  assert.equal(await engage.setNote("2026-10-02", ""), "");
  assert.equal(await engage.getNote("2026-10-02"), "");
  const rawLikes = JSON.parse(storage.getItem("steadfast.daily.likes"));
  assert.equal(rawLikes["2026-10-02"], true);
  assert.equal(Object.hasOwn(rawLikes, "2026-10-03"), false);
  engage.setAdapter(null);
});

test("October 2 through 6 keep their verses and the longer section lengths", function () {
  const feed = JSON.parse(fs.readFileSync(path.join(__dirname, "../app/daily.json"), "utf8"));
  DATES.forEach(function (date) {
    const item = feed.items.find(function (entry) { return entry.date === date; });
    assert.ok(item, date);
    assert.equal(item.verseRef, VERSES[date][0]);
    assert.equal(item.verse, VERSES[date][1]);
    assert.equal(item.body, item.carryBody);
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
