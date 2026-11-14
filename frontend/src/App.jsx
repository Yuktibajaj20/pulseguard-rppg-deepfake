import { useEffect, useState } from "react";

const API = (import.meta.env.VITE_API_URL || "https://pulseguard-api-xcbk.onrender.com").replace(/\/$/, "");
const STEPS = [
  "Uploading video",
  "Detecting face and landmarks",
  "Extracting RGB signals from skin regions",
  "Filtering noise and estimating heart rate",
  "Comparing facial regions",
];
 
const pretty = (k) => String(k).toLowerCase().replace(/_/g, " ").replace(/^\w|\s\w/g, (c) => c.toUpperCase());
const fmt = (n, d = 1) => (typeof n === "number" && isFinite(n) ? n.toFixed(d) : "—");

const Ic = ({ children }) => <svg viewBox="0 0 24 24">{children}</svg>;
const Arrow = () => <Ic><path d="M5 12h14M13 6l6 6-6 6" /></Ic>;

const NAV = [
  ["overview", "Overview", <><path d="M3 11l9-8 9 8v10H3z" /><path d="M9 21v-6h6v6" /></>],
  ["analysis", "New Analysis", <><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M10 8l6 4-6 4z" /></>],
  ["results", "Results", <path d="M4 20V10M10 20V4M16 20v-8M21 20H3" />],
  ["method", "Methodology", <><path d="M2 5c3-1 7-1 10 1 3-2 7-2 10-1v14c-3-1-7-1-10 1-3-2-7-2-10-1z" /><path d="M12 6v14" /></>],
  ["about", "About", <><circle cx="12" cy="12" r="9" /><path d="M12 11v5M12 8h.01" /></>],
];

const IDEA = [
  ["01 · SIGNAL", "A pulse in the pixels", "Each heartbeat shifts blood through facial skin, causing tiny changes in reflected light that an ordinary camera can capture."],
  ["02 · CHECK", "Consistency over time", "We compare signals across the forehead and cheeks to see whether they agree, as they should in a real face."],
  ["03 · HONESTY", "Uncertainty, shown", "Results are a screening aid, not a verdict. The dashboard communicates uncertainty instead of guaranteeing a conclusion."],
];

const TILES = [
  ["Facial regions", "Forehead and cheek skin regions detected with landmarks.", <><rect x="30" y="4" width="40" height="48" rx="20" /><path d="M38 18h24M36 34h8M56 34h8" /></>],
  ["Heart rate", "A separate beats-per-minute estimate for every region.", <path d="M0 30h20l5-20 8 40 7-30 6 10h54" />],
  ["Signal quality", "How trustworthy the extracted signals are.", <path d="M10 48V30M30 48V18M50 48V8M70 48V24M90 48V14" />],
  ["Cross-region match", "Do different facial regions tell the same story?", <path d="M0 20c15-14 25 14 40 0s25 14 40 0M0 40c15-14 25 14 40 0s25 14 40 0" />],
];

export default function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [step, setStep] = useState(0);
  const [slow, setSlow] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [over, setOver] = useState(false);
  const [active, setActive] = useState("overview");

  useEffect(() => {
    if (status !== "running") return;
    setStep(0);
    setSlow(false);
    const a = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 3000);
    const b = setTimeout(() => setSlow(true), 8000);
    return () => { clearInterval(a); clearTimeout(b); };
  }, [status]);

  function pick(f) {
    if (!f) return;
    setFile(f);
    setError("");
  }

  async function run() {
    if (!file) { setError("Choose a video first (.mp4, .mov or .avi, up to 100 MB)."); return; }
    setError("");
    setResult(null);
    setStatus("running");
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 300000);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const r = await fetch(`${API}/analyze`, { method: "POST", body: fd, signal: ctrl.signal });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(typeof j.detail === "string" ? j.detail : `Server error (${r.status})`);
      setResult(j);
      setStatus("done");
      setTimeout(() => document.getElementById("results")?.scrollIntoView({ behavior: "smooth" }), 150);
    } catch (e) {
      setError(
        e.name === "AbortError" ? "The analysis took too long. Try a shorter clip."
        : e.message === "Failed to fetch" ? "Could not reach the server. It may be waking up, so try again in a minute."
        : e.message
      );
      setStatus("error");
    } finally {
      clearTimeout(t);
    }
  }

  const rf = result?.regional_features || {};
  const q = result?.signal_quality || {};
  const vd = result?.video || {};
  const inconclusive = result?.assessment === "INCONCLUSIVE";
  const corr = typeof rf.mean_correlation === "number" ? rf.mean_correlation : null;

  return (
    <div className="shell">
      <header className="top">
        <span className="tag">Beyond the Face. Beneath the Pixels.</span>
        <div>
          <a href="#method">Research</a><a href="#about">About</a>
          <a className="btn" href="#analysis">Start Analysis <Arrow /></a>
        </div>
      </header>

      <aside>
        <div className="logo">PULSEGUARD</div>
        <nav>
          {NAV.map(([id, label, icon]) => (
            <a key={id} href={`#${id}`} className={active === id ? "on" : ""} onClick={() => setActive(id)}>
              <Ic>{icon}</Ic>{label}
            </a>
          ))}
        </nav>
      </aside>

      <main id="overview">
        <section className="hero">
          <small>rPPG-based deepfake screening</small>
          <h1>Beyond the Face. <span>Beneath the Pixels.</span></h1>
          <p>Instead of examining only what a face looks like, PulseGuard investigates what subtle physiological information a face reveals over time, using the faint colour changes of a heartbeat as an extra layer of evidence.</p>
          <div className="cta">
            <a className="btn" href="#analysis">Start Analysis <Arrow /></a>
            <a className="btn ghost" href="#method">Explore Technology <Ic><circle cx="12" cy="12" r="9" /><path d="M12 11v5M12 8h.01" /></Ic></a>
          </div>
          <svg className="pulse" viewBox="0 0 1200 90" preserveAspectRatio="none" aria-hidden="true">
            <defs><linearGradient id="pg"><stop offset="0" stopColor="#5b4cff" /><stop offset="1" stopColor="#c040e0" /></linearGradient></defs>
            <path d="M0 45H180l15-30 22 62 18-50 12 18h140l15-30 22 62 18-50 12 18h140l15-30 22 62 18-50 12 18h140l15-30 22 62 18-50 12 18h140" />
          </svg>
        </section>

        <h2>The idea</h2>
        <section className="row3">
          {IDEA.map(([b, h, p]) => <div className="card" key={b}><b>{b}</b><h3>{h}</h3><p>{p}</p></div>)}
        </section>

        <section className="wide" id="method">
          <div className="slab"><h3>How it works</h3>
            <ol>
              <li>Upload a short video with a visible face</li>
              <li>Detect the face and select skin regions</li>
              <li>Extract RGB variations across frames</li>
              <li>Filter noise and analyse frequencies</li>
              <li>Estimate a heart rate for each region</li>
              <li>Compare regions for consistency and signal quality</li>
              <li>Review the evidence and flag the video for review</li>
            </ol>
          </div>
          <div className="slab" id="about"><h3>Research grounding</h3>
            <p>Built with Python, FastAPI, OpenCV, MediaPipe, SciPy and React. Physiological detection is not new, since Intel’s FakeCatcher explored it, so our goal is to implement, evaluate and extend it, including how lighting, motion and compression affect results.</p>
          </div>
        </section>

        <h2 id="analysis">Start a new analysis</h2>
        <label
          className={"drop" + (over ? " over" : "")}
          onDragOver={(e) => { e.preventDefault(); setOver(true); }}
          onDragLeave={() => setOver(false)}
          onDrop={(e) => { e.preventDefault(); setOver(false); pick(e.dataTransfer.files[0]); }}
        >
          <input type="file" accept=".mp4,.mov,.avi,video/*" onChange={(e) => pick(e.target.files[0])} />
          <strong>Drop a video here or click to upload</strong><br />
          <span>Short clip with a clearly visible face</span>
          {file && <span className="fname">{file.name} · {(file.size / 1048576).toFixed(1)} MB</span>}
        </label>
        <div className="cta" style={{ marginTop: 18 }}>
          <button className="btn" type="button" onClick={run} disabled={status === "running"}>
            {status === "running" ? "Analysing…" : "Analyse video"} <Arrow />
          </button>
        </div>
        {error && <p className="note err">{error}</p>}

        {status === "running" && (
          <>
            <ul className="steps">
              {STEPS.map((s, i) => <li key={s} className={i < step ? "done" : i === step ? "now" : ""}><i />{s}</li>)}
            </ul>
            {slow && <p className="note">The server may be waking up after being idle. The first analysis can take up to a minute.</p>}
          </>
        )}

        <h2 id="results">Results</h2>
        {!result ? (
          <section className="row4">
            {TILES.map(([h, p, icon]) => (
              <div className="tile" key={h}><svg viewBox="0 0 100 56">{icon}</svg><div><h3>{h}</h3><p>{p}</p></div></div>
            ))}
          </section>
        ) : (
          <>
            <div className={"verdict " + (inconclusive ? "warn" : "ok")}>
              <span className="badge">{pretty(result.assessment)}</span>
              <p>{inconclusive
                ? "The pulse signal was too weak or noisy to judge. Try a clearer, well-lit clip with a steady face."
                : "The pulse signal is usable. This does not prove the video is real or fake, so review the evidence below."}</p>
            </div>

            <section className="row3">
              {Object.entries(result.heart_rates || {}).map(([k, v]) => (
                <div className="card" key={k}><b>{pretty(k)}</b><h3 className="big">{fmt(v, 0)} <small>BPM</small></h3></div>
              ))}
            </section>

            <section className="wide">
              <div className="slab"><h3>Cross-region agreement</h3>
                <div className="bar"><span style={{ width: `${corr === null ? 0 : Math.max(0, Math.min(1, corr)) * 100}%` }} /></div>
                <p>Mean correlation between region signals: <b>{fmt(corr, 2)}</b>. Heart-rate gap between regions: <b>{fmt(rf.hr_difference_bpm)} BPM</b>. Higher correlation and a smaller gap mean the regions tell the same story.</p>
              </div>
              <div className="slab"><h3>Signal quality</h3>
                <span className="badge" style={inconclusive ? { background: "#cfc8e2", color: "#1b1040" } : {}}>{pretty(q.quality || "unknown")}</span>
                <div className="stats">
                  <span>Valid regions: {rf.valid_regions ?? "—"}</span>
                  <span>Duration: {fmt(vd.duration_seconds)} s</span>
                  <span>{fmt(vd.fps, 0)} fps</span>
                  <span>{vd.sampled_frames ?? "—"} frames</span>
                </div>
              </div>
            </section>

            <details><summary>Raw analysis data</summary><pre>{JSON.stringify(result, null, 2)}</pre></details>
            {result.disclaimer && <p className="note">{result.disclaimer}</p>}
          </>
        )}

        <footer>PulseGuard · a screening aid, not a guarantee</footer>
      </main>
    </div>
  );
}
