# PulseGuard frontend

Run the backend (from `backend/`):  `uvicorn main:app --reload`
Run this app (from `frontend/`):    `npm install` then `npm run dev`  -> http://localhost:5173

If the backend is elsewhere, create `.env` with `VITE_API_URL=http://host:port`.

## Backend change for waveforms and spectra
Add these two helpers and fields to the dict returned by `analyze_video` in `backend/pipeline.py`:

    def _band_spectrum(out):
        f = np.asarray(out["frequencies"]); p = np.asarray(out["power_spectrum"])
        m = (f >= 0.7) & (f <= 4.0)
        return {"bpm": [round(float(x * 60), 1) for x in f[m]], "power": [float(x) for x in p[m]]}

    "waveforms": {n: {"fs": 15, "values": [round(float(v), 3) for v in o["filtered_signal"]]}
                  for n, o in region_outputs.items()},
    "spectra": {n: _band_spectrum(o) for n, o in region_outputs.items()},

Optional: when the classifier exists, add `"fake_probability": 0.0-1.0` and the UI shows it.

## Hero image
The Overview page draws a landmark-mesh illustration. To use a real portrait instead, save an image as `public/hero-face.png`.
Use a photo you have rights to, ideally one you recorded yourself.
