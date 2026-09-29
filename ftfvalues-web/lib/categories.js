// Category configuration + shared display helpers for FTF Values.
// Mirrors the design tokens from the original static site so the rebuilt
// Next.js version keeps the same look & feel.

export const CATEGORIES = {
  Sets: {
    key: "Sets",
    slug: "sets",
    name: "Bundles & Sets",
    emoji: "🎁",
    color: "#e94560",
    gradient: "linear-gradient(135deg,#1a1a2e 0%,#2d1a2e 100%)",
    desc: "Exclusive item bundles and themed collections with unique trading value.",
  },
  Legendaries: {
    key: "Legendaries",
    slug: "legendaries",
    name: "Legendaries",
    emoji: "👑",
    color: "#f1c40f",
    gradient: "linear-gradient(135deg,#1a1a2e 0%,#2e2a1a 100%)",
    desc: "Highest-tier items with the most valuable trading worth in Flee the Facility.",
  },
  Epics: {
    key: "Epics",
    slug: "epics",
    name: "Epics",
    emoji: "💎",
    color: "#9b59b6",
    gradient: "linear-gradient(135deg,#1a1a2e 0%,#1a1a2e 100%)",
    desc: "Mid-to-high tier items highly sought after by experienced traders.",
  },
  Rares: {
    key: "Rares",
    slug: "rares",
    name: "Rares",
    emoji: "🔥",
    color: "#e74c3c",
    gradient: "linear-gradient(135deg,#1a1a2e 0%,#2e1a1a 100%)",
    desc: "Moderately valued items with steady trading activity in the community.",
  },
  Commons: {
    key: "Commons",
    slug: "commons",
    name: "Commons",
    emoji: "✨",
    color: "#3498db",
    gradient: "linear-gradient(135deg,#1a1a2e 0%,#1a2a2e 100%)",
    desc: "Entry-level items perfect for new traders and fair starter trades.",
  },
};

export const CATEGORY_ORDER = ["Sets", "Legendaries", "Epics", "Rares", "Commons"];

// Stability tag -> color (kept from the original site).
export const STABILITY_COLORS = {
  Rising: "#2ecc71",
  Stable: "#3498db",
  Fluctuating: "#f39c12",
  Dropping: "#e74c3c",
  Volatile: "#9b59b6",
  Unstable: "#e67e22",
  "Stable-Ish": "#1abc9c",
  Undetermined: "#95a5a6",
  "Doing Well": "#27ae60",
  Improving: "#16a085",
  Struggling: "#e67e22",
  Receding: "#d35400",
};

export function stabilityColor(s) {
  return STABILITY_COLORS[s] || "#95a5a6";
}

// Status tag -> color.
export const STATUS_COLORS = {
  "Overpaid For": "#2ecc71",
  "Underpaid For": "#e74c3c",
  Niche: "#9b59b6",
  Bio: "#2ecc71",
  Fake: "#e74c3c",
  Perm: "#3498db",
};

export function statusColor(s) {
  return STATUS_COLORS[s] || "#95a5a6";
}

// Render demand as a 0-5 star string (ported from original generator).
export function demandStars(n) {
  if (n === null || n === undefined || n === "") return "☆☆☆☆☆";
  const v = Math.trunc(Number(n));
  if (isNaN(v)) return "☆☆☆☆☆";
  const full = Math.min(5, Math.floor(v / 2) + (v % 2 ? 1 : 0));
  return "★".repeat(full) + "☆".repeat(5 - full);
}

// Build the "All (N)" + per-stability filter buttons with counts.
export function stabilityFilters(items) {
  const sc = {};
  for (const i of items) {
    const s = i.stability || "Unknown";
    sc[s] = (sc[s] || 0) + 1;
  }
  return Object.entries(sc)
    .sort((a, b) => b[1] - a[1])
    .map(([s, c]) => ({ stability: s, count: c, color: stabilityColor(s) }));
}
