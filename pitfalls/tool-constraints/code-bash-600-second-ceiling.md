# Claude Code's `Bash` documents a 600000ms (10-minute) `timeout` max — but does not hard-reject above it

> Claude Code's `Bash` tool description states `timeout` maxes at 600000ms (10 minutes). Empirically, passing a higher value is **not** rejected — the call is silently accepted (clamped or ignored), so the documented ceiling is not a hard gate.

- **Category:** tool-constraints
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ❌
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Silent clamp

## Symptom

A SKILL.md that hardcodes a long bash timeout on Claude Code expects either a 10-minute cap or a rejection above it. Neither assumption is safe to rely on: the documented max is 600000ms, but values above it are accepted without error rather than rejected.

## Cause

`Bash`'s tool description states the `timeout` parameter maxes at 600000ms (10 minutes). The earlier inference here — that values above the ceiling are rejected by the schema — was incorrect. In practice the call succeeds; the over-limit value is silently clamped or ignored rather than producing a validation error. The effective wall-clock ceiling for a foreground command is still bounded, so genuinely long work must be backgrounded.

## Reproduction

Passing `timeout: 700000` (above the documented 600000 max):

```
Bash(command="echo 'this should never run if the schema rejects the call'", timeout=700000)
→ this should never run if the schema rejects the call
```

The command runs normally — no `InputValidationError`, no rejection. (The reproduction does not distinguish silent clamping from silently honoring the value; it only establishes that over-limit timeouts are **not** rejected.)

## Fix

Don't rely on the timeout value to bound long work, and don't expect an over-limit timeout to surface an error. For anything that may exceed ~10 minutes, use `run_in_background: true` and poll via the appropriate harness mechanism, or split the command.

## Notes

Claude.ai's `bash_tool` doesn't expose a timeout parameter; Desktop's bash caps at 45s — see [`desktop-bash-45-second-ceiling.md`](./desktop-bash-45-second-ceiling.md). A skill that hardcodes a long timeout works only on Code, and even there should not assume the documented max is enforced as a hard gate.
