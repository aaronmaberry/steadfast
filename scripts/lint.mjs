import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const root = new URL("..", import.meta.url).pathname;
const fail = [];

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === "node_modules" || name === ".git") continue;
    const path = join(dir, name);
    const st = statSync(path);
    if (st.isDirectory()) walk(path, out);
    else out.push(path);
  }
  return out;
}

const files = walk(root).filter((p) => /\.(html|js|css|json|xml|txt|md)$/.test(p));
const banned = ["\u2014", "\u2013", "\u201c", "\u201d", "\u2018", "\u2019"];

for (const path of files) {
  const text = readFileSync(path, "utf8");
  const rel = path.slice(root.length);
  for (const ch of banned) {
    if (text.includes(ch)) fail.push(rel + " contains a banned dash or curly quote");
  }
  if (/steadfastmen\.com/i.test(text)) fail.push(rel + " names steadfastmen.com");
  if (/SteadfastTable26|WalkThePath26/.test(text)) fail.push(rel + " ships a password");
  if (/4242 4242 4242 4242/.test(text)) fail.push(rel + " publishes a test card");
  if (/placeholder review/i.test(text)) fail.push(rel + " ships a fake review");
  if (rel.endsWith(".html") && /type="file"/.test(text)) fail.push(rel + " ships a file upload");
  if (rel.endsWith(".html") && /buy\.stripe\.com|donate\.stripe\.com/.test(text)) {
    fail.push(rel + " links a Stripe checkout from a public page");
  }
}

const css = readFileSync(join(root, "styles.css"), "utf8");
for (const token of ["#0B1F38", "#E3C572", "#E6DDCC", "Playfair Display", "Libre Franklin", "EB Garamond"]) {
  if (!css.includes(token)) fail.push("styles.css missing " + token);
}
if (/Geist/.test(css)) fail.push("styles.css still names Geist");

const index = readFileSync(join(root, "index.html"), "utf8");
const links = JSON.parse(readFileSync(join(root, "app/links.json"), "utf8"));
if (links.hub !== "https://walksteadfast.com") fail.push("links.json hub drifted");
const expectedSocials = [
  "https://youtube.com/@steadfastwalk",
  "https://instagram.com/steadfastwalk",
  "https://x.com/steadfastwalk",
  "https://facebook.com/steadfastwalk",
  "https://tiktok.com/@steadfastwalk"
];
const gotSocials = (links.socials || []).map((s) => s.href);
if (gotSocials.join("|") !== expectedSocials.join("|")) fail.push("links.json socials drifted");
for (const url of expectedSocials) {
  if (!index.includes(url)) fail.push("index.html missing " + url);
}
for (const url of ["img/logo-lockup.png", "img/mark.png", "https://www.walksteadfast.com/img/og-banner.jpg"]) {
  if (!index.includes(url)) fail.push("index.html missing " + url);
}
if (!index.includes("data-social-dock")) fail.push("index.html social dock is not bound to links.json");
const htmlFiles = files.filter((p) => p.endsWith(".html")).map((p) => readFileSync(p, "utf8")).join("\n");
if (/linkedin\.com|reddit\.com/i.test(htmlFiles + JSON.stringify(links))) fail.push("parked profile linked");
for (const [key, href] of Object.entries(links.ctas || {})) {
  const path = new URL(href).pathname.replace(/\/$/, "") || "/";
  if (!href.startsWith("https://walksteadfast.com")) fail.push("cta " + key + " is not on the hub");
  if (path === "/") continue;
  const file = join(root, path.slice(1) + ".html");
  if (!existsSync(file)) fail.push("cta " + key + " has no page " + path);
}

const checkout = readFileSync(join(root, "checkout.js"), "utf8");
if (!/armed:\s*false/.test(checkout)) fail.push("checkout.js is armed");
if (/buy\.stripe\.com\/(?!test_)/.test(checkout) || /donate\.stripe\.com\/(?!test_)/.test(checkout)) {
  fail.push("checkout.js has a live Stripe URL");
}

if (fail.length) {
  console.error(fail.join("\n"));
  process.exit(1);
}
console.log("lint ok", files.length, "files");
