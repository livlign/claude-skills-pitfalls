# `view` lists directories; `Read` cannot

> On Claude.ai the `view` tool can list a directory's contents; on Claude Code and Desktop the `Read` tool errors on directory paths.

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ (lists dirs) | Claude Code ❌ | Claude Desktop ❌
- **Verified on:** Claude.ai 2026-05-17, Claude Code 2026-05-17; Code error re-confirmed on Opus 4.8, 2026-06-14
- **Verification tier:** verified
- **Severity:** Functional gap

## Symptom

A SKILL.md that points Claude at a directory expecting a listing succeeds on Claude.ai and errors on Code/Desktop.

## Cause

Claude.ai's `view` lists directories up to two levels deep. Code's `Read` and Desktop's `Read` cannot list directories at all — they error and direct the user to use Bash `ls`.

## Reproduction

On Claude Code (Opus 4.8, 2026-06-14), calling `Read` on a directory path:

```
Read(file_path="/tmp/probe")
→ EISDIR: illegal operation on a directory, read '/tmp/probe'
```

If you searched for `EISDIR: illegal operation on a directory` after a skill pointed `Read` at a folder, this is the cause: use Bash `ls`/`find` instead.

## Fix

For portable skills, use `bash_tool` / `Bash` with `ls` (or `find`) to list directories. Don't rely on view-style directory introspection.

## Notes

Related: [`../tool-behaviors/claude-ai-view-requires-absolute-paths.md`](../tool-behaviors/claude-ai-view-requires-absolute-paths.md).
