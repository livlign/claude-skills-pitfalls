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

Two entry points:

- **By tool / failure type:** browse [`pitfalls/`](./pitfalls/) by category
- **By platform:** check the [compatibility matrix](matrix/tool-inventory.md) to see if your skill's tools exist on the platform you're targeting

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
