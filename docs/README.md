# Compatibility checker

This directory hosts the static site for the Claude Skill compatibility checker — a single-page tool that takes a `SKILL.md` and reports which Claude platforms (Claude.ai, Claude Code, Claude Desktop) it'll work on without silent fallbacks, schema errors, or behavioral divergence.

Local preview:

```
open docs/index.html
# or
python3 -m http.server 8000 --directory docs
```

To publish via GitHub Pages: in the repo settings, set Pages → Source → "Deploy from a branch", Branch = `main`, Folder = `/docs`. The site will be served at `https://<owner>.github.io/claude-skills-pitfalls/`.

## How detection works

The page does static regex matching over the pasted text for tool names and patterns that appear in the catalog (e.g. `Write`, `ask_user_input_v0`, `references/foo.md`, `pip install`). Each match maps to per-platform status (`ok` | `caveat` | `missing`) and links to the pitfall page that explains the divergence.

This is intentionally shallow — it catches what the catalog covers, not every possible runtime issue. False negatives are likely; treat a green report as "no known catalog hit," not "guaranteed to work."

## Contributing a new detection

Edit the `TOOLS` array in `index.html`. Each entry needs:

- `id` — tool name shown in the report
- `pattern` — a global regex matched against the input text
- `platforms` — for each of `claude.ai`, `code`, `desktop`: `{ status, reason, href }` where `status` is `ok | caveat | missing` and `href` points to the relevant pitfall page

Keep `reason` strings short and copy-editable — they appear inline in the report.
