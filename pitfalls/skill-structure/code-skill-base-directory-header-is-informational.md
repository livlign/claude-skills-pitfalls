# The "Base directory for this skill" header on Code is informational only

> The 'Base directory for this skill: <path>' line Claude Code injects above SKILL.md is informational only — tools do not resolve relative paths against it.

- **Category:** skill-structure
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ❓
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Misleading affordance

## Symptom

A SKILL.md author reads the "Base directory for this skill: ..." line that Claude Code injects when a skill triggers and reasonably concludes relative paths will resolve from there. They don't.

## Cause

The base-directory header is text in the turn — it does NOT change the process cwd and does NOT affect how `Read` resolves relative paths. Code's `Read` continues to resolve against the launch directory.

## Reproduction

Reproduced 2026-05-17 on Claude Code: skill triggered with the base-directory header visible; `Read("references/foo.md")` still resolved against the user's project directory, not the skill directory.

## Fix

Treat the base-directory header as a hint to the model, not a runtime affordance. SKILL.md must instruct Claude to construct absolute paths explicitly.

## Notes

The header is useful as a hint — it gives the model the string it needs to build an absolute path. But the skill author must instruct that construction. See [`references-directory-path-resolution.md`](./references-directory-path-resolution.md).
