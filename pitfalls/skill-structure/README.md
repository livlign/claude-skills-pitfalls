# Skill structure pitfalls

SKILL.md authoring traps — file path resolution, references/ directory loading, hot-reload behavior, and instructions that don't survive across platforms.

Common questions this page answers:

- Why doesn't `references/foo.md` load relative to my SKILL.md?
- Does Claude Code reload my SKILL.md edits without restarting?
- Are new skill directories picked up automatically?
- Why do my instructions referencing tool names break on other platforms?

## Entries

- [The "Base directory for this skill" header on Code is informational only](./code-skill-base-directory-header-is-informational.md)
- [New skill directories hot-load on Claude Code (positive finding)](./code-skill-directory-hot-load-works.md)
- [`references/foo.md` doesn't resolve from the skill's directory](./references-directory-path-resolution.md)
- [SKILL.md edit hot-reload behavior is unverified](./skill-md-edit-hot-reload-unverified.md)
- [Hardcoded tool names in SKILL.md are non-portable](./tool-names-as-instructions-non-portable.md)

See also: [back to all categories](../)
