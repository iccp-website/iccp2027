# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for ICCP 2027 (International Conference on Computational Photography), August 2–4, 2027, University of Maryland, College Park. Hosted on GitHub Pages at iccp2027.iccp-conference.org (see `CNAME`); deploys automatically on push to `main`.

The repo was cloned from the ICCP 2026 site (Princeton, NJ). Only Home, Call for Papers, Summer School, and Team are live in the nav; the other nav buttons are commented out in `index.html`. Pages not yet in the nav (venue, lodging, program, talks, etc.) and `static/materials/` still contain 2026/Princeton content and need rewriting before they go live.

## Development

No build system, linter, or tests. Serve locally (pages are loaded with `fetch`, so `file://` won't work):
```bash
python3 -m http.server 8000
```

`crop_headshots.py` (needs `opencv-python`, `numpy`; run from repo root) face-detects and crops every image in `static/img/talk-content/` to 512×512, **overwriting the files in place**.

## Git

Use the personal SSH key for all git operations:
```bash
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519' git push ...
```

## Architecture

Single-page app with hash-based routing. `index.html` is the shell (hero header, nav buttons, footer, `<div id="content">`). The router is an **inline `<script>` at the bottom of `index.html`**:

- `loadContent()` maps `#page` → `pages/page.html` and injects it into `#content` via `innerHTML`; defaults to `home`. Requests are cache-busted (`?t=` + `no-store`).
- Deep links use `#page/sectionId`: after loading, it scrolls to the element with id `sectionId`. Dropdown items (e.g. the Program dropdown) follow the same format.
- The active nav button gets the `active-button` class by matching `a[href="#page"]`.
- To add a page: create `pages/<name>.html` and add `<a href="#<name>" class="button">` to the nav.

`pages/*.html` are HTML fragments, not full documents, usually a `<section class="section container is-max-desktop content" id="...">`. Page-specific CSS goes in a `<style>` block inside the fragment, scoped under the section id (see `team.html`). Because fragments are inserted with `innerHTML`, `<script>` tags inside them **do not execute**.

Shared styles: `static/css/index.css` (CSS variables `--bg-grey`, `--bg-red`, etc.) on top of `static/css/bulma.min.css`. Those two stylesheets are the only assets `index.html` loads. `static/js/` (including `index.js`), jQuery, Font Awesome, and the bulma-carousel/slider files are unused leftovers from the template.

The hero (title, dates, location, background image) and the footer (past ICCP years, logo, contact) are hard-coded in `index.html`.
