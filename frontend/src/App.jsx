import { useEffect, useRef, useState } from "react";
import { Home, Play, BarChart3, BookOpen, Settings, ShieldCheck, ArrowRight } from "lucide-react";
import { analyzeVideo, health } from "./api";
import Overview from "./pages/Overview";
import Analyze from "./pages/Analyze";
import Methodology from "./pages/Methodology";
import SettingsPage from "./pages/SettingsPage";
import Results from "./components/Results";

const NAV = [
  ["overview", "Overview", Home],
  ["analyze", "New Analysis", Play],
  ["results", "Results", BarChart3],
  ["methodology", "Methodology", BookOpen],
  ["settings", "Settings", Settings],
];
const MAX_MB = 100;
const REPO = "https://github.com/Yuktibajaj20/pulseguard-rppg-deepfake";

export default function App() {
  const [page, setPage] = useState("overview");
  const [online, setOnline] = useState(false);
  const [a, setA] = useState({ file: null, url: null, status: "idle", result: null, error: "" });
  const ctrl = useRef(null);

  useEffect(() => {
    let alive = true;
    const ping = () => health().then((ok) => alive && setOnline(ok));
    ping();
    const id = setInterval(ping, 15000);
    return () => { alive = false; clearInterval(id); };
  }, []);

  async function run(file) {
    if (!file) return;
    setPage("analyze");
    if (!/\.(mp4|mov|avi)$/i.test(file.name)) return setA((s) => ({ ...s, status: "error", error: "Use an .mp4, .mov or .avi file." }));
    if (file.size > MAX_MB * 1048576) return setA((s) => ({ ...s, status: "error", error: `That file is over ${MAX_MB} MB. Trim or compress it first.` }));
    ctrl.current?.abort();
    ctrl.current = new AbortController();
    setA((s) => { if (s.url) URL.revokeObjectURL(s.url); return { file, url: URL.createObjectURL(file), status: "loading", result: null, error: "" }; });
    try {
      const result = await analyzeVideo(file, ctrl.current.signal);
      setA((s) => ({ ...s, status: "done", result }));
    } catch (err) {
      if (err.name !== "AbortError") setA((s) => ({ ...s, status: "error", error: err.message }));
    }
  }

  const titles = { overview: "", analyze: "New analysis", results: "Results", methodology: "Methodology", settings: "Settings" };

  return (
    <div className="shell">
      <nav className="side" aria-label="Main">
        <div className="logo"><ShieldCheck size={46} strokeWidth={1.5} /><b>PULSEGUARD</b></div>
        <ul>
          {NAV.map(([id, text, Icon]) => (
            <li key={id}>
              <button className={page === id ? "on" : ""} aria-current={page === id ? "page" : undefined} onClick={() => setPage(id)}>
                <Icon size={19} /> {text}
              </button>
            </li>
          ))}
        </ul>
        <div className="status"><i className={online ? "up" : "down"} />{online ? "System online" : "Backend offline"}<small>Prototype</small></div>
      </nav>

      <div className="main">
        <header className="top">
          <span className="tagline">{titles[page] || "Beyond the face. Beneath the pixels."}</span>
          <div>
            <button className="link" onClick={() => setPage("methodology")}>Methodology</button>
            <a className="link" href={REPO} target="_blank" rel="noreferrer">GitHub</a>
            <button className="btn primary sm" onClick={() => setPage("analyze")}>Start Analysis <ArrowRight size={16} /></button>
          </div>
        </header>

        <main className="page">
          {page === "overview" && <Overview go={setPage} />}
          {page === "analyze" && <Analyze a={a} run={run} />}
          {page === "results" && (a.result
            ? <Results result={a.result} />
            : <p className="empty big">No results yet. <button className="link" onClick={() => setPage("analyze")}>Analyse a video</button> to see them here.</p>)}
          {page === "methodology" && <Methodology />}
          {page === "settings" && <SettingsPage online={online} />}
        </main>
      </div>
    </div>
  );
}
