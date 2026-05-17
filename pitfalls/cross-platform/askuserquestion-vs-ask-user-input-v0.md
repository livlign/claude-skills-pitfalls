# `AskUserQuestion` and `ask_user_input_v0` are different tools

**Category:** cross-platform
**Applies to:** Claude.ai has `ask_user_input_v0` | Claude Code has `AskUserQuestion` | Claude Desktop has `AskUserQuestion`
**Verified on:** Claude.ai 2026-05-17, Claude Code 2026-05-17
**Verification tier:** verified
**Severity:** Silent substitution

## Symptom

A SKILL.md that names one of the two tools is silently substituted (or fails) on the other platform. Question shape, option shape, and supported variants differ enough that hardcoding either name is non-portable.

## Cause

Same purpose, different schemas. Differences:

- **Max questions:** 3 (Claude.ai `ask_user_input_v0`) vs 4 (Code/Desktop `AskUserQuestion`)
- **Question types:** Claude.ai has `single_select` / `multi_select` / `rank_priorities`; Code/Desktop has single and multi (via `multiSelect: true`), no `rank_priorities`
- **Options:** Claude.ai uses plain strings; Code/Desktop requires `{label, description}` objects with optional `preview`
- **"Other":** Claude.ai doesn't auto-add; Code/Desktop auto-adds (don't include manually)
- **Header field:** required (max 12 chars) on Code/Desktop; absent on Claude.ai
- **Recommendation convention:** Code/Desktop expect the first option marked "(Recommended)" when applicable

## Fix

Treat them as different tools. A portable skill must conform to the *stricter* constraints of both: 3 questions max, every option must include a `description`, header under 12 chars, no manual "Other" option.

## Notes

The schema-cap details for Claude.ai's variant live in [`../tool-constraints/ask-user-input-v0-question-and-option-limits.md`](../tool-constraints/ask-user-input-v0-question-and-option-limits.md).
