const STEPS = [
  ["Find the face", "MediaPipe locates facial landmarks in every sampled frame."],
  ["Pick skin regions", "The forehead and both cheeks are cropped from the face."],
  ["Read colour over time", "The average red, green and blue value of each region is recorded per frame."],
  ["Clean the signal", "The trace is resampled, detrended and filtered to the 0.7 to 4 Hz heart-rate band."],
  ["Estimate the pulse", "A frequency analysis finds the strongest rhythm, giving a heart rate and a signal-to-noise figure."],
  ["Compare regions", "Heart rates and waveforms from the three regions are checked for agreement."],
  ["Check quality", "If the signal is weak, the result is Inconclusive instead of a guess."],
];
const LIMITS = [
  "No trained real/fake classifier is connected yet, so the result is a signal report, not a verdict.",
  "Video compression, low light and head movement weaken the pulse signal.",
  "Some deepfakes keep the pulse of the source video, so a normal pulse does not prove a video is real.",
  "Accuracy can vary across skin tones and lighting. Test before relying on it.",
];

export default function Methodology() {
  return (
    <div className="doc">
      <h2>How PulseGuard works</h2>
      <p className="hint">Each heartbeat changes how much light skin reflects. A camera can pick this up, and it is hard to fake consistently.</p>
      <ol className="panel pad">{STEPS.map(([t, d]) => <li key={t}><strong>{t}.</strong> {d}</li>)}</ol>
      <h3>What it cannot do</h3>
      <ul className="panel pad">{LIMITS.map((l) => <li key={l}>{l}</li>)}</ul>
      <p className="hint">Related research: Intel FakeCatcher, DeepFakesON-Phys.</p>
    </div>
  );
}
