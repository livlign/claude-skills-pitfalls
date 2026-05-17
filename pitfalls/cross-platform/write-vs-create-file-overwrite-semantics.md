# `Write` overwrites silently; `create_file` refuses to overwrite

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude.ai web 2026-05-17, Claude Code 2026-05-17
- **Verification tier:** verified
- **Severity:** Data loss risk

## Symptom

A skill instructed to "create file X with content Y" succeeds on one platform and errors on another, depending on whether X already exists.

## Cause

Code's `Write` and Desktop's `Write` silently overwrite existing files. Claude.ai's `create_file` refuses with `File already exists`. Same instruction, opposite behavior.

## Reproduction

**Claude.ai (2026-05-17):**
- First call: `create_file("/tmp/x.txt", "hello")` → success
- Second call: `create_file("/tmp/x.txt", "overwritten")` → `File already exists: /tmp/x.txt`

**Claude Code:** `Write("/tmp/x.txt", "hello")` then `Write("/tmp/x.txt", "different")` — silently overwrites; original data lost.

## Fix

Don't hardcode tool names. Describe intent: "Replace the contents of X with Y. If X exists, make the user aware before overwriting." The model on each platform uses the available primitives appropriately. For explicit safety, instruct: "If X exists, read it first to confirm, then proceed."

## Notes

Most dangerous pitfall in this catalog. A Claude.ai author testing locally sees the "won't overwrite" guard and assumes universality; the same skill on Code silently destroys user data. The reverse direction (Code → Claude.ai) errors loudly, which is the safer failure mode.

Related: [`../tool-behaviors/write-requires-prior-read-for-existing-files.md`](../tool-behaviors/write-requires-prior-read-for-existing-files.md).
