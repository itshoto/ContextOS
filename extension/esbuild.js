// Bundles the background service worker and content script into dist/,
// and copies manifest.json alongside them. The popup (React/Vite app under
// src/popup/) is built separately via `npm run build:popup` (see
// src/popup/vite.config.ts), which writes into dist/popup/.
const fs = require("fs");
const path = require("path");
const esbuild = require("esbuild");

const watch = process.argv.includes("--watch");
const production = process.argv.includes("--production");

function copyManifest() {
  fs.mkdirSync("dist", { recursive: true });
  fs.copyFileSync(
    path.join(__dirname, "manifest.json"),
    path.join(__dirname, "dist", "manifest.json")
  );
}

async function main() {
  copyManifest();

  // background.js is declared `"type": "module"` in manifest.json, so it can
  // be bundled as an ES module. content.js is injected as a classic script
  // (MV3 content_scripts don't support module type), so it must be an IIFE
  // with no top-level import/export statements.
  const backgroundCtx = await esbuild.context({
    entryPoints: { background: "src/background.ts" },
    bundle: true,
    format: "esm",
    platform: "browser",
    target: "es2022",
    outdir: "dist",
    sourcemap: !production,
    minify: production,
    logLevel: "info",
  });

  const contentCtx = await esbuild.context({
    entryPoints: { content: "src/content.ts" },
    bundle: true,
    format: "iife",
    platform: "browser",
    target: "es2022",
    outdir: "dist",
    sourcemap: !production,
    minify: production,
    logLevel: "info",
  });

  if (watch) {
    await backgroundCtx.watch();
    await contentCtx.watch();
  } else {
    await backgroundCtx.rebuild();
    await contentCtx.rebuild();
    await backgroundCtx.dispose();
    await contentCtx.dispose();
    copyManifest(); // re-copy in case dist was cleared by the rebuild
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
