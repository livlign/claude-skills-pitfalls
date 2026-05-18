# `Write` requires a prior `Read` for existing files

> Claude Code's `Write` refuses to overwrite an existing file unless `Read` was called on that path earlier in the conversation — even when the overwrite is intentional.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
- **Verification tier:** schema-only
- **Severity:** Hard error

## Symptom

A SKILL.md that says "create or replace this file" without reading first errors on Code/Desktop when the target already exists. New files are fine.

## Cause

`Write`'s description on both Code and Desktop requires a prior `Read` of the target file before overwriting it.

## Fix

For portable skills, instruct Claude to read the existing file before writing. The extra `Read` is harmless on Claude.ai (where `create_file` refuses overwrite regardless).

## Notes

Related: [`../cross-platform/write-vs-create-file-overwrite-semantics.md`](../cross-platform/write-vs-create-file-overwrite-semantics.md) and the parallel `Edit` rule in [`edit-requires-prior-read-same-conversation.md`](./edit-requires-prior-read-same-conversation.md).
