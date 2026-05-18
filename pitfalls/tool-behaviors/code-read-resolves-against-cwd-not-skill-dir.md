# Claude Code's `Read` resolves relative paths against cwd, not the skill directory

> Claude Code's `Read` resolves relative paths against the current working directory, not the skill's own directory — `Read('references/foo.md')` from a skill rarely finds the file.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ (different failure mode — see notes) | Claude Code ✅ | Claude Desktop ❓
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Silent 404

## Symptom

A SKILL.md at `~/.claude/skills/<name>/` that tells Claude to `Read("references/foo.md")` errors with "File does not exist", and the hint message points at the user's project directory — not the skill directory.

## Cause

`Read` resolves relative paths against the process working directory (where Claude Code was launched), not the skill's own directory. The "Base directory for this skill: ..." header that Claude Code injects into the triggered turn is informational only — it does not `chdir`. See [`../skill-structure/code-skill-base-directory-header-is-informational.md`](../skill-structure/code-skill-base-directory-header-is-informational.md).

## Reproduction

Reproduced 2026-05-17 on Claude Code: `Read("references/relative.md")` from a skill triggered while cwd was a project dir → `File does not exist. Note: your current working directory is /Users/<user>/Documents/<project>.`

## Fix

SKILL.md must instruct Claude to construct an absolute path before reading sibling resources. See [`../skill-structure/references-directory-path-resolution.md`](../skill-structure/references-directory-path-resolution.md) for the pattern.

## Notes

Claude.ai's `view` doesn't even attempt resolution — it rejects the relative path outright. See [`claude-ai-view-requires-absolute-paths.md`](./claude-ai-view-requires-absolute-paths.md).
