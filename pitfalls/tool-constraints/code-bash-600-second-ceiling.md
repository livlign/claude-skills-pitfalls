# Claude Code's `Bash` caps `timeout` at 600000ms (10 minutes)

- **Category:** tool-constraints
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ❌
- **Verification tier:** schema-only
- **Severity:** Hard error

## Symptom

A SKILL.md that hardcodes a long bash timeout on Claude Code fails for anything over 10 minutes.

## Cause

`Bash`'s `timeout` parameter accepts up to 600000ms (10 minutes). Tasks longer than that need to be backgrounded (`run_in_background: true`) or split into smaller calls.

## Fix

For long-running work, use `run_in_background: true` and poll via the appropriate harness mechanism, or split the command.

## Notes

Claude.ai's `bash_tool` doesn't expose a timeout parameter; Desktop's bash caps at 45s — see [`desktop-bash-45-second-ceiling.md`](./desktop-bash-45-second-ceiling.md). A skill that hardcodes a long timeout works only on Code.
