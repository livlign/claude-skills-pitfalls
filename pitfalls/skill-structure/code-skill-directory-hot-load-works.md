# New skill directories hot-load on Claude Code (positive finding)

> Positive finding: dropping a new skill directory into the skills folder on Claude Code is picked up on the next turn without restarting the session.

- **Category:** skill-structure
- **Applies to:** Claude Code ✅
- **Verified on:** Claude Code, 2026-05-17; re-confirmed Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Informational — not a pitfall, a positive finding worth documenting

## Symptom

Earlier testing suggested that skills added mid-session weren't picked up. They are.

## Cause

Subsequent testing (2026-05-17) confirmed Claude Code's harness does hot-load new `~/.claude/skills/<name>/` directories on the next turn. No session restart required.

## Notes

Included to correct earlier hearsay. If a new skill doesn't appear in the inventory, suspect the auto-mode classifier blocked the write of `SKILL.md`, not the loader.

Note the contrast with *edits to an already-loaded SKILL.md*, which are **not** hot-reloaded mid-session — that body is cached at first load. See [`skill-md-edit-no-hot-reload.md`](./skill-md-edit-no-hot-reload.md).
