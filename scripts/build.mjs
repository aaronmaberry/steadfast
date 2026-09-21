import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
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

const vercel = JSON.parse(readFileSync(join(root, "vercel.json"), "utf8"));
if (!Array.isArray(vercel.redirects) || !vercel.headers) {
  console.error("vercel.json is not a static site config");
  process.exit(1);
}
if (vercel.framework !== null || vercel.buildCommand !== "" || vercel.installCommand !== "") {
  console.error("vercel.json must stay a static upload: framework null, empty build and install");
  process.exit(1);
}
if (Object.prototype.hasOwnProperty.call(vercel, "outputDirectory")) {
  console.error("vercel.json must not set outputDirectory");
  process.exit(1);
}

const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
if (pkg.scripts && Object.prototype.hasOwnProperty.call(pkg.scripts, "build")) {
  console.error("package.json must not define a build script");
  process.exit(1);
}
if (!pkg.scripts || pkg.scripts.check !== "node scripts/build.mjs") {
  console.error("package.json check script must run scripts/build.mjs");
  process.exit(1);
}

console.log("check ok, static site, no bundler");
