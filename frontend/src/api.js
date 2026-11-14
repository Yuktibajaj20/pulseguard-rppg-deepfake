// Set VITE_API_URL in a .env file if your backend is not on this address.
export const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function health() {
  try {
    const res = await fetch(`${API}/`);
    return res.ok;
  } catch {
    return false;
  }
}

export async function analyzeVideo(file, signal) {
  const body = new FormData();
  body.append("file", file);

  let res;
  try {
    res = await fetch(`${API}/analyze`, { method: "POST", body, signal });
  } catch (err) {
    if (err.name === "AbortError") throw err;
    throw new Error(`Can't reach the analysis server at ${API}. Start it with: uvicorn main:app --reload`);
  }

  let data = null;
  try { data = await res.json(); } catch { /* non-JSON error body */ }
  if (!res.ok) throw new Error(data?.detail || `Analysis failed (HTTP ${res.status}).`);
  return data;
}
