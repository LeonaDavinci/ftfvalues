import SmartImage from "./SmartImage";
import { stabilityColor, demandStars } from "@/lib/categories";

function imgPath(item) {
  const p = item.local_image_path || "";
  return "/images/" + p.replace(/ /g, "%20");
}

function valDisplay(item) {
  if (item.value_min && item.value_max) {
    return `${item.value_min}–${item.value_max}`;
  }
  return String(item.value ?? "");
}

export default function MiniCard({ item, slug, color }) {
  const img = imgPath(item);
  const stab = item.stability;
  const sc = stabilityColor(stab);
  const ds = demandStars(item.demand);
  return (
    <a href={`/${slug}#${item.slug || ""}`} className="mc" data-v={item.value}>
      <div className="mi">
        <SmartImage src={img} alt={item.name} />
      </div>
      <div className="mn">{item.name}</div>
      <div className="mv" style={{ color }}>
        &#9889; {valDisplay(item)}
      </div>
      <div className="mt">
        {stab ? (
          <span className="ms" style={{ background: `${sc}33`, color: sc, border: `1px solid ${sc}` }}>
            {stab}
          </span>
        ) : null}
      </div>
      <div className="md">
        <span className="mds" style={{ color: "#f1c40f" }}>
          {ds}
        </span>
      </div>
    </a>
  );
}
