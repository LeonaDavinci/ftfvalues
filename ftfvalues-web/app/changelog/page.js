import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";
export const metadata = { title: "Changelog" };

export default function Changelog() {
  const data = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), "data", "changelog.json"), "utf-8")
  );

  return (
    <div className="content">
      <h1>Changelog</h1>
      <p className="lead">
        Track all updates, changes, and improvements to FTF item values
      </p>

      {data.map((v) => (
        <div className="changelog-version" key={v.version}>
          <div className="vh">
            <h2>Version {v.version}</h2>
            <span className="vd">{v.date}</span>
          </div>
          <ul className="change-list">
            {v.changes.map((c, i) => (
              <li key={i}>
                <span className={`change-type ct-${c.type.replace(/\s/g, "")}`}>
                  {c.type}
                </span>
                <span>{c.text}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
