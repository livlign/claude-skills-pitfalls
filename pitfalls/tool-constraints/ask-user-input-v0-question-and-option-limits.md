# `ask_user_input_v0` enforces a 3-question, 4-option ceiling

> `ask_user_input_v0` on Claude.ai enforces a schema-level ceiling of 3 questions and 4 options per question; exceeding either limit fails with a validation error.

- **Category:** tool-constraints
- **Applies to:** Claude.ai ✅ | Claude Code ❌ (tool doesn't exist) | Claude Desktop ❌ (tool doesn't exist)
- **Verified on:** Claude.ai web, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A skill written for Claude.ai that calls `ask_user_input_v0` with more than 3 questions, or with more than 4 options per question, fails with a schema validation error. The constraint isn't documented in user-facing skill-authoring guidance.

## Cause

The tool's schema declares `maxItems: 3` on the questions array and `maxItems: 4` on the options array. The tool description mentions these limits in prose ("one question where possible — three is a ceiling, not a target", "2-4 short, mutually exclusive options") but they read as guidance rather than hard limits.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `ask_user_input_v0` with 4 questions → schema validation error.

## Fix

Cap questions at 3, options at 4. If elicitation needs more, chain across turns or use `multi_select` to combine. A portable skill that also targets Code/Desktop's `AskUserQuestion` (which caps at 4 questions) must conform to the stricter limit of 3.

## Notes

Related Claude.ai hard ceilings: see [`image-search-result-count-bounds.md`](./image-search-result-count-bounds.md) and [`recent-chats-max-n.md`](./recent-chats-max-n.md). For the cross-platform tool divergence, see [`../cross-platform/askuserquestion-vs-ask-user-input-v0.md`](../cross-platform/askuserquestion-vs-ask-user-input-v0.md).
