#!/usr/bin/env bash
# Installs the ZON web-development toolkit for Claude Code on macOS or Linux.
# Idempotent, no sudo. Review before running.
set -euo pipefail

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1 — install it first." >&2; exit 1; }; }
need claude; need node; need npx; need git

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Official Anthropic plugin marketplace"
claude plugin marketplace list 2>/dev/null | grep -q claude-plugins-official \
  || claude plugin marketplace add anthropics/claude-plugins-official

echo "== Plugins (user scope)"
for p in frontend-design skill-creator superpowers context7; do
  if claude plugin list 2>/dev/null | grep -q "$p@claude-plugins-official"; then
    echo "already installed: $p"
  else
    claude plugin install "$p@claude-plugins-official" --scope user
  fi
done

echo "== Skills (global, ~/.claude/skills) via Vercel's skills CLI"
SKILLS_CLI="skills@1.7.2"
[ -d "$HOME/.claude/skills/web-design-guidelines" ] && [ -d "$HOME/.claude/skills/vercel-react-best-practices" ] \
  && echo "already installed: Vercel skills" \
  || npx -y "$SKILLS_CLI" add vercel-labs/agent-skills --skill web-design-guidelines --skill vercel-react-best-practices -g -a claude-code -y
[ -d "$HOME/.claude/skills/webapp-testing" ] \
  && echo "already installed: webapp-testing" \
  || npx -y "$SKILLS_CLI" add anthropics/skills --skill webapp-testing -g -a claude-code -y

echo "== ZON Website Master skill"
mkdir -p "$HOME/.claude/skills"
if [ -d "$HOME/.claude/skills/zon-website-master" ]; then
  echo "exists: ~/.claude/skills/zon-website-master (left unchanged; delete it manually to reinstall)"
else
  cp -R "$REPO_ROOT/.claude/skills/zon-website-master" "$HOME/.claude/skills/"
fi

echo "== Python Playwright for webapp-testing"
if python3 -c "import playwright" 2>/dev/null; then
  echo "already installed: playwright (python)"
else
  echo "Run when ready (user-level install, downloads browsers ~150 MB):"
  echo "  python3 -m pip install --user playwright && python3 -m playwright install chromium"
fi

echo "Done. Restart Claude Code, then run /plugin and /skills to confirm."
