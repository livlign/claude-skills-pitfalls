# Claude Desktop's bash has no state carryover between calls

**Category:** tool-behaviors
**Applies to:** Claude.ai ❌ (cwd persists) | Claude Code ❌ (cwd persists) | Claude Desktop ✅
**Verification tier:** schema-only
**Severity:** Behavioral divergence

## Symptom

A SKILL.md that runs `cd somewhere` in one bash call and a follow-up command in another finds itself back at the default working directory.

## Cause

On Desktop, each `mcp__workspace__bash` call is independent — no cwd carryover, no shell state, no environment-variable carryover.

## Fix

Combine related shell operations into a single bash call, or pass absolute paths to every command. Don't rely on `cd` persisting across calls.

## Notes

Both Claude.ai's `bash_tool` and Code's `Bash` persist cwd across calls. Skills written and tested on those platforms will silently misbehave on Desktop.
