import Results from "../components/Results";

export default function Analyze({ a, run }) {
  return (
    <div className="analyze">
      <aside>
        <label className="drop" onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => { e.preventDefault(); run(e.dataTransfer.files?.[0]); }}>
          <input type="file" accept="video/mp4,video/quicktime,video/x-msvideo,.mp4,.mov,.avi"
            onChange={(e) => run(e.target.files?.[0])} />
          <strong>{a.file ? "Choose another video" : "Choose a video"}</strong>
          <span>or drop it here</span>
        </label>
        <ul className="tips">
          <li>15 seconds or longer</li>
          <li>One face, looking at the camera</li>
          <li>Even light, little movement</li>
        </ul>
        {a.url && <video src={a.url} controls muted playsInline />}
        {a.file && <p className="meta">{a.file.name} ({(a.file.size / 1048576).toFixed(1)} MB)</p>}
      </aside>
      <div className="stage">
        {a.status === "idle" && <p className="empty big">Upload a clip to see its pulse waveform, heart rate per face region, and how well the regions agree.</p>}
        {a.status === "loading" && (
          <div className="loading" role="status"><div className="bar" /><p>Reading the pulse from each face region. Long videos can take a minute.</p></div>
        )}
        {a.status === "error" && <p className="error" role="alert">{a.error}</p>}
        {a.status === "done" && a.result && <Results result={a.result} />}
      </div>
    </div>
  );
}
