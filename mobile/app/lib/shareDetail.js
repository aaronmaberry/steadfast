"use strict";

function buildSharePayload(title, url) {
  const name = String(title || "Steadfast").trim() || "Steadfast";
  const link = typeof url === "string" ? url.trim() : "";
  const payload = {
    title: name,
    message: link ? name + "\n" + link : name
  };
  if (link) payload.url = link;
  return payload;
}

function canceled(err) {
  if (!err) return false;
  if (err.name === "AbortError") return true;
  return /cancel|dismiss/i.test(String(err.message || ""));
}

async function copyText(text) {
  if (!text) return false;
  if (typeof navigator === "undefined" || !navigator.clipboard || !navigator.clipboard.writeText) {
    return false;
  }
  await navigator.clipboard.writeText(text);
  return true;
}

async function shareDetail(title, url, shareFn) {
  const payload = buildSharePayload(title, url);
  try {
    if (typeof shareFn === "function") {
      const result = await shareFn(payload);
      if (result && result.action && /dismiss/i.test(String(result.action))) return "dismissed";
      return "shared";
    }
  } catch (err) {
    if (canceled(err)) return "dismissed";
  }
  try {
    const copied = await copyText(payload.url || payload.message);
    if (copied) return "copied";
  } catch (copyErr) {}
  return "failed";
}

module.exports = {
  buildSharePayload: buildSharePayload,
  shareDetail: shareDetail
};
