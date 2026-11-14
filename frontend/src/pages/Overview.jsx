import { Play, ArrowRight, Info, ScanFace, Activity, ShieldCheck, Layers, Waves, Timer } from "lucide-react";
import HeroArt from "../components/HeroArt";

const CARDS = [
  { icon: ScanFace, title: "Facial Mapping", text: "Finds the face and picks the forehead and cheek regions." },
  { icon: Activity, title: "rPPG Analysis", text: "Reads tiny colour changes in the skin that follow the heartbeat." },
  { icon: ShieldCheck, title: "Deepfake Screening", text: "Compares pulse consistency across regions as one screening signal." },
];
const STATS = [
  { icon: Layers, value: "3", label: "Face regions compared" },
  { icon: Waves, value: "0.7 to 4 Hz", label: "Pulse band analysed" },
  { icon: Timer, value: "15 s+", label: "Minimum clip length" },
];

export default function Overview({ go }) {
  return (
    <div className="overview">
      <section className="hero">
        <div className="hero-copy">
          <h1>See beyond<br />what looks <span>real.</span></h1>
          <p>An experimental deepfake screening system exploring hidden physiological signals within facial videos.</p>
          <div className="cta">
            <button className="btn primary" onClick={() => go("analyze")}><Play size={18} /> Start Analysis <ArrowRight size={18} /></button>
            <button className="btn ghost" onClick={() => go("methodology")}>Explore Technology <Info size={18} /></button>
          </div>
        </div>
        <HeroArt />
        <aside className="ppg-card">
          <h4>rPPG <em>Analysis</em></h4>
          <svg viewBox="0 0 180 60" className="ecg">
            <path d="M0 32 L22 32 L30 32 L36 10 L44 54 L50 32 L72 32 L80 32 L86 12 L94 52 L100 32 L122 32 L130 32 L136 10 L144 54 L150 32 L180 32" />
          </svg>
          <ul>
            <li><i style={{ background: "#22d3ee" }} />Forehead</li>
            <li><i style={{ background: "#a78bfa" }} />Left Cheek</li>
            <li><i style={{ background: "#f472b6" }} />Right Cheek</li>
          </ul>
        </aside>
      </section>

      <section className="cards">
        {CARDS.map(({ icon: Icon, title, text }) => (
          <button key={title} className="card" onClick={() => go("methodology")}>
            <span className="icon"><Icon size={30} /></span>
            <span><strong>{title}</strong><small>{text}</small></span>
            <ArrowRight size={18} />
          </button>
        ))}
      </section>

      <section className="stats">
        {STATS.map(({ icon: Icon, value, label }) => (
          <div key={label}><Icon size={26} /><span><strong>{value}</strong><small>{label}</small></span></div>
        ))}
        <p className="tag"><b>PulseGuard</b><small>Prototype. Not a validated detector.</small></p>
      </section>
    </div>
  );
}
