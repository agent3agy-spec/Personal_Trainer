# Setup · from the link to your first sheet

_About 10 minutes if you already use Claude Code, 20 to 25 if you are installing it. Nothing here needs you to know how to code._

## What you need

| | why | cost |
|:-|:-|:-|
| a GitHub account | your copy of the trainer lives there, private | free, two minutes at github.com/signup |
| a Claude plan with Claude Code | Claude is the coach | the free plan does not include it: see claude.com/pricing |

## Step 1 · Your own copy

1. On the trainer's GitHub page, press the green **Use this template** button, then **Create a new repository**.
2. Owner: you. Name: `personal-trainer`. Visibility: **Private** (important: your health answers will live here).
3. Press **Create repository**.

## Step 2 · Open it with Claude Code

### A · In your browser (easiest, works on a phone too)

1. Go to **claude.ai/code** and sign in.
2. Connect GitHub when it asks, and allow access to your `personal-trainer` repository.
3. Start a session on `personal-trainer`.

### B · On your computer (on Windows, the browser path above is simpler)

Once:

| | Mac | Windows |
|:-|:-|:-|
| Python 3 | usually there already (Terminal offers it on first use) | install from python.org and tick "Add python.exe to PATH" |
| Git | open Terminal, type `git`, accept the install prompt | install "Git for Windows" from git-scm.com |
| GitHub CLI | from cli.github.com | from cli.github.com |
| Claude Code | in Terminal: `curl -fsSL https://claude.ai/install.sh \| bash` | in PowerShell: `irm https://claude.ai/install.ps1 \| iex` |

Then, in Terminal or PowerShell:

```
gh auth login
gh repo clone YOUR-GITHUB-NAME/personal-trainer
cd personal-trainer
claude
```

`gh auth login` signs you in to GitHub in your browser, so your private copy can be downloaded and your sessions saved back to it. The first time Claude Code opens, it asks you to log in to Claude and whether you trust this folder: say yes (that is what lets the trainer save your sessions without asking every time).

## Step 3 · Type `/train`

That's it. It will:
1. run a 12-item safety check (one reply),
2. ask about your goal, your week, your place and you (three short rounds, mostly taps),
3. show you three programs with one recommended,
4. offer your first session: four taps about today, then your PDF.

**Opening your sheet:** in the browser, tap the link it gives you (it opens the PDF on GitHub). On a computer, click the file path, or find it in the `sessions` folder.

**After training:** type `/train` again (or just "done") and tell it how it went in your own words.

## If something goes wrong

| what you see | what to do |
|:-|:-|
| "Use this template" is not there | you are not on the trainer's main page, or not signed in to GitHub |
| `gh: command not found` / `claude: command not found` | close and reopen Terminal after installing; on Windows, reopen PowerShell |
| Claude Code asks permission for every step | you said no to trusting the folder: close it, run `claude` again in the folder and say yes |
| the sheet is an HTML file, or the PDF looks plain | no browser engine was found on your computer: the plain PDF works fine; installing Google Chrome gives the nicer one |
| "saved on this session's branch but NOT on main" (browser) | open your repository on GitHub, and merge the pull request or branch it made; or train from a computer |
| it says your copy is public | on GitHub: Settings, General, Danger zone, Change visibility, Private |
| you want to start over | `/train forget`, or delete the repository and make a new copy |
