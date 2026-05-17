# `conversation_search` is keyword-only; meta-words poison results

**Category:** tool-behaviors
**Applies to:** Claude.ai ✅ | Claude Code ❌ | Claude Desktop ❓
**Verified on:** Claude.ai web, 2026-05-17
**Verification tier:** verified
**Severity:** Silent semantic failure

## Symptom

A skill that searches past chats for "what we discussed yesterday" returns plausible-looking but wrong chats — often from weeks or months prior.

## Cause

`conversation_search` matches keywords literally — including meta-words like "discussed" or "yesterday" that describe the act of having a conversation rather than its content. Any past chat containing those literal tokens scores well.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: query `"discussed yesterday"` returned chats from weeks and months prior, none of which were from yesterday.

## Fix

Queries must contain *content nouns* from the original conversation, not words that describe the meta. "Discussed" and "yesterday" are meta; "Atlassian", "Lambda OutOfMemory", "Lighthouse ProductHub" are content. For time-windowed retrieval, use `recent_chats` instead.

## Notes

For the cross-platform shape of past-chat search, see [`../cross-platform/past-chat-search-three-shapes.md`](../cross-platform/past-chat-search-three-shapes.md).
