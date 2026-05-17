# `Write` requires a prior `Read` for existing files

**Category:** tool-behaviors
**Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
**Verification tier:** schema-only
**Severity:** Hard error

## Symptom

A SKILL.md that says "create or replace this file" without reading first errors on Code/Desktop when the target already exists. New files are fine.

## Cause

`Write`'s description on both Code and Desktop requires a prior `Read` of the target file before overwriting it.

## Fix

For portable skills, instruct Claude to read the existing file before writing. The extra `Read` is harmless on Claude.ai (where `create_file` refuses overwrite regardless).

## Notes

Related: [`../cross-platform/write-vs-create-file-overwrite-semantics.md`](../cross-platform/write-vs-create-file-overwrite-semantics.md) and the parallel `Edit` rule in [`edit-requires-prior-read-same-conversation.md`](./edit-requires-prior-read-same-conversation.md).
