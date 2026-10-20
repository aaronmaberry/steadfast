/* Paywall gate. Runs before the CDN on every matched path.
   /private/* is served only to a valid signed session with the right entitlement.
   Old public paths for paid files are closed. */
export const config = {
  matcher: [
    "/private/:path*",
    "/files/lessons/:path*",
    "/files/steadfast-men-ebook.pdf",
    "/files/steadfast-way-workbook.pdf",
    "/walksteadfast/audio/:path*",
    "/training-locked/audio/:path*"
  ]
};

const enc = new TextEncoder();
function b64uToBytes(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
async function readSession(request) {
  const secret = process.env.SESSION_SECRET;
  if (!secret || secret.length < 32) return null;
  const raw = (request.headers.get("cookie") || "").split(/;\s*/).find((c) => c.startsWith("sm_sess="));
  if (!raw) return null;
  const [body, sig] = raw.slice(8).split(".");
  if (!body || !sig) return null;
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
  let ok = false;
  try { ok = await crypto.subtle.verify("HMAC", key, b64uToBytes(sig), enc.encode(body)); } catch { return null; }
  if (!ok) return null;
  let p;
  try { p = JSON.parse(new TextDecoder().decode(b64uToBytes(body))); } catch { return null; }
  if (!p || typeof p.exp !== "number" || p.exp < Date.now() / 1000) return null;
  return p;
}
const deny = (status) => new Response(status === 401 ? "Sign in required." : "Not available.", {
  status, headers: { "Cache-Control": "no-store", "Content-Type": "text/plain; charset=utf-8" }
});

export default async function middleware(request) {
  const path = new URL(request.url).pathname;
  if (!path.startsWith("/private/")) return deny(404);
  const sess = await readSession(request);
  if (!sess) return deny(401);
  const ent = Array.isArray(sess.ent) ? sess.ent : [];
  const need = path === "/private/steadfast-men-ebook.pdf" ? ["bundle"] : ["training", "bundle"];
  if (!need.some((e) => ent.includes(e))) return deny(403);
  // entitled: fall through to the static file (CDN serves Range / 206)
}
