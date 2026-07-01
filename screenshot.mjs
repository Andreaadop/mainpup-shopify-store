// Usage: node screenshot.mjs <url> [label] [--eval "<js>"]
// Saves to ./temporary screenshots/screenshot-N[-label].png (auto-incremented).
// Optional --eval runs JS in the page before screenshotting (e.g. to set state).
//
// Puppeteer install location: C:/Users/aracy/AppData/Local/Temp/puppeteer-test/
// Chrome cache:               C:/Users/aracy/.cache/puppeteer/
//
// If puppeteer is not yet installed there:
//   cd C:/Users/aracy/AppData/Local/Temp/puppeteer-test
//   npm init -y
//   npm install puppeteer

import { readdir, mkdir } from "node:fs/promises";
import { resolve, join } from "node:path";
import { createRequire } from "node:module";

const PUPPETEER_ROOT = "C:/Users/aracy/AppData/Local/Temp/puppeteer-test";
const SCREENSHOT_DIR = resolve("./temporary screenshots");

const url = process.argv[2];
const args = process.argv.slice(3);
let label;
let evalJs;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--eval") { evalJs = args[i + 1]; i++; }
  else if (!label) { label = args[i]; }
}

if (!url) {
  console.error('Usage: node screenshot.mjs <url> [label] [--eval "<js>"]');
  process.exit(1);
}

const require = createRequire(join(PUPPETEER_ROOT, "package.json"));
let puppeteer;
try {
  puppeteer = require("puppeteer");
} catch (e) {
  console.error(`Could not load puppeteer from ${PUPPETEER_ROOT}.`);
  console.error("Install it with:");
  console.error(`  cd ${PUPPETEER_ROOT} && npm init -y && npm install puppeteer`);
  process.exit(1);
}

await mkdir(SCREENSHOT_DIR, { recursive: true });

const existing = await readdir(SCREENSHOT_DIR);
let maxN = 0;
for (const f of existing) {
  const m = f.match(/^screenshot-(\d+)/);
  if (m) maxN = Math.max(maxN, parseInt(m[1], 10));
}
const n = maxN + 1;
const filename = label ? `screenshot-${n}-${label}.png` : `screenshot-${n}.png`;
const outPath = join(SCREENSHOT_DIR, filename);

const browser = await puppeteer.launch({ headless: "new" });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });
  if (evalJs) {
    await page.evaluate(evalJs);
    await new Promise(r => setTimeout(r, 800)); // let animations settle
  }
  await page.screenshot({ path: outPath, fullPage: true });
  console.log(`Saved: ${outPath}`);
} finally {
  await browser.close();
}
