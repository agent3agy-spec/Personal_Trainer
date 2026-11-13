# 05 · Claude Code and GitHub mechanics

_Research return 13 nov 2026, checked by a docs subagent. Marks: [checked] = read in the official docs this session, [believe] = from a search snippet or memory. docs.github.com did not resolve from the session, so the GitHub items are [believe] and must be checked at milestone 1._

## Claude Code

| question | answer | mark | source |
|:-|:-|:-|:-|
| project skill path | `.claude/skills/<name>/SKILL.md`, committed with the repo, becomes the slash command `/<name>` | [checked] | https://code.claude.com/docs/en/skills.md |
| useful frontmatter | `name`, `description`, `argument-hint`, `disable-model-invocation`, `allowed-tools`, `model`, `context: fork`. `disable-model-invocation: true` makes it run only when typed | [checked] | same |
| old `.claude/commands/` | still works, the older format | [checked] | same |
| CLAUDE.md | `./CLAUDE.md` loads at the start of every session in the repo. `@path` imports, four hops deep. Keep under 200 lines | [checked] | https://code.claude.com/docs/en/memory.md |
| subagents | `.claude/agents/<name>.md`, YAML frontmatter `name`, `description`, optional `tools`, `model` (`haiku`, `sonnet`, `opus`, `inherit`), then the prompt. Called through the `Agent` tool (alias `Task`) | [checked] | https://code.claude.com/docs/en/sub-agents.md |
| pre-allowed commands | `permissions.allow` in a committed `.claude/settings.json`. They apply only after the user trusts the folder. Allow narrow commands only, never `python3 *`. Syntax uses the space form, `Bash(python3 engine/sheet.py *)` | [checked] | https://code.claude.com/docs/en/settings.md, https://code.claude.com/docs/en/permissions.md |
| SessionStart hook | stdout goes into Claude's context, not shown to the user | [checked] | https://code.claude.com/docs/en/hooks-guide.md |
| install | macOS, Linux, WSL: `curl -fsSL https://claude.ai/install.sh \| bash` · Windows PowerShell: `irm https://claude.ai/install.ps1 \| iex` · also the Homebrew cask `claude-code`, `winget install Anthropic.ClaudeCode`. Then `claude`, log in | [checked] | https://code.claude.com/docs/en/quickstart.md |
| plans | Free does not include Claude Code. Pro $20 a month ($17 annual), Max $100, Team seats, Enterprise. Console (API) login also supported. Prices change, link the live page, never print a price on the site | [checked] 13 nov 2026 | https://claude.com/pricing |
| no install at all | Claude Code on the web (claude.ai/code), on Pro and above, works on a GitHub repo through the Claude GitHub App, also on a phone | [checked] | https://code.claude.com/docs/en/claude-code-on-the-web.md |

## GitHub

| question | answer | mark |
|:-|:-|:-|
| template | Settings, tick "Template repository". Others press "Use this template", choose owner, name and **private** visibility | [believe] |
| direct link | `https://github.com/OWNER/REPO/generate` opens the create page | [believe] |
| history | the new repo starts with one commit, no link back to the template, so updates have to be pulled by hand (a remote called `upstream`) | [believe] |
| fork vs template | a fork of a public repo stays public and keeps full history: wrong for health data. Template is the only right choice | [believe] |
| Pages | source is a branch (root or `/docs`) or a GitHub Actions workflow. Pages settings are not copied to a template copy, but **workflow files are**, so a Pages workflow must be guarded to the upstream repo | [believe] |
| Pages on private repos | needs a paid plan, which is another reason the user's copy never publishes | [believe] |
