# Changelog

All notable changes to this catalog are recorded here. Dates are ISO 8601.

## [Unreleased]

### Added

- **tool-behaviors/code-bash-no-cwd-or-state-carryover** — new `verified` entry: Claude Code's `Bash` resets cwd to the project directory after every call and does not carry over exported variables (reproduced on Opus 4.8, 2026-06-14). Added to the README symptom list and the tool-inventory matrix.
- **README "Find by symptom"** — expanded from 16 to all 35 entries, so every catalogued pitfall is reachable from the README by the error/symptom a stuck author would search. Improves in-repo discoverability.
- **cross-platform/view-vs-read-directory-listing** — added the verbatim Code error (`EISDIR: illegal operation on a directory`) as a reproduction, so the page surfaces when that error is searched (re-confirmed on Opus 4.8, 2026-06-14).
- **tool-behaviors/edit-old-string-must-not-include-read-line-number-prefix** — new `verified` entry: `Edit` fails with "String to replace not found in file" when `old_string` carries the `<line>\t` prefix from `Read`'s `cat -n` output (reproduced on Opus 4.8, 2026-06-14). Added to the README symptom list and the tool-behaviors index (which also gained the previously-missing `code-bash-no-cwd-or-state-carryover` link).
- **README discoverability pass** — added a keyword-rich tagline under the title and a question-shaped **FAQ** section (matching how people search and how AI assistants surface answers) linking to the most-searched entries. Set the repository homepage URL to the live site so the GitHub "About" sidebar links to the checker.
- **Web catalog (static site)** — every entry is now published as its own HTML page under `docs/pitfalls/<category>/<slug>.html`, with a browsable `docs/pitfalls/index.html`, a `docs/sitemap.xml`, and `docs/robots.txt`. This turns the catalog into dozens of individually-indexable landing pages (organic-search reach) instead of one checker page. Pages are generated from the Markdown sources by the dependency-free `tools/build_catalog.py`; each carries its own `<title>`, meta description, canonical URL, and OG tags. Linked from the checker hero and the README. Added `docs/.nojekyll` so GitHub Pages serves the subdirectories verbatim.
- **Catalog navigation** — sticky top nav (Catalog / Checker / GitHub) on every page; per-entry sidebar listing sibling entries (current highlighted) and all categories; Previous/Next links across the catalog; sticky category chips with counts on the index. Responsive collapse on narrow screens.
- **Semantic search** — the catalog index now ranks results by meaning, not substring. Entry text and the query are embedded entirely in-browser with `all-MiniLM-L6-v2` via transformers.js (loaded lazily from a CDN on first focus; ~20 MB, cached thereafter), scored by cosine similarity. Substring search runs instantly as a fallback while the model loads or if it can't (offline / CDN blocked). No backend or API key.

### Changed

- **skill-structure/skill-md-edit-no-hot-reload** (renamed from `skill-md-edit-hot-reload-unverified`) — resolved the `stub` to `verified`: edits to an already-loaded SKILL.md are **not** hot-reloaded mid-session (the body is cached at first load; restart required). Reproduced live with a throwaway skill on Opus 4.8, 2026-06-14. Updated referrers in the category README and the hot-load entry; added a README symptom line.
- **skill-structure/code-skill-directory-hot-load-works**, **skill-structure/code-skill-base-directory-header-is-informational**, **tool-behaviors/code-read-resolves-against-cwd-not-skill-dir** — re-confirmed accurate on Opus 4.8, 2026-06-14 (drift sweep); refreshed "Verified on" dates. The `Read`-cwd entry also notes relative paths still resolve against cwd despite the tool description now saying paths must be absolute.
- **tool-behaviors/desktop-bash-no-state-carryover** — corrected a false cross-platform claim: Code's `Bash` does **not** persist cwd across calls (the entry previously asserted it did). Non-carryover affects both Code and Desktop; only Claude.ai persists cwd.
- **matrix/tool-inventory.md** — updated the shell-command row (Code now flagged "no state carryover"; timeout noted as documented-not-hard-enforced) and bumped "Last updated" to 2026-06-14.

- Promoted four Claude Code entries from `schema-only` to `verified` by reproducing them live in a Claude Code session (Opus 4.8, 2026-06-14):
  - **tool-behaviors/edit-requires-prior-read-same-conversation** — added verbatim reproduction; corrected the error string to `File has not been read yet. Read it first before writing to it.`
  - **tool-behaviors/write-requires-prior-read-for-existing-files** — added reproduction confirming the gate fires only for existing files.
  - **tool-constraints/code-bash-600-second-ceiling** — **corrected**: an over-limit `timeout` (700000ms) is **not** rejected as previously inferred; it is silently accepted/clamped. Severity changed from Hard error to Silent clamp.
  - **tool-behaviors/code-bash-embedded-git-policy** — updated to the current (Opus 4.8) policy text; the `Co-Authored-By` trailer is now `Claude Opus 4.8 (1M context)` (was `4.7`) and the prohibition list has drifted. Added a warning not to hardcode version-specific git policy details.

## [0.1.0] — 2026-05-17

Initial release. 34 pitfalls across five categories, each labeled with a verification tier (`verified` / `schema-only` / `stub`) and platform applicability for Claude.ai, Claude Code, and Claude Desktop.

### Added

- **tool-constraints/** (5): schema-enforced ceilings on `ask_user_input_v0`, `image_search`, `recent_chats`, Code's `Bash`, and Desktop's `mcp__workspace__bash`.
- **tool-behaviors/** (7): `view` absolute-path requirement, Code's `Read` cwd resolution, `conversation_search` keyword-only matching, prior-`Read` requirements for `Edit` and `Write`, Code's embedded git policy, Desktop's bash state non-carryover.
- **cross-platform/** (12): `Write` vs `create_file` overwrite semantics (flagship), silent fallback when a named tool doesn't exist, `AskUserQuestion` vs `ask_user_input_v0`, the three bash-tool shapes, `view` vs `Read` directory listing, `Edit.replace_all` divergence, MCP tool-name format, MCP deferred-loading, MCP discovery layer, "don't assume" instructions without a picker, past-chat search shapes, visualization absence on Code.
- **environment/** (5): Claude.ai pip `--break-system-packages`, read-only `/mnt/user-data/uploads/`, network egress allowlist, sandbox filesystem resets (stub), Desktop bash sandbox vs Code host filesystem.
- **skill-structure/** (5): `references/` path resolution (flagship), Code's base-directory header is informational, skill-directory hot-load works, tool-names-as-instructions are non-portable, SKILL.md edit hot-reload (stub).
- Cross-platform tool inventory matrix at `matrix/tool-inventory.md`.
- Pitfall template at `pitfalls/_template.md`.
- CC BY 4.0 license, README with thesis and five "Start here" entries, CONTRIBUTING with verification-tier guidance.

[0.1.0]: https://github.com/livlign/claude-skills-pitfalls/releases/tag/v0.1.0
