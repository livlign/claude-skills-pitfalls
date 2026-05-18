# `Edit` requires a prior `Read` in the same conversation

> Claude Code's `Edit` errors with 'you must use Read first' unless `Read` was called on the same file earlier in the same conversation — even if your skill just wrote it.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
- **Verification tier:** schema-only
- **Severity:** Hard error

## Symptom

A SKILL.md that jumps straight to `Edit` (e.g., to apply a patch the skill computed in advance) errors on Code and Desktop.

## Cause

Both Code's and Desktop's `Edit` tool descriptions state: "You must use your Read tool at least once in the conversation before editing." The check happens at call time and errors out. Claude.ai's `str_replace` has no such requirement.

## Fix

For portable skills, instruct Claude to read the file before editing. The extra `Read` is harmless on Claude.ai but mandatory on Code/Desktop.

## Notes

Same pattern applies to `Write` on existing files — see [`write-requires-prior-read-for-existing-files.md`](./write-requires-prior-read-for-existing-files.md).
