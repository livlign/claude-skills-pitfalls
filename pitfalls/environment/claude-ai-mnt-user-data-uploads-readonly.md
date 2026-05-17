# `/mnt/user-data/uploads/` is read-only on Claude.ai

**Category:** environment
**Applies to:** Claude.ai ✅ | Claude Code ❌ (path doesn't exist) | Claude Desktop ❌
**Verified on:** Claude.ai web, 2026-05-17
**Verification tier:** verified
**Severity:** Hard error

## Symptom

A SKILL.md that edits uploaded files in place on Claude.ai errors with a read-only filesystem error.

## Cause

`/mnt/user-data/uploads/` is mounted read-only. Skills cannot modify uploaded files in place.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `echo > /mnt/user-data/uploads/x.txt` → `Read-only file system`.

## Fix

Copy uploaded files to a writable location (`/home/claude/` in the Claude.ai sandbox) before modifying.

## Notes

This path doesn't exist on Code or Desktop, so the pitfall is Claude.ai-only — but a SKILL.md authored on Claude.ai and ported elsewhere will reference a path that no longer resolves.
