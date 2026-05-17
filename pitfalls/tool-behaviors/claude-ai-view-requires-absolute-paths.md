# Claude.ai's `view` rejects relative paths and bare filenames

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ✅ | Claude Code ❌ | Claude Desktop ❌
- **Verified on:** Claude.ai web, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that tells Claude.ai to view a relatively-named file errors. No silent resolution attempt — the tool refuses outright.

## Cause

`view`'s description requires an absolute path and includes the realpath hint verbatim in its error.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `view("references/foo.md")` → `references/foo.md is not an absolute path. Run realpath references/foo.md to get the absolute path, then view that.`

## Fix

Always pass absolute paths to `view`. If a SKILL.md uses a relative path, instruct Claude to resolve it first via `bash_tool` (`realpath` or `readlink -f`).

## Notes

See also [`code-read-resolves-against-cwd-not-skill-dir.md`](./code-read-resolves-against-cwd-not-skill-dir.md) for the Code-side analogue, and [`../skill-structure/references-directory-path-resolution.md`](../skill-structure/references-directory-path-resolution.md) for the full skill-structure implication.
