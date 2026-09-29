import CategoryGrid from "./CategoryGrid";
import { CATEGORIES } from "@/lib/categories";
import { getCategory, getStats } from "@/lib/data";

export default function CategoryView({ categoryKey }) {
  const cfg = CATEGORIES[categoryKey];
  const { items, meta } = getCategory(categoryKey);
  const { count, avg } = getStats(categoryKey);
  const updated = meta.last_updated || "Unknown";

  return (
    <div
      style={{
        "--accent": cfg.color,
        "--cat-gradient": cfg.gradient,
      }}
    >
      <section className="cat-hero">
        <h1>
          {cfg.emoji} {cfg.name}
        </h1>
        <p>{cfg.desc}</p>
        <div className="sb">
          <div className="st">
            <div className="stv">{count}</div>
            <div className="stl">Total Items</div>
          </div>
          <div className="st">
            <div className="stv">{avg}</div>
            <div className="stl">Avg Value</div>
          </div>
          <div className="st">
            <div className="stv" style={{ fontSize: "1.1rem" }}>
              {updated}
            </div>
            <div className="stl">Last Updated</div>
          </div>
        </div>
      </section>

      <CategoryGrid items={items} />
    </div>
  );
}
