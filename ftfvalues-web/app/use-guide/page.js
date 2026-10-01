import { USE_GUIDE } from "@/lib/content";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Use Guide",
  alternates: { canonical: "/use-guide" },
};

export default function UseGuide() {
  const g = USE_GUIDE;
  return (
    <div className="content">
      <h1>Use Guide</h1>
      <p className="lead">Last Updated: January 21st, 2026</p>

      <div className="card-block">
        <h2>{g.changeInValue.title}</h2>
        {g.changeInValue.body.map((b, i) => (
          <p key={i} style={{ color: "#a0a0b0", marginBottom: 6, fontSize: "0.9rem" }}>
            {b}
          </p>
        ))}
      </div>

      <div className="card-block">
        <h2>Stability Tags</h2>
        <div className="tag-row">
          {g.stabilityTags.map((t) => (
            <div className="tag-item" key={t.name}>
              <div className="tn">{t.name}</div>
              <div className="td">{t.desc}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card-block">
        <h2>Status Tags</h2>
        <div className="tag-row">
          {g.statusTags.map((t) => (
            <div className="tag-item" key={t.name}>
              <div className="tn">{t.name}</div>
              <div className="td">{t.desc}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card-block">
        <h2>Demand Tags</h2>
        <ul style={{ listStyle: "none" }}>
          {g.demandTags.map((d, i) => (
            <li
              key={i}
              style={{
                padding: "6px 0",
                borderBottom: "1px solid #23233e",
                color: "#c0c0d0",
                fontSize: "0.9rem",
              }}
            >
              {i + 1}. {d}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
