# Claude Code's `Bash` embeds a strict git policy in its tool description

**Category:** tool-behaviors
**Applies to:** Claude.ai ❌ | Claude Code ✅ | Claude Desktop ❌
**Verification tier:** schema-only
**Severity:** Workflow constraint

## Symptom

A skill that templates raw git commands on Code (e.g., to amend, force-push, or reset) hits unexpected refusals or partial execution.

## Cause

Claude Code's `Bash` tool description embeds an extensive git policy: no `--no-verify`, no amend, no force-push without explicit permission, no `reset --hard`, no destructive operations. Commit messages must use HEREDOC with a `Co-Authored-By: Claude Opus 4.7 ...` trailer. Skills that ignore the policy run into these guards mid-execution.

## Fix

Work *with* the policy rather than against it. The HEREDOC commit format and `Co-Authored-By` trailer are non-negotiable on Code. For amend or force-push workflows, the skill must surface them to the user for explicit permission.

## Notes

This policy is unique to Code's `Bash` — it does not apply to Claude.ai's `bash_tool` or Desktop's `mcp__workspace__bash`. Skills that need to template git work portably should describe the *intent* (commit, push) and let each platform's Claude handle the mechanics.
