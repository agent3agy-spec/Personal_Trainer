#!/bin/sh
# Rebuild the page and send it to Cloudflare Pages (project personal-trainer). The link stays the same.
set -e
cd "$(dirname "$0")/.."
python3 site/build_bundle.py
cp site/index.html site/app.js site/app.css site/mark.png site/bundle.json share/web/
cd share/web
wrangler pages deploy . --project-name personal-trainer --branch main --commit-dirty=true
