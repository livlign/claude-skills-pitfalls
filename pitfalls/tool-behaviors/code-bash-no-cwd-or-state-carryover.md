# Claude Code's `Bash` does not persist cwd or shell state between calls

> On Claude Code, each `Bash` call effectively starts in the project working directory with a fresh shell — a `cd` in one call, and exported variables, do not carry over to the next. The harness resets cwd back to the project directory after every call.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ (cwd persists) | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Behavioral divergence

## Symptom

A SKILL.md that runs `cd somewhere` (or `export VAR=…`) in one `Bash` call and a follow-up command in another finds itself back in the project directory with the variable unset.

## Cause

After each `Bash` call, Claude Code resets the working directory to the project root — it even emits a `Shell cwd was reset to <project dir>` notice. Shell state (environment variables, functions) is likewise not carried between calls. This contradicts the once-common assumption (including earlier versions of this catalog) that Code's `Bash` persists cwd across calls; as of Opus 4.8 it does not.

## Reproduction

```
# Call 1 — cd into /tmp
$ cd /tmp; pwd
/tmp
Shell cwd was reset to /Users/linh/Documents/prjs/claude-skills-pitfalls

# Call 2 — separate call, back in the project dir
$ pwd
/Users/linh/Documents/prjs/claude-skills-pitfalls
```

Environment variables behave the same way:

```
# Call 1
$ export PROBE_VAR=hello; echo "$PROBE_VAR"
hello

# Call 2 — separate call
$ echo "'${PROBE_VAR:-<empty>}'"
'<empty>'
```

## Fix

Combine related shell operations into a single `Bash` call (chained with `&&`), or pass absolute paths to every command. Don't rely on `cd` or `export` persisting across calls. This is the same defensive pattern that portable skills already need for Claude Desktop.

## Notes

The Code environment hint says "Working directory persists between calls" — in practice that means each call *returns to* the project directory, not that your `cd` is remembered. Claude.ai's `bash_tool` does persist cwd; the parallel Desktop behavior is documented in [`desktop-bash-no-state-carryover.md`](./desktop-bash-no-state-carryover.md). Because both Code and Desktop reset between calls, a skill that relies on carryover misbehaves on two of three platforms.
