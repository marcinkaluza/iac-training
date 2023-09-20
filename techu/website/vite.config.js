import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "https://djm5s3dmokx3f.cloudfront.net",
        changeOrigin: false,
        secure: true,
        //rewrite: (path) => path.replace("/api", ""),
      },
      "/bapi": {
        target: "https://jsonplaceholder.typicode.com",
        changeOrigin: false,
        secure: false,
        rewrite: (path) => path.replace("/bapi", ""),
      },
    },
  },
});
