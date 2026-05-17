# Skills fail silently when their named tool doesn't exist

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Silent fallback

## Symptom

A SKILL.md authored against one platform's tool names runs on another platform and produces plausible-looking output — but the named tool was never called. The author doesn't see an error; tests that only check for "did the conversation succeed?" pass.

## Cause

When a SKILL.md instructs Claude to call a tool that doesn't exist on the running platform, Claude does NOT error. Two observed shapes:

- On Claude Code, the model falls back to prose. Verified 2026-05-17: 6 of 7 Claude.ai-only tools tested produced no error; the model substituted natural-language output.
- On Claude.ai, the model silently substitutes a similar-named tool with different parameters, discarding fields the analogue doesn't support.

## Reproduction

Reproduced 2026-05-17 on Claude Code: SKILL.md instructing `image_search(...)`, `visualize:show_widget(...)`, and other Claude.ai-only tools. Model produced prose answers; no tool call errors surfaced.

## Fix

CI/smoke tests for skills must assert that the *expected tool was actually called*, not just that the conversation produced plausible output. Test on every target platform, not just one.

## Notes

This is the meta-pitfall behind most of the cross-platform catalog. Related: [`mcp-tool-name-format-diverges.md`](./mcp-tool-name-format-diverges.md), [`../skill-structure/tool-names-as-instructions-non-portable.md`](../skill-structure/tool-names-as-instructions-non-portable.md).
