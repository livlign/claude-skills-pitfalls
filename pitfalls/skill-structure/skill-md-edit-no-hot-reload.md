# Edits to an already-loaded SKILL.md do not hot-reload mid-session (Claude Code)

> On Claude Code, *new* skill directories hot-load on the next turn — but **edits to the body of an already-loaded SKILL.md are not picked up mid-session**. The content is cached at first load; a session restart is required to see changes.

- **Category:** skill-structure
- **Applies to:** Claude.ai ❓ | Claude Code ✅ | Claude Desktop ❓
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Stale content / silent

## Symptom

A skill author edits a SKILL.md that has already been triggered once in the current session, re-triggers the skill, and sees the *old* instructions take effect — silently. Nothing signals that the injected content is stale.

## Cause

Claude Code caches a skill's body at first load for the session. Subsequent invocations inject the cached content, not the current on-disk file. This is the opposite of the *new-directory* case, where a freshly added skill is hot-loaded on the next turn (see [`code-skill-directory-hot-load-works.md`](./code-skill-directory-hot-load-works.md)).

## Reproduction

Reproduced on Claude Code (Opus 4.8), 2026-06-14:

```
1. Create ~/.claude/skills/pitfall-hotreload-test/SKILL.md whose body says
   "output exactly: MARKER-VERSION-ONE".
2. Invoke the skill → it hot-loads and injects MARKER-VERSION-ONE.
3. Edit the SKILL.md body in place: MARKER-VERSION-ONE → MARKER-VERSION-TWO
   (confirmed on disk with grep).
4. Invoke the same skill again → it injects MARKER-VERSION-ONE (the cached,
   pre-edit content), NOT version two.
```

The on-disk file held `MARKER-VERSION-TWO`, yet the second invocation still served `MARKER-VERSION-ONE` — proving the body is cached at first load.

## Fix

After editing an already-triggered SKILL.md, restart the Claude Code session (or start a fresh conversation) before relying on the new content. During iterative authoring, don't trust mid-session re-triggers to reflect your latest edits.

## Notes

Claude.ai and Desktop are not yet tested for this case (`❓`). The companion positive finding — that *new* skill directories are hot-loaded without a restart — is in [`code-skill-directory-hot-load-works.md`](./code-skill-directory-hot-load-works.md).
