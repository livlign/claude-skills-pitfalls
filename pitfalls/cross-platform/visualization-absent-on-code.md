# Inline SVG/HTML visualization is absent on Claude Code

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ | Claude Code ❌ | Claude Desktop ✅
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Feature gap

## Symptom

A SKILL.md that builds diagrams or interactive widgets via `visualize:show_widget` produces nothing visible on Claude Code. The model likely falls back to ASCII or skips silently.

## Cause

Inline SVG/HTML widget rendering (`visualize:show_widget` family) exists on Claude.ai and Desktop. Claude Code renders CommonMark markdown only — no rendering surface for inline visuals.

## Fix

For portable visual output, fall back to markdown tables, ASCII diagrams, or generate SVG/HTML to a file (`Write` / `create_file`) and surface it via `present_files` where present.

## Notes

Related: [`silent-fallback-when-tool-missing.md`](./silent-fallback-when-tool-missing.md) — the visualization tools are a frequent victim of the silent-fallback pattern.
