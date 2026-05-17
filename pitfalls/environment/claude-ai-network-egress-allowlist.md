# Claude.ai's bash has an HTTPS egress allowlist

- **Category:** environment
- **Applies to:** Claude.ai ✅ | Claude Code ❌ (open network) | Claude Desktop ❓
- **Verified on:** Claude.ai web, 2026-05-17
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that runs `curl` against an arbitrary URL from `bash_tool` on Claude.ai gets HTTP 403 with `x-deny-reason: host_not_allowed`.

## Cause

`bash_tool` network egress is allowlisted. Only certain domains are reachable (npm, pypi, github, anthropic, ubuntu, crates, and similar). Arbitrary fetches fail.

## Reproduction

Reproduced 2026-05-17 on Claude.ai web: `curl https://example.com` from `bash_tool` → HTTP 403, `x-deny-reason: host_not_allowed`.

## Fix

Use `web_fetch` for arbitrary HTTPS GETs on Claude.ai (it has different, broader allowlisting), or rewrite the skill to depend only on allowlisted domains. Code has open network egress; Desktop's bash is sandboxed (verify before assuming).

## Notes

Related: [`../cross-platform/bash-tool-three-shapes.md`](../cross-platform/bash-tool-three-shapes.md).
