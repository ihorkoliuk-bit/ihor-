# Claude Code web-development setup for ZON: installation report

Date: 2026-10-17. Environment tested: Claude Code 2.1.302, Node 22.22.0, npm 10.9.4, Git 2.43.0, Python 3.13 (Linux cloud session).

## Sources (verified)

| Component | Source | Install method |
|---|---|---|
| Frontend Design | `anthropics/claude-plugins-official` → `plugins/frontend-design` | `claude plugin install frontend-design@claude-plugins-official` |
| Skill Creator | `anthropics/claude-plugins-official` → `plugins/skill-creator` | `claude plugin install skill-creator@claude-plugins-official` |
| Superpowers 7.0.0 | `obra/superpowers`, pinned by the official Anthropic marketplace | `claude plugin install superpowers@claude-plugins-official` |
| Context7 | `anthropics/claude-plugins-official` → `external_plugins/context7` (Upstash hosted MCP) | `claude plugin install context7@claude-plugins-official` |
| Web App Testing | `anthropics/skills` → `skills/webapp-testing` | `npx skills add anthropics/skills --skill webapp-testing -g -a claude-code` |
| Web Design Guidelines | `vercel-labs/agent-skills` → `skills/web-design-guidelines` | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines -g -a claude-code` |
| React Best Practices | `vercel-labs/agent-skills` → `skills/react-best-practices` (skill name `vercel-react-best-practices`) | same CLI |

The `skills` CLI is Vercel's npm package (`vercel-labs/skills`, maintainer rauchg), pinned to 1.7.2. Installed skill files were diffed against the upstream repositories: identical.

## Results

| Component | Status | Test performed |
|---|---|---|
| frontend-design | Installed, ready | Plugin loads, 1 skill registered |
| skill-creator | Installed, ready | Its `quick_validate.py` used to validate all skills below |
| superpowers | Installed, ready | 15 skills registered; SessionStart hook executed and emitted context; hook script reviewed (no network or destructive commands) |
| context7 | Installed, **blocked here** | MCP endpoint `mcp.context7.com` denied by this cloud environment's network policy. Works anonymously on a normal network; optional `CONTEXT7_API_KEY` raises rate limits (free tier exists; paid tiers not required) |
| webapp-testing | Installed, ready | Playwright smoke test: 4 viewports, keyboard order, reduced motion, console errors: PASS |
| web-design-guidelines | Installed, ready | Skill valid; fetches rules from `raw.githubusercontent.com/vercel-labs/web-interface-guidelines` (reachable) |
| vercel-react-best-practices | Installed, ready | Skill valid |
| zon-website-master | Created, ready | Skill valid; tokens tested in a page rendered by Playwright |
| Python Playwright 1.64 | Installed (pip) | Uses preinstalled Chromium |

## Notes

- `with_server.py` from webapp-testing launches the server through a shell; prefix the command with `exec` or the server outlives the test and blocks the port.
- `.claude/settings.json` in this repository declares the official marketplace and enables the four plugins for anyone who opens the project in Claude Code (they are asked to trust it first).
- To set up a Mac: `bash scripts/setup-claude-web-dev.sh` (idempotent, no sudo). Python Playwright is only suggested, not auto-installed.

## ZON Website Master skill

Path: `.claude/skills/zon-website-master/` (copy installed globally at `~/.claude/skills/zon-website-master/`).

`references/verified-facts.md` is intentionally empty. Until it is filled from official ZON sources, the skill writes `[[VERIFY: …]]` placeholders instead of facts. The fonts (Cormorant Garamond, Inter) and exact hex values are working defaults until official brand guidelines replace them.
