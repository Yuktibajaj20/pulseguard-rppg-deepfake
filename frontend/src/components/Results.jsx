import { useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const REGIONS = {
  forehead: { label: "Forehead", color: "#22d3ee" },
  left_cheek: { label: "Left cheek", color: "#a78bfa" },
  right_cheek: { label: "Right cheek", color: "#f472b6" },
};
const label = (k) => REGIONS[k]?.label ?? k;
const color = (k) => REGIONS[k]?.color ?? "#ccc";
const fmt = (v, d = 1) => (typeof v === "number" && isFinite(v) ? v.toFixed(d) : "—");
const tip = { contentStyle: { background: "#14102f", border: "1px solid #3b3270", borderRadius: 8, color: "#f1eefe" } };

function waveSeries(w) {
  const names = Object.keys(w || {});
  if (!names.length) return { names, rows: [] };
  const fs = w[names[0]].fs || 15;
  const n = Math.max(...names.map((k) => w[k].values.length));
  const rows = Array.from({ length: n }, (_, i) => {
    const row = { t: +(i / fs).toFixed(2) };
    names.forEach((k) => { row[k] = w[k].values[i]; });
    return row;
  });
  return { names, rows };
}

function spectrumSeries(s) {
  const names = Object.keys(s || {});
  if (!names.length) return { names, rows: [] };
  const rows = s[names[0]].bpm.map((b, i) => {
    const row = { bpm: b };
    names.forEach((k) => { row[k] = s[k].power[i]; });
    return row;
  });
  return { names, rows };
}

function Verdict({ result }) {
  const ok = result.assessment === "REVIEW_REQUIRED";
  const reasons = result.signal_quality?.reasons ?? [];
  return (
    <section className={`verdict ${ok ? "ok" : "weak"}`} aria-live="polite">
      <h2>{ok ? "Pulse signal found" : "Inconclusive"}</h2>
      <p>
        {ok
          ? "Signal quality is acceptable. This does not prove the video is real or fake. Compare the regions below."
          : "The pulse signal is too weak or too inconsistent to judge this video."}
      </p>
      {reasons.length > 0 && <ul>{reasons.map((r) => <li key={r}>{r}</li>)}</ul>}
      {typeof result.fake_probability === "number" && ok && (
        <p className="prob">
          Classifier score: {(result.fake_probability * 100).toFixed(0)}% likelihood of manipulation. Treat as a screening hint only.
        </p>
      )}
    </section>
  );
}

function WaveChart({ waveforms }) {
  const { names, rows } = useMemo(() => waveSeries(waveforms), [waveforms]);
  if (!rows.length) return <p className="empty">The server did not return waveforms. Add the waveforms field to pipeline.py (see README).</p>;
  return (
    <div className="panel chart tall">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 12, right: 16, bottom: 4, left: 0 }}>
          <XAxis dataKey="t" type="number" domain={["dataMin", "dataMax"]} tickFormatter={(v) => `${v}s`} stroke="#8b87b8" />
          <YAxis hide domain={["auto", "auto"]} />
          <Tooltip {...tip} formatter={(v, k) => [fmt(v, 2), label(k)]} labelFormatter={(v) => `${v} s`} />
          {names.map((k) => (
            <Line key={k} type="monotone" dataKey={k} stroke={color(k)} strokeWidth={2} dot={false} animationDuration={1400} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function SpectrumChart({ spectra }) {
  const { names, rows } = useMemo(() => spectrumSeries(spectra), [spectra]);
  if (!rows.length) return null;
  return (
    <div className="panel chart short">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
          <XAxis dataKey="bpm" type="number" domain={["dataMin", "dataMax"]} tickFormatter={(v) => Math.round(v)} stroke="#8b87b8" />
          <YAxis hide />
          <Tooltip {...tip} formatter={(v, k) => [fmt(v, 3), label(k)]} labelFormatter={(v) => `${v} bpm`} />
          {names.map((k) => (
            <Line key={k} type="monotone" dataKey={k} stroke={color(k)} strokeWidth={2} dot={false} isAnimationActive={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function RegionTable({ result }) {
  const hr = result.heart_rates ?? {};
  const spec = result.spectral_features ?? {};
  const names = Object.keys(hr);
  if (!names.length) return <p className="empty">No region produced a usable pulse.</p>;
  return (
    <table>
      <thead><tr><th>Region</th><th>Heart rate</th><th>Peak clarity</th></tr></thead>
      <tbody>
        {names.map((k) => (
          <tr key={k}>
            <td><span className="swatch" style={{ background: color(k) }} />{label(k)}</td>
            <td>{fmt(hr[k], 0)} bpm</td>
            <td>{spec[k] ? fmt(1 - spec[k].spectral_entropy, 2) : "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function Results({ result }) {
  const reg = result.regional_features ?? {};
  const q = result.signal_quality ?? {};
  const v = result.video ?? {};
  return (
    <div className="results">
      <Verdict result={result} />
      <section>
        <h3>Pulse waveform by region</h3>
        <p className="hint">Regions of a real face tend to rise and fall together.</p>
        <WaveChart waveforms={result.waveforms} />
      </section>
      <div className="two">
        <section className="panel pad">
          <h3>Heart rate per region</h3>
          <RegionTable result={result} />
        </section>
        <section className="panel pad">
          <h3>Cross-region agreement</h3>
          <dl>
            <dt>Mean correlation</dt><dd>{fmt(reg.mean_correlation, 2)}</dd>
            <dt>Heart-rate spread</dt><dd>{fmt(reg.hr_difference_bpm, 1)} bpm</dd>
            <dt>Average signal-to-noise</dt><dd>{fmt(q.mean_snr_db, 1)} dB</dd>
            <dt>Signal quality</dt><dd>{q.quality === "ACCEPTABLE" ? "Acceptable" : "Low"}</dd>
          </dl>
        </section>
      </div>
      {result.spectra && (
        <section>
          <h3>Frequency spectrum</h3>
          <p className="hint">A single clear peak means a steady pulse. Several peaks mean noise.</p>
          <SpectrumChart spectra={result.spectra} />
        </section>
      )}
      <p className="meta">Analysed {fmt(v.duration_seconds, 1)} s of video, {v.sampled_frames ?? "—"} frames sampled.</p>
      <p className="disclaimer">{result.disclaimer}</p>
    </div>
  );
}
