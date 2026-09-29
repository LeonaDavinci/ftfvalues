const FOOTER_LINKS = [
  { href: "/", label: "Home" },
  { href: "/use-guide", label: "Use Guide" },
  { href: "/changelog", label: "Changelog" },
  { href: "/faq", label: "FAQ" },
  { href: "/sets", label: "Bundles" },
  { href: "/legendaries", label: "Legendaries" },
  { href: "/epics", label: "Epics" },
  { href: "/rares", label: "Rares" },
  { href: "/commons", label: "Commons" },
];

export default function Footer() {
  return (
    <footer>
      <p>
        &copy; 2026 FTF Values. Unofficial fan-made guide for Flee the
        Facility on Roblox.
      </p>
      <p className="footer-links">
        {FOOTER_LINKS.map((l, i) => (
          <span key={l.href}>
            <a href={l.href}>{l.label}</a>
            {i < FOOTER_LINKS.length - 1 ? " | " : ""}
          </span>
        ))}
      </p>
    </footer>
  );
}
