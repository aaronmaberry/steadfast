/* Server session for the paywall. Signed HttpOnly cookie, HMAC SHA-256 with SESSION_SECRET.
   Entitlements come from MEMBER_ACCOUNTS (Vercel env, JSON) at login time. */
const crypto = require("crypto");
const COOKIE = "sm_sess";
const TTL = 7 * 24 * 3600;
const b64u = (buf) => Buffer.from(buf).toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
function sign(payload) {
  const secret = process.env.SESSION_SECRET;
  if (!secret || secret.length < 32) throw new Error("SESSION_SECRET missing");
  const body = b64u(JSON.stringify(payload));
  return body + "." + b64u(crypto.createHmac("sha256", secret).update(body).digest());
}
function accounts() {
  try { return JSON.parse(process.env.MEMBER_ACCOUNTS || "[]"); } catch { return []; }
}
function checkPassword(stored, pass) {
  // stored: scrypt$<salt hex>$<hash hex>
  const [alg, salt, hex] = String(stored || "").split("$");
  if (alg !== "scrypt" || !salt || !hex) return false;
  const want = Buffer.from(hex, "hex");
  const got = crypto.scryptSync(String(pass || ""), Buffer.from(salt, "hex"), want.length);
  return want.length > 0 && crypto.timingSafeEqual(want, got);
}
function cookieHeader(value, maxAge) {
  return COOKIE + "=" + value + "; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=" + maxAge;
}
module.exports = { COOKIE, TTL, sign, accounts, checkPassword, cookieHeader };
