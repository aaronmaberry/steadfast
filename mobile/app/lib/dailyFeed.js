const feed = require("../../../app/daily.json");

function chicagoDateKey(now) {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Chicago",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(now || new Date());
}

function pickDailyItem(items, key) {
  const list = items || [];
  if (!list.length) return null;
  const day = key || chicagoDateKey();
  const past = list
    .filter(function (item) { return item && item.date && item.date <= day; })
    .sort(function (a, b) { return a.date < b.date ? -1 : 1; });
  return past[past.length - 1] || list[list.length - 1];
}

function paragraphs(text) {
  return String(text || "")
    .split(/\n\n+/)
    .map(function (part) { return part.trim(); })
    .filter(Boolean);
}

function plainVerse(verse) {
  return String(verse || "")
    .replace(/[“”]/g, '"')
    .trim()
    .replace(/^"+|"+$/g, "")
    .split(" — ")[0]
    .replace(/\s*\([^)]*NIV\)\s*$/, "")
    .trim();
}

function readingBlocks(item) {
  if (!item) return ["This day is not in the walk yet."];
  const blocks = [];
  const verse = plainVerse(item.verse);
  if (verse) blocks.push(verse);
  const ref = String(item.verseRef || "").replace(/\s*NIV\s*$/i, "").trim();
  if (ref) blocks.push(ref + " NIV");
  paragraphs(item.silentBody || item.body || "").forEach(function (part) { blocks.push(part); });
  paragraphs(item.carryBody || item.body || "").forEach(function (part) { blocks.push(part); });
  paragraphs(item.reflection || "").forEach(function (part) { blocks.push(part); });
  paragraphs(item.prayer || "").forEach(function (part) { blocks.push(part); });
  return blocks;
}

module.exports = {
  feed: feed,
  chicagoDateKey: chicagoDateKey,
  pickDailyItem: pickDailyItem,
  paragraphs: paragraphs,
  readingBlocks: readingBlocks
};
