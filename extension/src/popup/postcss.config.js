const path = require("path");

// Explicit config path: without it, the tailwindcss PostCSS plugin resolves
// tailwind.config.js relative to process.cwd() (wherever `vite build` was
// invoked from), not relative to this file -- which silently produces an
// empty `content` warning and no generated utility classes when this build
// is run from the extension/ root via `npm run build:popup`.
module.exports = {
  plugins: {
    tailwindcss: { config: path.join(__dirname, "tailwind.config.js") },
    autoprefixer: {},
  },
};
