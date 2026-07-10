# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for ICCP 2027 (International Conference on Computational Photography), Princeton, NJ. Hosted on GitHub Pages at iccp2027.iccp-conference.org. Currently a placeholder — all pages except the homepage are commented out of navigation.

## Tech Stack

- Plain HTML5, CSS3, vanilla JavaScript (no framework, no build system)
- Bulma CSS for layout/components, Font Awesome for icons
- jQuery for DOM manipulation
- Python utility (`crop_headshots.py`) for speaker headshot processing (requires `opencv-python`, `numpy`)

## Development

No build step. To run locally:
```bash
python3 -m http.server 8000
```
Then open http://localhost:8000.

Deployment is automatic via GitHub Pages on push to `main`.

## Git

Use the personal SSH key for all git operations:
```bash
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519' git push ...
```

## Architecture

**Single-Page Application with hash-based routing.** `index.html` is the shell; content pages live in `pages/` and are fetched dynamically.

- `index.html` — App shell with header, navigation buttons, hero section, and `<div id="content">` container
- `static/js/index.js` — Core routing logic: `loadContent()` reads `window.location.hash`, fetches `pages/{hash}.html`, injects into `#content`. Supports deep linking via `#page/section` format
- `pages/*.html` — Partial HTML fragments (not full documents) loaded into the content container
- `static/css/index.css` — Custom styles using CSS variables (`--bg-grey`, `--bg-red`, `--bg-blue`, etc.)

**Navigation flow:** Button click or hash change → `loadContent()` → fetch page fragment → inject into DOM → update active button styling → scroll to anchor if subsection specified.

## Key Directories

- `pages/` — Content page fragments (home, venue, talks, callforpapers, team, sponsors, etc.)
- `static/css/` — Bulma (minified) + custom styles
- `static/js/` — App logic + vendored libraries (bulma-carousel, bulma-slider, fontawesome)
- `static/img/` — All images: `speakers/`, `team/`, `logos/` (sponsor SVGs), `talk-content/`, `lodging-venue/`
- `static/materials/` — Downloadable files (LaTeX template, program CSV/SVG)
