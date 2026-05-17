# New skill directories hot-load on Claude Code (positive finding)

**Category:** skill-structure
**Applies to:** Claude Code ✅
**Verified on:** Claude Code, 2026-05-17
**Verification tier:** verified
**Severity:** Informational — not a pitfall, a positive finding worth documenting

## Symptom

Earlier testing suggested that skills added mid-session weren't picked up. They are.

## Cause

Subsequent testing (2026-05-17) confirmed Claude Code's harness does hot-load new `~/.claude/skills/<name>/` directories on the next turn. No session restart required.

## Notes

Included to correct earlier hearsay. If a new skill doesn't appear in the inventory, suspect the auto-mode classifier blocked the write of `SKILL.md`, not the loader.

Whether *edits to an already-loaded SKILL.md* hot-reload is a separate question not yet verified. See [`skill-md-edit-hot-reload-unverified.md`](./skill-md-edit-hot-reload-unverified.md).
