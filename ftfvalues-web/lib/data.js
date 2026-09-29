// Server-side data access. Reads the scraped JSON at request time so the
// pages are rendered on the server (SSR) and always reflect the latest data.
import fs from "fs";
import path from "path";

const DATA_PATH = path.join(process.cwd(), "data", "ftf_values_full_data.json");

let _cache = null;

function getRawData() {
  if (!_cache) {
    _cache = JSON.parse(fs.readFileSync(DATA_PATH, "utf-8"));
  }
  return _cache;
}

export function getCategory(key) {
  const d = getRawData();
  const c = d[key] || { items: [], metadata: {} };
  return {
    items: c.items || [],
    meta: c.metadata || {},
    pageName: c.page_name || key,
    pageUrl: c.page_url || "",
  };
}

// Total value + average for a category.
export function getStats(key) {
  const { items } = getCategory(key);
  const total = items.reduce((a, i) => a + (Number(i.value) || 0), 0);
  const avg = items.length ? Math.round(total / items.length) : 0;
  return { count: items.length, total, avg };
}

// Top N items by value, for the home-page preview sections.
export function getTopItems(key, n = 10) {
  const { items } = getCategory(key);
  return [...items]
    .sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
    .slice(0, n);
}

// Image path for an item -> served from /images.
export function imageSrc(item) {
  const p = item.local_image_path || "";
  return "/images/" + p.replace(/ /g, "%20");
}

// Value display string (range when min/max present, else single value).
export function valueDisplay(item) {
  if (item.value_min && item.value_max) {
    return `${item.value_min}–${item.value_max}`;
  }
  return String(item.value ?? "");
}
