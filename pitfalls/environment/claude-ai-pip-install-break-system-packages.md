# Plain `pip install` fails on Claude.ai without `--break-system-packages`

> Plain `pip install <pkg>` on Claude.ai's bash sandbox fails with 'externally-managed-environment' (PEP 668); add `--break-system-packages` or use a venv.

- **Category:** environment
- **Applies to:** Claude.ai ✅ | Claude Code ❓ | Claude Desktop ❓
- **Verified on:** Claude.ai web, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that runs `pip install <pkg>` from `bash_tool` on Claude.ai errors out before installing.

## Cause

The sandbox treats the system Python environment as externally-managed (PEP 668). Plain `pip install` returns `error: externally-managed-environment`.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `pip install requests` → `error: externally-managed-environment`.

## Fix

Always pass `--break-system-packages` for pip installs on Claude.ai, or create a venv first.

## Notes

Whether Code's host Python and Desktop's sandbox carry the same constraint hasn't been verified. Test before assuming.
