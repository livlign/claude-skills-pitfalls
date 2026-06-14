# `Write` requires a prior `Read` for existing files

> Claude Code's `Write` refuses to overwrite an existing file unless `Read` was called on that path earlier in the conversation — even when the overwrite is intentional.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that says "create or replace this file" without reading first errors on Code/Desktop when the target already exists. New files are fine.

## Cause

`Write`'s description on both Code and Desktop requires a prior `Read` of the target file before overwriting it.

## Reproduction

An existing file is created out-of-band (so it was never read via the `Read` tool this conversation), then `Write` targets it:

```
$ printf 'original contents\n' > /tmp/repro-existing-file.txt

Write(file_path="/tmp/repro-existing-file.txt", content="overwritten contents\n")
→ File has not been read yet. Read it first before writing to it.
```

Same gate and same verbatim error as `Edit`. A brand-new path (no existing file) writes without complaint; the check fires only when the target already exists.

## Fix

For portable skills, instruct Claude to read the existing file before writing. The extra `Read` is harmless on Claude.ai (where `create_file` refuses overwrite regardless).

## Notes

Related: [`../cross-platform/write-vs-create-file-overwrite-semantics.md`](../cross-platform/write-vs-create-file-overwrite-semantics.md) and the parallel `Edit` rule in [`edit-requires-prior-read-same-conversation.md`](./edit-requires-prior-read-same-conversation.md).
