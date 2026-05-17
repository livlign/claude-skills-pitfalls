# MCP tool schemas are deferred on Claude Code and Desktop

- **Category:** cross-platform
- **Applies to:** Claude.ai ❌ (eager) | Claude Code ✅ (deferred) | Claude Desktop ✅ (deferred)
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that calls an MCP tool directly on Code/Desktop hits `InputValidationError` even though the tool is visible by name in the inventory.

## Cause

On Code and Desktop, MCP tool schemas are NOT loaded at session start. They appear by name only — schemas are "deferred." Calling one without first loading via `ToolSearch select:<name>` raises `InputValidationError`. Claude.ai loads them eagerly.

## Fix

SKILL.md targeting Code/Desktop should not assume an MCP tool is immediately callable. Either instruct Claude to `ToolSearch` first, or describe the capability and let Claude handle the loading.

## Notes

Related: [`mcp-tool-name-format-diverges.md`](./mcp-tool-name-format-diverges.md), [`mcp-discovery-layer-absent-on-code.md`](./mcp-discovery-layer-absent-on-code.md).
