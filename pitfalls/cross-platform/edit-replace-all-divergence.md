# `Edit.replace_all` exists on Code/Desktop; Claude.ai's `str_replace` has no equivalent

> Claude Code and Desktop's `Edit` accepts a `replace_all` flag; Claude.ai's `str_replace_based_edit_tool` has no equivalent and requires unique matches.

- **Category:** cross-platform
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ✅
- **Verification tier:** schema-only
- **Severity:** Feature gap

## Symptom

A SKILL.md that renames an identifier across a file works in one call on Code/Desktop (`replace_all: true`) but fails or partially completes on Claude.ai.

## Cause

Code/Desktop `Edit` supports `replace_all: true`. Claude.ai's `str_replace` has no such field — `old_str` must be unique in the file or the call fails.

## Fix

For portable rename-style operations, either:

- Chain multiple unique-string `str_replace` calls (Claude.ai path), or
- Use `Edit` with `replace_all: true` (Code/Desktop path)

Don't write a SKILL.md that assumes either path universally. Describe the rename intent and let each platform's Claude pick the mechanism.

## Notes

Related: [`../tool-behaviors/edit-requires-prior-read-same-conversation.md`](../tool-behaviors/edit-requires-prior-read-same-conversation.md).
