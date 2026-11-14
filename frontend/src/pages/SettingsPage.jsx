import { API } from "../api";

export default function SettingsPage({ online }) {
  return (
    <div className="doc">
      <h2>Settings</h2>
      <dl className="panel pad">
        <dt>Backend address</dt><dd>{API}</dd>
        <dt>Backend status</dt><dd>{online ? "Online" : "Offline"}</dd>
      </dl>
      <p className="hint">To change the address, create a .env file in the frontend folder with VITE_API_URL=http://host:port and restart npm run dev.</p>
    </div>
  );
}
