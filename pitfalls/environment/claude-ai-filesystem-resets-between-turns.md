# Claude.ai's sandbox filesystem resets between turns

> Claude.ai's sandbox filesystem is wiped between conversation turns — files your skill wrote in turn N are gone in turn N+1 unless persisted to `/mnt/user-data/outputs/`.

- **Category:** environment
- **Applies to:** Claude.ai ✅ | Claude Code ❌ (persistent) | Claude Desktop ❓
- **Verification tier:** stub
- **Severity:** State loss

## Symptom

A skill that writes a file expecting it to persist across user messages finds it missing on the next turn.

## Cause

Claude.ai's sandbox filesystem resets between turns/tasks. Exact persistence boundary is not yet pinned down.

## Verification needed

Determine the exact boundary: per-turn? per-conversation? per-task? Whether `/home/claude/` and `/mnt/user-data/outputs/` behave the same. Whether artifacts written for `present_files` survive while other paths do not.
