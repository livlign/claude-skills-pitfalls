# `Edit` requires a prior `Read` in the same conversation

> Claude Code's `Edit` errors unless `Read` was called on the same file earlier in the same conversation — even if your skill just wrote it.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that jumps straight to `Edit` (e.g., to apply a patch the skill computed in advance) errors on Code and Desktop.

## Cause

Both Code's and Desktop's `Edit` tool descriptions state that you must `Read` the file in the conversation before editing. The check happens at call time and errors out. Claude.ai's `str_replace` has no such requirement.

## Reproduction

In a fresh Claude Code conversation where `LICENSE` has not yet been read, calling `Edit` on it:

```
Edit(file_path="…/LICENSE", old_string="Creative Commons", new_string="Creative Commons!!")
→ File has not been read yet. Read it first before writing to it.
```

The verbatim error is `File has not been read yet. Read it first before writing to it.` (not the older "use Read first" phrasing). A `Read` of the same path earlier in the conversation clears the check.

## Fix

For portable skills, instruct Claude to read the file before editing. The extra `Read` is harmless on Claude.ai but mandatory on Code/Desktop.

## Notes

Same pattern applies to `Write` on existing files — see [`write-requires-prior-read-for-existing-files.md`](./write-requires-prior-read-for-existing-files.md).
