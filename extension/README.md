# ContextOS -- Chrome Extension (Manifest V3)

This is the browser-extension half of ContextOS. It talks to the local
ContextOS backend (see `../backend`, run via `../docker-compose.yml`).

## Structure

- `manifest.json` -- MV3 manifest.
- `src/background.ts` -- the service worker. The only place that calls the
  backend over HTTP or messages the content script.
- `src/content.ts` -- injected into every page; extracts page text on
  request from the background worker.
- `src/popup/` -- the popup UI (Vite + React + TypeScript + Tailwind).
  Talks only to the background worker via `chrome.runtime.sendMessage`.
- `src/messages.ts` -- shared message-type contracts used by all three.

## Develop / build

```bash
npm install
npm run build       # builds background.js + content.js + the popup bundle
```

Under the hood, `npm run build` runs:
- `npm run compile` -- esbuild bundles `src/background.ts` and
  `src/content.ts` into `dist/background.js` / `dist/content.js`, and copies
  `manifest.json` into `dist/manifest.json`.
- `npm run build:popup` -- Vite builds `src/popup/` into `dist/popup/`
  (`index.html`, `main.js`, `main.css`, fixed non-hashed filenames).

The result is a complete unpacked extension rooted at `extension/dist/`.

## Load into Chrome

1. Run `npm run build` (above).
2. Open `chrome://extensions`.
3. Enable **Developer mode** (top right).
4. Click **Load unpacked** and select the `extension/dist` folder.

## Use

1. Make sure the backend is running (`docker compose up -d` from the repo
   root).
2. Navigate to any page, open the ContextOS popup, and click
   **Index This Page**.
3. Ask a question in the popup -- it's answered using everything you've
   indexed so far, with source citations (clickable when the source is a
   URL).

## Known gaps

- No options page yet -- the backend URL defaults to
  `http://localhost:8000` and can only be overridden by setting
  `chrome.storage.local`'s `backendUrl` key manually (e.g. from the
  extension's service worker console).
- Page text extraction (`src/content.ts`) is a naive `document.body.innerText`
  dump, not a readability-style extraction -- it will include nav/ads/etc.
  See the TODO comment in that file.
- No icon assets are included (`manifest.json` omits the `icons` key, so
  Chrome shows a generic icon). Add real icons before any Chrome Web Store
  submission.
- Packaging for the Chrome Web Store (zipping `dist/`, a developer account,
  store listing) is out of scope for this skeleton.
