import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

// This config's own directory (extension/src/popup) is the Vite project
// root, resolved from the config file's location so `npm run build:popup`
// works the same regardless of the shell's current directory. Output goes
// to extension/dist/popup with fixed, non-hashed filenames so
// manifest.json's `action.default_popup: "popup/index.html"` and its
// sibling assets resolve reliably inside the unpacked extension.
const root = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  root,
  // Relative asset base: index.html is served from chrome-extension://<id>/popup/,
  // so script/style URLs must resolve relative to that file (./main.js), not
  // the default absolute "/main.js" (which would resolve to the extension
  // root, not the popup subfolder, and fail to load).
  base: "./",
  plugins: [react()],
  build: {
    outDir: "../../dist/popup",
    emptyOutDir: true,
    rollupOptions: {
      input: `${root}index.html`,
      output: {
        entryFileNames: "main.js",
        chunkFileNames: "main.js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "main.css";
          }
          return "[name][extname]";
        },
      },
    },
  },
});
