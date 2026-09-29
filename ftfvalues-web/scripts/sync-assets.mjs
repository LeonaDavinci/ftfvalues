// Regenerates public/images and data/ftf_values_full_data.json from the
// source repo (the parent folder that holds the scraped data + images).
// Run with: npm run sync-assets
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, ".."); // ftfvalues-web
const srcRepo = path.resolve(root, ".."); // parent repo root

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const e of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, e.name);
    const d = path.join(dest, e.name);
    if (e.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

const imgSrc = path.join(srcRepo, "images");
if (fs.existsSync(imgSrc)) {
  copyDir(imgSrc, path.join(root, "public", "images"));
  console.log("images synced -> public/images");
} else {
  console.warn("source images not found at", imgSrc);
}

const dataSrc = path.join(srcRepo, "ftf_values_full_data.json");
if (fs.existsSync(dataSrc)) {
  fs.copyFileSync(dataSrc, path.join(root, "data", "ftf_values_full_data.json"));
  console.log("data synced -> data/ftf_values_full_data.json");
} else {
  console.warn("source data not found at", dataSrc);
}
