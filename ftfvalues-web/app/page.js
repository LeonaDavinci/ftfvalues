import MiniCard from "@/components/MiniCard";
import { CATEGORIES, CATEGORY_ORDER } from "@/lib/categories";
import { getCategory, getTopItems } from "@/lib/data";
import { HOME_PREVIEW_ORDER, HOME_FEATURES, COMMUNITY, STAFF, SITE } from "@/lib/content";

export const dynamic = "force-dynamic";

export default function Home() {
  return (
    <>
      <section className="hero">
        <h1>
          <a href="https://www.ftfvalues.app" className="hero-brand-link">
            FTF Values
          </a>
        </h1>
        <p>
          Your trusted source for FTF item values, trading insights, and market
          trends. Make smarter trades with accurate, community-driven value data
          updated daily.
        </p>
        <div className="cb">
          <a href="/legendaries" className="btn bp">
            View Legendary Values
          </a>
          <a href="/sets" className="btn bs">
            Browse Bundles
          </a>
        </div>
      </section>

      <section className="calc-card-wrap">
        <a href="/calculator" className="calc-card">
          <div className="calc-ic" aria-hidden="true">🧮</div>
          <div className="calc-body">
            <h3>FTF Calculator</h3>
            <p>
              Build both sides of a trade and compare totals in fv — know
              instantly if you are winning, losing, or making a fair deal.
            </p>
          </div>
          <span className="calc-go">Open Calculator &rarr;</span>
        </a>
      </section>

      <section className="features">
        {HOME_FEATURES.map((f) => (
          <div className="fc" key={f.title}>
            <h3>{f.title}</h3>
            <p>{f.text}</p>
          </div>
        ))}
      </section>

      {HOME_PREVIEW_ORDER.map((key) => {
        const cfg = CATEGORIES[key];
        const items = getTopItems(key, 12);
        const count = getCategory(key).items.length;
        return (
          <section className="ps" key={key}>
            <div className="psh">
              <h2 style={{ color: cfg.color }}>
                {cfg.emoji} {cfg.name}
              </h2>
              <a
                href={`/${cfg.slug}`}
                className="psl"
                style={{ borderColor: cfg.color, color: cfg.color }}
              >
                View All {count} Items &rarr;
              </a>
            </div>
            <div className="psg">
              {items.map((it) => (
                <MiniCard key={it.id ?? it.slug} item={it} slug={cfg.slug} color={cfg.color} />
              ))}
            </div>
          </section>
        );
      })}

      <section className="community">
        <h2>{COMMUNITY.title}</h2>
        <p>{COMMUNITY.text}</p>
        <a href={SITE.discord} className="db">
          💬 Join Discord
        </a>
      </section>

      <section className="staff">
        <h2>Our Team</h2>
        <div className="sg">
          {STAFF.map((s) => (
            <div className="sc" key={s.name}>
              <div className="av">{s.name.charAt(0).toUpperCase()}</div>
              <h4>{s.name}</h4>
              <div className="ro">{s.role}</div>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
