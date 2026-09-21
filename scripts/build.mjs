import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

const root = new URL("..", import.meta.url).pathname;
const lint = spawnSync(process.execPath, [join(root, "scripts/lint.mjs")], { stdio: "inherit" });
if (lint.status !== 0) process.exit(lint.status || 1);

for (const file of ["index.html", "styles.css", "site.js", "vercel.json", "img/logo-lockup.png", "img/mark.png", "img/og-banner.jpg", "img/book-cover.jpg"]) {
  if (!existsSync(join(root, file))) {
    console.error("missing", file);
    process.exit(1);
  }
}

const vercel = JSON.parse(await (await import("node:fs")).promises.readFile(join(root, "vercel.json"), "utf8"));
if (!Array.isArray(vercel.redirects) || !vercel.headers) {
  console.error("vercel.json is not a static site config");
  process.exit(1);
}

console.log("build ok, static site, no bundler");
