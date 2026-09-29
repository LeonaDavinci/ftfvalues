import { FAQ, SITE } from "@/lib/content";

export const dynamic = "force-dynamic";
export const metadata = { title: "FAQ" };

export default function Faq() {
  return (
    <div className="content">
      <h1>Frequently Asked Questions</h1>
      <p className="lead">Common questions about FTF Values and trading</p>

      {FAQ.map((f, i) => (
        <div className="faq-item" key={i}>
          <h3>{f.q}</h3>
          <p>{f.a}</p>
        </div>
      ))}

      <div className="card-block" style={{ textAlign: "center" }}>
        <h2>Still have questions?</h2>
        <p style={{ color: "#a0a0b0", marginBottom: 14 }}>
          Join our Discord communities for help from experienced traders and
          staff members.
        </p>
        <a href={SITE.discord} className="db" style={{ display: "inline-flex" }}>
          💬 AW Apps Discord
        </a>
      </div>
    </div>
  );
}
