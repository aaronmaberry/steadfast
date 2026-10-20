const s = require("../lib/session");
module.exports = (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Set-Cookie", s.cookieHeader("", 0));
  res.status(200).json({ ok: true });
};
