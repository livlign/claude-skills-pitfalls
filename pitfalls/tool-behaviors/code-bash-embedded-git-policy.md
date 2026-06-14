# Claude Code's `Bash` embeds a strict git policy in its tool description

> Claude Code's `Bash` tool description embeds a git safety policy — refusing `--amend`, `--no-verify`, `reset --hard`, force-push, etc. without explicit user permission.

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ❌
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Workflow constraint

## Symptom

A skill that templates raw git commands on Code (e.g., to amend, force-push, or reset) hits unexpected refusals, or templates a `Co-Authored-By` trailer that no longer matches the model the harness expects.

## Cause

Claude Code's environment embeds a git policy in its instructions. **This policy is version-dependent and drifts between releases — a skill that hardcodes its specifics will rot.** As observed on Opus 4.8 (2026-06-14), the current policy reads:

- Interactive flags (`-i`, e.g. `git rebase -i`, `git add -i`) are not supported.
- Use the `gh` CLI for GitHub operations (PRs, issues, API).
- Commit or push only when the user asks. If on the default branch, branch first.
- Git commit messages end with a `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` trailer.
- Hard-to-reverse / outward-facing actions require confirmation first.

This differs from what earlier versions of this entry documented (which named an explicit `--no-verify` / amend / `reset --hard` / force-push prohibition list and a `Claude Opus 4.7` trailer). The exact prohibitions and the trailer string both changed — confirming the policy is not stable across model versions.

## Fix

Work *with* the policy rather than against it, and **never hardcode the trailer string or the exact prohibition list** — both move between versions. Describe the *intent* (commit, push) and let each platform's Claude fill in the current trailer and mechanics. For amend or force-push workflows, surface them to the user for explicit permission.

## Notes

This policy is unique to Code — it does not apply to Claude.ai's `bash_tool` or Desktop's `mcp__workspace__bash`. The reproduction here is observation of the live environment's git instructions rather than a triggered refusal (running destructive git against a real repo to force a refusal is not worth the risk); the verified facts are the policy's presence and its current content on Opus 4.8.
