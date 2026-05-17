# Claude Desktop's bash runs in a sandbox, not the user's real filesystem

- **Category:** environment
- **Applies to:** Claude.ai ✅ (separate sandbox) | Claude Code ❌ (host filesystem) | Claude Desktop ✅
- **Verification tier:** schema-only
- **Severity:** Functional gap

## Symptom

A SKILL.md that references `~/Documents/...` or other host paths works on Claude Code (real home dir) and fails on Claude Desktop (no real home; the workspace is a fresh sandbox).

## Cause

Desktop's `mcp__workspace__bash` runs in an isolated sandbox at `/sessions/<id>/mnt/`, not the user's real filesystem. Code's `Bash` runs on the host.

## Fix

Skills assuming "the user's real filesystem" only work on Code. For portable file workflows on Desktop, expect mounted folders under `/sessions/.../mnt/` and use `request_cowork_directory` to discover paths.

## Notes

Related: [`../cross-platform/bash-tool-three-shapes.md`](../cross-platform/bash-tool-three-shapes.md), [`../tool-behaviors/desktop-bash-no-state-carryover.md`](../tool-behaviors/desktop-bash-no-state-carryover.md).
