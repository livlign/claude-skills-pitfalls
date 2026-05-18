# `image_search.max_results` is bounded to [3, 5]

> `image_search.max_results` is bounded to the range [3, 5]; values outside that window are rejected by the tool's schema validation.

- **Category:** tool-constraints
- **Applies to:** Claude.ai ✅ | Claude Code ❌ (tool doesn't exist) | Claude Desktop ❌ (tool doesn't exist)
- **Verified on:** Claude.ai web, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A skill that calls `image_search` with `max_results=2` or `max_results=10` fails with a Pydantic-style validation error.

## Cause

The schema requires `max_results >= 3` and `max_results <= 5`.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `image_search(..., max_results=2)` → `Input should be greater than or equal to 3`.

## Fix

Always pass 3, 4, or 5.

## Notes

Sibling Claude.ai ceilings: [`recent-chats-max-n.md`](./recent-chats-max-n.md), [`ask-user-input-v0-question-and-option-limits.md`](./ask-user-input-v0-question-and-option-limits.md).
