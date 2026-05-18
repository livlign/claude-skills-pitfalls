# Claude Desktop's bash caps `timeout_ms` at 45 seconds

> Claude Desktop's bash tool caps `timeout_ms` at 45000 — values above 45 seconds are silently clamped, and long-running commands die mid-execution.

- **Category:** tool-constraints
- **Applies to:** Claude.ai ❌ | Claude Code ❌ | Claude Desktop ✅
- **Verification tier:** schema-only
- **Severity:** Hard error

## Symptom

A skill that runs long-running shell work on Claude Desktop (npm install, build pipelines, anything slow) is killed mid-run.

## Cause

`mcp__workspace__bash`'s schema caps `timeout_ms` at 45000 (45 seconds). Not documented in user-facing material.

## Fix

For long-running tasks, break work into smaller bash calls or trigger it via a different mechanism. Don't assume Desktop's bash has the same patience as Code's `Bash` (600s) or Claude.ai's `bash_tool`.

## Notes

For the broader cross-platform bash divergence, see [`../cross-platform/bash-tool-three-shapes.md`](../cross-platform/bash-tool-three-shapes.md). Sibling ceiling on Code: [`code-bash-600-second-ceiling.md`](./code-bash-600-second-ceiling.md).
