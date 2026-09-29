"use client";

import { useMemo, useState } from "react";
import ItemCard from "./ItemCard";
import { stabilityFilters } from "@/lib/categories";

export default function CategoryGrid({ items }) {
  const [stab, setStab] = useState("all");
  const [q, setQ] = useState("");

  const counts = useMemo(() => stabilityFilters(items), [items]);

  const filtered = useMemo(
    () =>
      items.filter((it) => {
        const okS = stab === "all" || (it.stability || "Unknown") === stab;
        const okQ =
          !q || (it.name || "").toLowerCase().includes(q.toLowerCase());
        return okS && okQ;
      }),
    [items, stab, q]
  );

  return (
    <>
      <div className="filters">
        <div className="fg">
          <span className="fl">Stability:</span>
          <button
            className={`fb${stab === "all" ? " active" : ""}`}
            onClick={() => setStab("all")}
          >
            All ({items.length})
          </button>
          {counts.map((c) => (
            <button
              key={c.stability}
              className={`fb${stab === c.stability ? " active" : ""}`}
              onClick={() => setStab(c.stability)}
            >
              <span className="dot" style={{ background: c.color }}></span>
              {c.stability} ({c.count})
            </button>
          ))}
        </div>
        <div className="sb2">
          <input
            type="text"
            placeholder="Search items..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
      </div>

      <section className="section">
        <div className="grid">
          {filtered.map((it) => (
            <ItemCard key={it.id ?? it.slug ?? it.name} item={it} />
          ))}
        </div>
        {filtered.length === 0 && (
          <div id="noResults" style={{ display: "block" }}>
            No items found matching your criteria.
          </div>
        )}
      </section>
    </>
  );
}
