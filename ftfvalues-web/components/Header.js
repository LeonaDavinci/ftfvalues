"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";

const MAIN_NAV = [
  { href: "/sets", label: "Bundles" },
  { href: "/legendaries", label: "Legendaries" },
  { href: "/epics", label: "Epics" },
  { href: "/rares", label: "Rares" },
  { href: "/commons", label: "Commons" },
];

const MORE_NAV = [
  { href: "/", label: "🏠 Home" },
  { href: "/use-guide", label: "📕 Use Guide" },
  { href: "/changelog", label: "🗝️ Changelog" },
  { href: "/faq", label: "❓ FAQ" },
];

export default function Header() {
  const pathname = usePathname();
  const [moreOpen, setMoreOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const isActive = (href) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header className="header">
      <a href="https://www.ftfvalues.app" className="logo">
        FTF Values
      </a>

      <nav className={`main-nav${mobileOpen ? " show" : ""}`} id="mainNav">
        {MAIN_NAV.map((n) => (
          <a
            key={n.href}
            href={n.href}
            className={isActive(n.href) ? "active" : ""}
          >
            {n.label}
          </a>
        ))}
      </nav>

      <div className="nav-more">
        <button
          className="nav-more-btn"
          aria-label="More pages"
          onClick={() => setMoreOpen((v) => !v)}
        >
          ⚙ More
        </button>
        <div className={`nav-more-menu${moreOpen ? " show" : ""}`}>
          {MORE_NAV.map((n) => (
            <a
              key={n.href}
              href={n.href}
              className={isActive(n.href) ? "active" : ""}
            >
              {n.label}
            </a>
          ))}
        </div>
      </div>

      <button
        className="mobile-menu-btn"
        aria-label="Toggle menu"
        onClick={() => setMobileOpen((v) => !v)}
      >
        ☰
      </button>
    </header>
  );
}
