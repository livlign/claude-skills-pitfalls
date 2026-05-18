# MCP discovery (`search_mcp_registry`, `suggest_connectors`) is absent on Claude Code

> `search_mcp_registry` and `suggest_connectors` exist on Claude.ai but not on Claude Code; skills that rely on runtime MCP discovery silently misbehave there.

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ | Claude Code ❌ | Claude Desktop ✅ (deferred)
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Feature gap

## Symptom

A skill that relies on `search_mcp_registry` or `suggest_connectors` to route the user to a connector silently no-ops on Claude Code.

## Cause

Claude Code has no MCP discovery layer. Those tools don't exist there. Discovery happens implicitly: Claude reads the startup MCP-server list and infers what's available. Skills that depend on the discovery flow for routing only work on Claude.ai (with an opt-in gate) and Desktop (deferred).

## Fix

For portable skills, don't expect the platform to handle connector picking. Use the platform's elicitation tool (`AskUserQuestion` / `ask_user_input_v0`) to ask the user explicitly inside the skill body.

## Notes

Related: [`dont-assume-instructions-unenforceable-without-picker.md`](./dont-assume-instructions-unenforceable-without-picker.md).
