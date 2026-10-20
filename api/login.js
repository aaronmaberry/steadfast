const s = require("../lib/session");
function readBody(req) {
  if (req.body && typeof req.body === "object") return Promise.resolve(req.body);
  return new Promise((resolve) => {
    let raw = "";
    req.on("data", (c) => { raw += c; if (raw.length > 4096) req.destroy(); });
    req.on("end", () => { try { resolve(JSON.parse(raw || "{}")); } catch { resolve({}); } });
  });
}
module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ ok: false }); return; }
  const body = await readBody(req);
  const email = String(body.email || "").trim().toLowerCase();
  const row = s.accounts().find((a) => String(a.email || "").toLowerCase() === email);
  if (!row || !s.checkPassword(row.hash, body.password)) { res.status(401).json({ ok: false }); return; }
  const ent = Array.isArray(row.ent) ? row.ent.filter((e) => e === "training" || e === "bundle") : [];
  const now = Math.floor(Date.now() / 1000);
  let token;
  try { token = s.sign({ e: email, ent, iat: now, exp: now + s.TTL }); }
  catch { res.status(500).json({ ok: false }); return; }
  res.setHeader("Set-Cookie", s.cookieHeader(token, s.TTL));
  res.status(200).json({ ok: true, email, ent, role: ent.includes("bundle") ? "bundle" : ent.includes("training") ? "member" : "none" });
};
