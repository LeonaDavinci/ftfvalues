// Regenerates public/images and data/ftf_values_full_data.json from the
// source repo (the parent folder that holds the scraped data + images).
// Only images referenced by the data file are copied, so orphaned source
// images never leak into the deployment.
// Run with: npm run sync-assets
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, ".."); // ftfvalues-web
const srcRepo = path.resolve(root, ".."); // parent repo root

const dataSrc = path.join(srcRepo, "ftf_values_full_data.json");
if (!fs.existsSync(dataSrc)) {
  console.warn("source data not found at", dataSrc);
  process.exit(1);
}
fs.copyFileSync(dataSrc, path.join(root, "data", "ftf_values_full_data.json"));
console.log("data synced -> data/ftf_values_full_data.json");

const data = JSON.parse(fs.readFileSync(path.join(root, "data", "ftf_values_full_data.json"), "utf8"));
const referenced = new Set();
for (const cat of Object.values(data)) {
  for (const item of cat.items || []) {
    const rel = (item.local_image_path || "").trim().replace(/\\/g, "/");
    if (rel) referenced.add(rel);
  }
}

const imgSrc = path.join(srcRepo, "images");
const imgDest = path.join(root, "public", "images");
if (fs.existsSync(imgSrc)) {
  fs.rmSync(imgDest, { recursive: true, force: true });
  for (const rel of referenced) {
    const s = path.join(imgSrc, rel);
    const d = path.join(imgDest, rel);
    if (fs.existsSync(s)) {
      fs.mkdirSync(path.dirname(d), { recursive: true });
      fs.copyFileSync(s, d);
      const thumb = path.join(imgSrc, "thumb", rel);
      if (fs.existsSync(thumb)) {
        const dt = path.join(imgDest, "thumb", rel);
        fs.mkdirSync(path.dirname(dt), { recursive: true });
        fs.copyFileSync(thumb, dt);
      }
    } else {
      console.warn("referenced image missing:", rel);
    }
  }
  console.log(`images synced -> public/images (${referenced.size} referenced files)`);
} else {
  console.warn("source images not found at", imgSrc);
}
