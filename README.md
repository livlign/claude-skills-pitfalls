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
- "`ask_user_input_v0` schema validation error / too many questions / too many options" → [ask_user_input_v0 3-question, 4-option ceiling](pitfalls/tool-constraints/ask-user-input-v0-question-and-option-limits.md)
- "`references/foo.md` not found / doesn't load from my skill dir" → [references/ path resolution](pitfalls/skill-structure/references-directory-path-resolution.md)
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
