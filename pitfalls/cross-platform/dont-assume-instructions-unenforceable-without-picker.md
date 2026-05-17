# "Don't assume which tool to use" is unenforceable without an in-skill picker

**Category:** cross-platform
**Applies to:** Claude.ai ❓ | Claude Code ✅ | Claude Desktop ❓
**Verified on:** Claude Code, 2026-05-17
**Verification tier:** verified
**Severity:** Silent UX divergence

## Symptom

A SKILL.md that instructs "do not assume which tool to use; let the user pick" runs on Code with multiple connected MCP servers, and Claude silently picks one — overriding the SKILL.md instruction.

## Cause

There is no platform-level picker UI on Code. With multiple candidates available, the model infers from inventory and proceeds. Verified 2026-05-17: with several MCP servers connected, Claude picked Atlassian without surfacing the choice to the user despite the SKILL.md saying not to assume.

## Fix

If user choice matters to the skill, the skill body itself must invoke an elicitation tool (`AskUserQuestion` / `ask_user_input_v0`) with the candidate options. Don't delegate the choice to "the platform."

## Notes

Related: [`mcp-discovery-layer-absent-on-code.md`](./mcp-discovery-layer-absent-on-code.md).
