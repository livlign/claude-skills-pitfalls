# The bash tool has three structurally different shapes across platforms

> Claude.ai, Claude Code, and Claude Desktop each expose a structurally different bash tool — different parameter names, different timeouts, different state semantics.

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ (`bash_tool`) | Claude Code ✅ (`Bash`) | Claude Desktop ✅ (`mcp__workspace__bash`)
- **Verified on:** schema-diff comparison, 2026-05-17
- **Verification tier:** verified
- **Severity:** Behavioral divergence

## Symptom

A skill that runs shell commands behaves differently on each platform: different filesystem, different timeout ceiling, different policy guards, different state-carryover semantics.

## Cause

Three different tools that look interchangeable from a SKILL.md perspective:

- **Claude.ai `bash_tool`:** sandboxed Linux, `description` required, no timeout parameter, allowlisted network egress
- **Claude Code `Bash`:** host filesystem (the user's real machine), `description` required, `run_in_background` first-class, embedded git policy, 600s ceiling
- **Claude Desktop `mcp__workspace__bash`:** sandboxed Linux at `/sessions/.../mnt/`, no `description`, no backgrounding, 45s ceiling, no state carryover

## Fix

Skills assuming "the user's real filesystem" only work on Code. Skills assuming a "fast sandboxed shell" only work on Desktop. Skills assuming Claude.ai's allowlisted network only work there. Don't write portable bash-heavy skills without per-platform branching, or constrain the skill to operations that work the same on all three.

## Notes

Related: [`../tool-constraints/desktop-bash-45-second-ceiling.md`](../tool-constraints/desktop-bash-45-second-ceiling.md), [`../tool-constraints/code-bash-600-second-ceiling.md`](../tool-constraints/code-bash-600-second-ceiling.md), [`../tool-behaviors/code-bash-embedded-git-policy.md`](../tool-behaviors/code-bash-embedded-git-policy.md), [`../tool-behaviors/desktop-bash-no-state-carryover.md`](../tool-behaviors/desktop-bash-no-state-carryover.md), [`../environment/desktop-bash-sandboxed-not-host.md`](../environment/desktop-bash-sandboxed-not-host.md).
