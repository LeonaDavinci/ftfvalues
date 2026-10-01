"use client";

import { useMemo, useRef, useState } from "react";

const fmt = (n) => (Number(n) || 0).toLocaleString("en-US");
const imgSrc = (p) => "/images/" + String(p || "").replace(/ /g, "%20");

function SlotImage({ src, alt }) {
  const [err, setErr] = useState(false);
  if (err) return <div className="slot-ph">?</div>;
  return <img src={src} alt={alt} loading="lazy" onError={() => setErr(true)} />;
}

export default function Calculator({ items, lastUpdated }) {
  const [your, setYour] = useState([]); // [{ slug, qty }]
  const [their, setTheir] = useState([]);
  const [side, setSide] = useState("your"); // where the next picked item goes
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const searchRef = useRef(null);

  const bySlug = useMemo(() => {
    const m = {};
    for (const it of items) m[it.slug] = it;
    return m;
  }, [items]);

  const results = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return [];
    return items.filter((i) => i.name.toLowerCase().includes(s)).slice(0, 30);
  }, [q, items]);

  const total = (list) =>
    list.reduce((a, e) => a + (bySlug[e.slug]?.value || 0) * e.qty, 0);
  const yourTotal = total(your);
  const theirTotal = total(their);

  const addItem = (item) => {
    const setter = side === "your" ? setYour : setTheir;
    setter((prev) => {
      const ex = prev.find((e) => e.slug === item.slug);
      if (ex)
        return prev.map((e) => (e.slug === item.slug ? { ...e, qty: e.qty + 1 } : e));
      return [...prev, { slug: item.slug, qty: 1 }];
    });
    setQ("");
    setOpen(false);
    searchRef.current?.focus();
  };

  const changeQty = (which, slug, d) => {
    const setter = which === "your" ? setYour : setTheir;
    setter((prev) =>
      prev
        .map((e) => (e.slug === slug ? { ...e, qty: e.qty + d } : e))
        .filter((e) => e.qty > 0)
    );
  };

  const removeItem = (which, slug) => {
    const setter = which === "your" ? setYour : setTheir;
    setter((prev) => prev.filter((e) => e.slug !== slug));
  };

  const reset = () => {
    setYour([]);
    setTheir([]);
  };

  // Verdict: their > your (beyond tolerance) means you WIN; the reverse LOSE.
  const diff = theirTotal - yourTotal;
  const tol = Math.max(50, 0.05 * Math.max(yourTotal, theirTotal));
  let verdict = null;
  if (your.length > 0 && their.length > 0) {
    if (Math.abs(diff) <= tol) verdict = "FAIR";
    else verdict = diff > 0 ? "WIN" : "LOSE";
  }

  // Render the trade as a shareable PNG via canvas (all images are same-origin).
  const saveImage = async () => {
    const loadImg = (src) =>
      new Promise((res) => {
        const im = new Image();
        im.onload = () => res(im);
        im.onerror = () => res(null);
        im.src = src;
      });

    const W = 900;
    const rowH = 52;
    const maxRows = 7;
    const rows = Math.min(maxRows, Math.max(your.length, their.length, 1));
    const H = 400 + rows * rowH + 40;
    const cv = document.createElement("canvas");
    cv.width = W;
    cv.height = H;
    const ctx = cv.getContext("2d");

    ctx.fillStyle = "#0f0f1a";
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#13132a";
    ctx.fillRect(30, 30, W - 60, H - 60);

    ctx.textAlign = "center";
    ctx.fillStyle = "#e94560";
    ctx.font = "bold 32px 'Segoe UI', sans-serif";
    ctx.fillText("FTF Values — Trade Calculator", W / 2, 85);
    ctx.fillStyle = "#808090";
    ctx.font = "15px 'Segoe UI', sans-serif";
    ctx.fillText(
      new Date().toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }),
      W / 2,
      112
    );

    const drawSide = async (list, x0, title) => {
      ctx.textAlign = "center";
      ctx.fillStyle = "#f0f0f0";
      ctx.font = "bold 22px 'Segoe UI', sans-serif";
      ctx.fillText(title, x0 + 190, 165);
      ctx.fillStyle = "#e94560";
      ctx.font = "bold 26px 'Segoe UI', sans-serif";
      ctx.fillText(fmt(total(list)) + " fv", x0 + 190, 196);
      const shown = list.slice(0, maxRows);
      let y = 230;
      for (const e of shown) {
        const it = bySlug[e.slug];
        if (!it) continue;
        const im = await loadImg(imgSrc(it.local_image_path));
        ctx.fillStyle = "#1a1a2e";
        ctx.fillRect(x0 + 40, y, 44, 44);
        if (im) ctx.drawImage(im, x0 + 40, y, 44, 44);
        ctx.textAlign = "left";
        ctx.fillStyle = "#e0e0e0";
        ctx.font = "16px 'Segoe UI', sans-serif";
        ctx.fillText(it.name + (e.qty > 1 ? " ×" + e.qty : ""), x0 + 96, y + 28);
        ctx.textAlign = "right";
        ctx.fillStyle = "#a0a0b0";
        ctx.font = "15px 'Segoe UI', sans-serif";
        ctx.fillText(fmt((it.value || 0) * e.qty) + " fv", x0 + 340, y + 28);
        y += rowH;
      }
      if (list.length > maxRows) {
        ctx.textAlign = "left";
        ctx.fillStyle = "#808090";
        ctx.font = "14px 'Segoe UI', sans-serif";
        ctx.fillText("+" + (list.length - maxRows) + " more…", x0 + 96, y + 10);
      }
      ctx.textAlign = "center";
    };

    await drawSide(your, 50, "Your Offer");
    await drawSide(their, W - 430, "Their Offer");

    ctx.strokeStyle = "#2a2a4e";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(W / 2, 150);
    ctx.lineTo(W / 2, 230 + rows * rowH);
    ctx.stroke();

    if (verdict) {
      const col =
        verdict === "WIN" ? "#2ecc71" : verdict === "LOSE" ? "#e74c3c" : "#f1c40f";
      ctx.fillStyle = col;
      ctx.font = "bold 44px 'Segoe UI', sans-serif";
      ctx.fillText(fmt(Math.abs(diff)), W / 2, 260);
      ctx.font = "bold 20px 'Segoe UI', sans-serif";
      ctx.fillText("FV " + verdict, W / 2, 292);
    } else {
      ctx.fillStyle = "#808090";
      ctx.font = "18px 'Segoe UI', sans-serif";
      ctx.fillText("Add items to both sides", W / 2, 260);
    }

    ctx.fillStyle = "#606070";
    ctx.font = "14px 'Segoe UI', sans-serif";
    ctx.fillText("www.ftfvalues.app", W / 2, H - 50);

    cv.toBlob((blob) => {
      if (!blob) return;
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "ftf-trade-calculator.png";
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 5000);
    }, "image/png");
  };

  const renderSide = (which, list, title) => {
    const slotCount = Math.max(9, Math.ceil((list.length + 1) / 3) * 3);
    const slots = [];
    for (let i = 0; i < slotCount; i++) {
      const entry = list[i];
      if (entry) {
        const it = bySlug[entry.slug];
        slots.push(
          <div className="slot filled" key={entry.slug}>
            <button
              className="slot-rm"
              onClick={() => removeItem(which, entry.slug)}
              aria-label={"Remove " + it.name}
            >
              ×
            </button>
            <SlotImage src={imgSrc(it.local_image_path)} alt={it.name} />
            <div className="qty">
              <button onClick={() => changeQty(which, entry.slug, -1)} aria-label="Decrease">
                −
              </button>
              <span>{entry.qty}</span>
              <button onClick={() => changeQty(which, entry.slug, +1)} aria-label="Increase">
                +
              </button>
            </div>
          </div>
        );
      } else {
        slots.push(
          <button
            key={"empty-" + i}
            className={"slot empty" + (side === which ? " target" : "")}
            onClick={() => {
              setSide(which);
              searchRef.current?.focus();
            }}
            aria-label={"Add item to " + title}
          >
            +
          </button>
        );
      }
    }
    return (
      <div className={"calc-side" + (which === "their" ? " their-side" : "")}>
        <h3>{title}</h3>
        <div className="slots">{slots}</div>
      </div>
    );
  };

  return (
    <div className="calc-wrap">
      <div className="calc-panel">
        <div className="calc-top">
          <div className="ctotal">
            {fmt(yourTotal)} <small>fv</small>
          </div>
          <div className="clegend">
            <span className="lw">Win</span>
            <span className="lf">Fair</span>
            <span className="ll">Lose</span>
          </div>
          <div className="ctotal right">
            {fmt(theirTotal)} <small>fv</small>
          </div>
        </div>

        <div className="calc-add">
          <div className="side-pick">
            <button className={side === "your" ? "on" : ""} onClick={() => setSide("your")}>
              Your Offer
            </button>
            <button className={side === "their" ? "on" : ""} onClick={() => setSide("their")}>
              Their Offer
            </button>
          </div>
          <div className="srch">
            <input
              ref={searchRef}
              value={q}
              placeholder="Search items to add…"
              aria-label="Search items"
              onChange={(e) => {
                setQ(e.target.value);
                setOpen(true);
              }}
              onFocus={() => setOpen(true)}
              onBlur={() => setTimeout(() => setOpen(false), 150)}
            />
            {open && q.trim() && (
              <div className="sr-drop">
                {results.length === 0 && (
                  <div className="sr-none">No items match &ldquo;{q}&rdquo;</div>
                )}
                {results.map((it) => (
                  <button className="sr-item" key={it.slug} onClick={() => addItem(it)}>
                    <SlotImage src={imgSrc(it.local_image_path)} alt={it.name} />
                    <span className="sr-name">{it.name}</span>
                    <span className="sr-val">{fmt(it.value)} fv</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="calc-grid3">
          {renderSide("your", your, "Your Offer")}
          <div className="calc-mid">
            {verdict ? (
              <>
                <div className={"vnum " + verdict.toLowerCase()}>{fmt(Math.abs(diff))}</div>
                <div className={"vlab " + verdict.toLowerCase()}>FV {verdict}</div>
              </>
            ) : (
              <div className="vnum idle">—</div>
            )}
            <button className="cbtn" onClick={reset}>
              Reset
            </button>
            <button className="cbtn" onClick={saveImage}>
              Save Image
            </button>
          </div>
          {renderSide("their", their, "Their Offer")}
        </div>

        <div className="calc-note">
          <span>Last updated: {lastUpdated || "—"}</span>
          <span className="cn2">Values in fv (valuables)</span>
        </div>
      </div>
    </div>
  );
}
