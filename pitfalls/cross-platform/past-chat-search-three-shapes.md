# Past-chat search has a different shape on each platform

> Searching past conversations uses `conversation_search` on Claude.ai, a different shape on Desktop, and isn't available on Claude Code — same intent, three implementations.

- **Category:** cross-platform
- **Applies to:** Claude.ai ✅ (keyword + time) | Claude Code ❌ (file-based memory) | Claude Desktop ✅ (session list, no keyword)
- **Verified on:** 2026-05-17
- **Verification tier:** verified
- **Severity:** Feature gap

## Symptom

A SKILL.md that says "find what we discussed about X last week" succeeds, fails, or produces wildly different results depending on the platform.

## Cause

Three different mechanisms:

- **Claude.ai:** `conversation_search` (keyword) + `recent_chats` (time-windowed)
- **Claude Code:** no chat search — uses file-based memory (`MEMORY.md` + `memory/*.md`)
- **Claude Desktop:** `mcp__session_info__list_sessions` + `read_transcript` (deferred, no keyword search)

## Fix

If a skill needs past-chat search, target one platform explicitly or describe the intent generically and accept divergent behavior. Don't write portable past-chat-search skills.

## Notes

Related: [`../tool-behaviors/conversation-search-keyword-only-matching.md`](../tool-behaviors/conversation-search-keyword-only-matching.md), [`../tool-constraints/recent-chats-max-n.md`](../tool-constraints/recent-chats-max-n.md).
