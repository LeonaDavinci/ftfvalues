"use client";

import { useState } from "react";

const FALLBACK =
  "data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect fill=%22%23222%22 width=%22100%22 height=%22100%22/%3E%3Ctext fill=%22%23888%22 x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22%3EIMG%3C/text%3E%3C/svg%3E";

export default function SmartImage({ src, alt, className }) {
  const [err, setErr] = useState(false);
  return (
    <img
      src={err ? FALLBACK : src}
      alt={alt}
      loading="lazy"
      className={className}
      onError={() => setErr(true)}
    />
  );
}
