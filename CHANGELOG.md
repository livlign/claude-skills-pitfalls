# Changelog

All notable changes to this catalog are recorded here. Dates are ISO 8601.

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
