import { useMemo, useState } from "react";

const CX = 150, CY = 190, RINGS = 8, SPOKES = 16;

function buildMesh() {
  const pts = [];
  for (let r = 1; r <= RINGS; r++) {
    const k = r / RINGS;
    for (let s = 0; s < SPOKES; s++) {
      const a = (2 * Math.PI * s) / SPOKES;
      pts.push({ r, s, x: CX + 105 * k * Math.cos(a), y: CY + 150 * k * Math.sin(a) });
    }
  }
  const at = (r, s) => pts[(r - 1) * SPOKES + (s % SPOKES)];
  const lines = [];
  for (let r = 1; r <= RINGS; r++) {
    for (let s = 0; s < SPOKES; s++) {
      lines.push([at(r, s), at(r, s + 1)]);
      if (r < RINGS) lines.push([at(r, s), at(r + 1, s)]);
    }
  }
  return { pts, lines };
}

// Drop a portrait at public/hero-face.png to replace the drawn mesh.
export default function HeroArt() {
  const [hasImage, setHasImage] = useState(true);
  const { pts, lines } = useMemo(buildMesh, []);
  return (
    <div className="hero-art" aria-hidden="true">
      <i className="br tl" /><i className="br tr" /><i className="br bl" /><i className="br bb" />
      {hasImage ? (
        <img src="/hero-face.png" alt="" onError={() => setHasImage(false)} />
      ) : (
        <svg viewBox="0 0 300 380">
          {lines.map(([a, b], i) => (
            <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#8b5cf6"
              strokeOpacity={a.x < CX ? 0.55 : 0.14} strokeWidth="0.8" />
          ))}
          {pts.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r={p.x < CX ? 2 : 1.2} fill="#c4b5fd" fillOpacity={p.x < CX ? 0.95 : 0.3} />
          ))}
        </svg>
      )}
    </div>
  );
}
