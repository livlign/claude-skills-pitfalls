# `recent_chats.n` caps at 20

**Category:** tool-constraints
**Applies to:** Claude.ai ✅ | Claude Code ❌ (tool doesn't exist) | Claude Desktop ❌ (tool doesn't exist)
**Verified on:** Claude.ai web, 2026-05-17
**Verification tier:** verified
**Severity:** Hard error

## Symptom

A skill that requests `n > 20` from `recent_chats` fails with a validation error.

## Cause

Schema caps `n` at 20.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `recent_chats(n=25)` → `Input should be less than or equal to 20`.

## Fix

To fetch more than 20 chats, paginate with the `before` cursor across multiple calls. The system-prompt guidance advises stopping after ~5 calls.

## Notes

For the broader past-chat-search divergence across platforms, see [`../cross-platform/past-chat-search-three-shapes.md`](../cross-platform/past-chat-search-three-shapes.md).
