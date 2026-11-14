import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Port 5173 is what backend/main.py allows in CORS.
export default defineConfig({ plugins: [react()], server: { port: 5173 } });
