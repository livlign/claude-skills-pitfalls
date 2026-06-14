# claude-skills-pitfalls

> Skills break in ways that aren't documented anywhere accessible to skill authors. Some breakages are hidden constraints on a single tool. Some are differences between platforms. Some are silent fallbacks the author never notices. This repo catalogs them — with reproductions — so you find the answer when you search for the error, not when you read 4,000 lines of system prompt.

## What this is / what this isn't

- Is: a catalog of runtime pitfalls when writing skills, with reproductions where possible
- Is: cross-platform (Claude.ai, Claude Code, Claude Desktop)
- Isn't: a tutorial on how to write skills (see Anthropic's [`skill-creator`](https://github.com/anthropics/skills))
- Isn't: a bug tracker for Anthropic (file those upstream)
- Isn't: prompt engineering tips

## Start here

If you read five entries, read these:

1. [`Write` overwrites silently; `create_file` refuses to overwrite](pitfalls/cross-platform/write-vs-create-file-overwrite-semantics.md) — most dangerous cross-platform divergence
2. [Skills fail silently when their named tool doesn't exist](pitfalls/cross-platform/silent-fallback-when-tool-missing.md) — explains why your skill "works" on your platform and produces gibberish on others
3. [`ask_user_input_v0` has hidden 3×4 limits](pitfalls/tool-constraints/ask-user-input-v0-question-and-option-limits.md) — the pitfall that started this repo
4. [`AskUserQuestion` and `ask_user_input_v0` are different tools](pitfalls/cross-platform/askuserquestion-vs-ask-user-input-v0.md) — same purpose, different schemas, different limits
5. [`references/` paths don't resolve from the skill's directory](pitfalls/skill-structure/references-directory-path-resolution.md) — corrects an officially-recommended pattern

## How to use this repo

Four entry points:

- **Paste your SKILL.md:** the [compatibility checker](docs/index.html) ([live](https://livlign.github.io/claude-skills-pitfalls/)) flags every catalogued pitfall in your skill, per platform
- **By tool / failure type:** browse [`pitfalls/`](./pitfalls/) by category
- **By platform:** check the [compatibility matrix](matrix/tool-inventory.md) to see if your skill's tools exist on the platform you're targeting
- **By symptom:** scan the "Find by symptom" list below for the phrase that matches what your skill is doing wrong

## Find by symptom

If you arrived here from a Google search, the entry that matches your symptom is probably one of these:

- "My skill works on Claude.ai but produces gibberish on Claude Code / Desktop" → [Skills fail silently when their named tool doesn't exist](pitfalls/cross-platform/silent-fallback-when-tool-missing.md)
- "`Write` overwrote my file with no warning" → [Write vs create_file overwrite semantics](pitfalls/cross-platform/write-vs-create-file-overwrite-semantics.md)
- "`Edit` failed with 'you must use Read first'" → [Edit requires a prior Read in the same conversation](pitfalls/tool-behaviors/edit-requires-prior-read-same-conversation.md)
- "`Edit` failed with 'String to replace not found' but the text is right there" → [old_string must not include Read's line-number prefix](pitfalls/tool-behaviors/edit-old-string-must-not-include-read-line-number-prefix.md)
- "`ask_user_input_v0` schema validation error / too many questions / too many options" → [ask_user_input_v0 3-question, 4-option ceiling](pitfalls/tool-constraints/ask-user-input-v0-question-and-option-limits.md)
- "`references/foo.md` not found / doesn't load from my skill dir" → [references/ path resolution](pitfalls/skill-structure/references-directory-path-resolution.md)
- "I edited my SKILL.md but Claude Code still uses the old instructions" → [Edits to a loaded SKILL.md don't hot-reload mid-session](pitfalls/skill-structure/skill-md-edit-no-hot-reload.md)
- "`pip install` fails on Claude.ai with externally-managed-environment" → [Claude.ai pip install break-system-packages](pitfalls/environment/claude-ai-pip-install-break-system-packages.md)
- "Files my skill wrote disappeared between turns on Claude.ai" → [Claude.ai sandbox filesystem resets between turns](pitfalls/environment/claude-ai-filesystem-resets-between-turns.md)
- "`curl` / network request blocked on Claude.ai" → [Claude.ai HTTPS egress allowlist](pitfalls/environment/claude-ai-network-egress-allowlist.md)
- "Bash `timeout` rejected / capped on Claude Code" → [Claude Code Bash 600s timeout ceiling](pitfalls/tool-constraints/code-bash-600-second-ceiling.md)
- "Bash `timeout_ms` capped on Claude Desktop" → [Claude Desktop bash 45s ceiling](pitfalls/tool-constraints/desktop-bash-45-second-ceiling.md)
- "Shell variable lost between bash calls on Claude Desktop" → [Desktop bash no state carryover](pitfalls/tool-behaviors/desktop-bash-no-state-carryover.md)
- "`cd` / exported variable doesn't carry to the next bash call on Claude Code" → [Code bash no cwd or state carryover](pitfalls/tool-behaviors/code-bash-no-cwd-or-state-carryover.md)
- "Claude Code refused my `git commit --amend` / `--no-verify`" → [Code Bash embedded git policy](pitfalls/tool-behaviors/code-bash-embedded-git-policy.md)
- "MCP tool name format mismatch across platforms" → [MCP tool name format diverges](pitfalls/cross-platform/mcp-tool-name-format-diverges.md)
- "`AskUserQuestion` vs `ask_user_input_v0` — which one?" → [AskUserQuestion vs ask_user_input_v0](pitfalls/cross-platform/askuserquestion-vs-ask-user-input-v0.md)
- "`Write` failed 'File has not been read yet' on an existing file" → [Write requires a prior Read for existing files](pitfalls/tool-behaviors/write-requires-prior-read-for-existing-files.md)
- "`Read` failed with `EISDIR` / can't list a directory on Claude Code" → [view lists directories; Read cannot](pitfalls/cross-platform/view-vs-read-directory-listing.md)
- "`Read('references/foo.md')` resolves to my project dir, not the skill dir" → [Read resolves against cwd, not the skill directory](pitfalls/tool-behaviors/code-read-resolves-against-cwd-not-skill-dir.md)
- "I set the 'Base directory for this skill' but relative paths still don't resolve" → [Base-directory header is informational only](pitfalls/skill-structure/code-skill-base-directory-header-is-informational.md)
- "`view` rejected my relative path / bare filename on Claude.ai" → [view requires absolute paths](pitfalls/tool-behaviors/claude-ai-view-requires-absolute-paths.md)
- "My new skill isn't showing up without restarting Claude Code" → [New skill directories hot-load on Claude Code](pitfalls/skill-structure/code-skill-directory-hot-load-works.md)
- "'use the Write tool' instruction breaks my skill on another platform" → [Hardcoded tool names in SKILL.md are non-portable](pitfalls/skill-structure/tool-names-as-instructions-non-portable.md)
- "MCP tool call fails with `InputValidationError` / schema not loaded on Code/Desktop" → [MCP tool schemas are deferred on Code and Desktop](pitfalls/cross-platform/mcp-tools-deferred-on-code-and-desktop.md)
- "`search_mcp_registry` / `suggest_connectors` missing on Claude Code" → [MCP discovery layer absent on Code](pitfalls/cross-platform/mcp-discovery-layer-absent-on-code.md)
- "`Edit` `replace_all` not working / Claude.ai needs a unique match" → [Edit.replace_all divergence](pitfalls/cross-platform/edit-replace-all-divergence.md)
- "Same bash command behaves differently across Claude.ai / Code / Desktop" → [The bash tool has three different shapes](pitfalls/cross-platform/bash-tool-three-shapes.md)
- "My SVG/HTML shows as raw markup instead of rendering on Claude Code" → [Inline visualization absent on Code](pitfalls/cross-platform/visualization-absent-on-code.md)
- "Searching past chats works differently / isn't available across platforms" → [Past-chat search has three shapes](pitfalls/cross-platform/past-chat-search-three-shapes.md)
- "`conversation_search` returns unrelated results / keyword-only matching" → [conversation_search is keyword-only](pitfalls/tool-behaviors/conversation-search-keyword-only-matching.md)
- "Telling the model 'don't assume which tool to use' isn't working" → [Unenforceable without an in-skill picker](pitfalls/cross-platform/dont-assume-instructions-unenforceable-without-picker.md)
- "Can't write to `/mnt/user-data/uploads/` on Claude.ai (read-only)" → [uploads/ is read-only; use outputs/](pitfalls/environment/claude-ai-mnt-user-data-uploads-readonly.md)
- "Claude Desktop's bash can't see my home dir / host files / installed binaries" → [Desktop bash is sandboxed, not the host](pitfalls/environment/desktop-bash-sandboxed-not-host.md)
- "`image_search` rejected my `max_results` value" → [image_search.max_results bounded to 3–5](pitfalls/tool-constraints/image-search-result-count-bounds.md)
- "`recent_chats` rejected my `n` value (too large)" → [recent_chats.n caps at 20](pitfalls/tool-constraints/recent-chats-max-n.md)

## Categories

- [`pitfalls/tool-constraints/`](./pitfalls/tool-constraints/) — hidden limits on a single tool (schema-enforced caps, undocumented ceilings)
- [`pitfalls/tool-behaviors/`](./pitfalls/tool-behaviors/) — undocumented behaviors (path resolution, prerequisite calls, side effects)
- [`pitfalls/cross-platform/`](./pitfalls/cross-platform/) — divergences across Claude.ai, Code, Desktop (same purpose, different shape)
- [`pitfalls/environment/`](./pitfalls/environment/) — sandbox, filesystem, network constraints
- [`pitfalls/skill-structure/`](./pitfalls/skill-structure/) — SKILL.md authoring traps (file paths, references, hot-reload)

## Verification tiers

Each pitfall is labeled with one of three tiers. The repo's credibility comes from honest labeling, not from claiming more than we tested.

- **`verified`** — reproduced empirically (Linh or a Claude Code session); a reproduction is included
- **`schema-only`** — verified by reading the tool's JSON schema or description; not triggered empirically
- **`stub`** — symptom and cause are documented but no reproduction yet; contributions welcome

## Relationship to skill-creator

Anthropic ships an excellent skill called [`skill-creator`](https://github.com/anthropics/skills) that teaches the authoring loop — how to write the frontmatter, structure progressive disclosure, run evals, iterate. This repo doesn't duplicate that work. If you're learning how to write a skill, read skill-creator first. If you've already written one and need to know whether it'll work on the platforms your users run, the catalog here picks up where skill-creator stops.

## Contributing

Every new pitfall declares a verification tier and platform applicability. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

CC BY 4.0 — see [LICENSE](LICENSE).
