# SKILL.md edit hot-reload behavior is unverified

- **Category:** skill-structure
- **Applies to:** Claude.ai ❓ | Claude Code ❓ | Claude Desktop ❓
- **Verification tier:** stub
- **Severity:** Unknown

## Symptom

It's not yet confirmed whether edits to the body of an *already-loaded* SKILL.md take effect on the next trigger, or whether a session restart is required to pick them up.

## Cause

We verified that *new* skill directories hot-load on Claude Code (see [`code-skill-directory-hot-load-works.md`](./code-skill-directory-hot-load-works.md)), but did not test the edit-of-existing case.

## Verification needed

Create a skill, trigger it (confirm loaded), edit the SKILL.md body, trigger again, observe whether the new content takes effect. Repeat on Claude.ai and Desktop.
