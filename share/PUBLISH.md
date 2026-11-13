# Publishing the trainer

Live link: https://personal-trainer-ear.pages.dev (Cloudflare Pages, project `personal-trainer`, account agent3agy@gmail.com).

The page is `share/web/` (index.html, app.js, app.css, mark.png, bundle.json, pyodide/). It is a build output, ignored by git. To update it:

Run `share/deploy.sh`: it rebuilds the bundle, copies the page into `share/web/` and deploys it. The first time, copy `site/pyodide/` into `share/web/pyodide/`.

The link stays the same. Each person's profile, plan and log live in their own browser (IndexedDB); Settings has a backup file. "Ask your trainer" is hidden here because it needs Claude (it shows inside claude.ai only).
