import SmartImage from "./SmartImage";
import { stabilityColor, statusColor, demandStars } from "@/lib/categories";

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

export default function ItemCard({ item }) {
  const img = imgPath(item);
  const name = item.name || "Unknown";
  const val = valDisplay(item);
  const hint =
    item.value_min && item.value_max ? (
      <div className="vh">
        Range: {item.value_min}–{item.value_max} valuables
      </div>
    ) : null;

  const stab = item.stability;
  const sc = stabilityColor(stab);
  const stabEl = stab ? (
    <span className="b" style={{ background: `${sc}33`, color: sc, border: `1px solid ${sc}` }}>
      {stab}
    </span>
  ) : null;

  const status = item.status;
  const pc = statusColor(status);
  const statusEl = status ? (
    <span className="b" style={{ background: `${pc}33`, color: pc, border: `1px solid ${pc}` }}>
      {status}
    </span>
  ) : null;

  const ds = demandStars(item.demand);

  return (
    <div className="ic" id={item.slug || undefined} data-v={item.value} data-n={name.toLowerCase()}>
      <div className="ii">
        <SmartImage src={img} alt={name} />
      </div>
      <div className="in">
        <h3>{name}</h3>
        <div className="va">
          &#9889; {val} <small>valuables</small>
        </div>
        {hint}
        <div className="tg">
          {stabEl}
          {statusEl}
        </div>
        <div className="dm">
          <span className="dl">Demand:</span>
          <span className="ds">{ds}</span>
        </div>
      </div>
    </div>
  );
}
