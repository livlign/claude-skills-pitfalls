# `references/foo.md` doesn't resolve from the skill's directory

**Category:** skill-structure
**Applies to:** Claude.ai ✅ | Claude Code ✅ | Claude Desktop ❓
**Verified on:** Claude.ai web 2026-05-17, Claude Code 2026-05-17
**Verification tier:** verified
**Severity:** Hard error (Claude.ai), Silent 404 (Code)

## Symptom

A SKILL.md that says "read `references/spec.md`" fails. On Claude.ai, the `view` tool rejects the relative path. On Claude Code, `Read` resolves the path against the process working directory and returns "File does not exist".

## Cause

Both platforms' file-reading tools require absolute paths. Neither resolves relative paths against the skill's own directory. There is no `$SKILL_DIR` variable. On Code, the "Base directory for this skill: ..." line injected into the triggered turn is informational only — see [`code-skill-base-directory-header-is-informational.md`](./code-skill-base-directory-header-is-informational.md).

## Reproduction

Skill at `~/.claude/skills/path-test/` with `references/relative.md` containing `RELATIVE_PATH_RESOLVED`. SKILL.md tells Claude to read `references/relative.md`. Reproduced 2026-05-17:

- Claude.ai: `view("references/relative.md")` → `references/relative.md is not an absolute path. Run realpath references/relative.md to get the absolute path, then view that.`
- Claude Code: `Read("references/relative.md")` → `File does not exist. Note: your current working directory is /Users/<user>/Documents/<project>.`
- Both: absolute paths work.

## Fix

SKILL.md must instruct Claude to construct an absolute path before reading sibling resources. Example:

> Determine the absolute path of this skill's directory (look for `SKILL.md` adjacent to `references/`). Read `<that path>/references/spec.md` using an absolute path.

## Notes

This pitfall contradicts the `references/` progressive-disclosure pattern recommended by Anthropic's `skill-creator`. The pattern is sound in principle but requires the model to construct absolute paths at runtime. Worth filing upstream — a `$SKILL_DIR` variable or skill-relative path support in `view` / `Read` would close the gap.

Related: [`../tool-behaviors/claude-ai-view-requires-absolute-paths.md`](../tool-behaviors/claude-ai-view-requires-absolute-paths.md), [`../tool-behaviors/code-read-resolves-against-cwd-not-skill-dir.md`](../tool-behaviors/code-read-resolves-against-cwd-not-skill-dir.md).
