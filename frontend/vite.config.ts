// frontend/vite.config.ts — конфиг Vite (proxy на backend) // (я добавил)
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // (я добавил)
    port: 5173, // (я добавил)
    proxy: {
      "/api": {
        target: "http://backend:8000", // (я добавил)
        changeOrigin: true, // (я добавил)
      },
    },
  },
});
