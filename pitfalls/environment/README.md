# Environment pitfalls

Sandbox, filesystem, and network constraints that affect what skills can do at runtime — and that often differ from the developer's local machine.

Common questions this page answers:

- Why do files my skill wrote disappear between turns on Claude.ai?
- Why does `pip install foo` fail with "externally-managed-environment" on Claude.ai?
- Why does my skill's `curl` to a custom domain fail on Claude.ai?
- Is Claude Desktop's bash actually my host shell?

## Entries

- [Claude.ai's sandbox filesystem resets between turns](./claude-ai-filesystem-resets-between-turns.md)
- [`/mnt/user-data/uploads/` is read-only on Claude.ai](./claude-ai-mnt-user-data-uploads-readonly.md)
- [Claude.ai's bash has an HTTPS egress allowlist](./claude-ai-network-egress-allowlist.md)
- [Plain `pip install` fails on Claude.ai without `--break-system-packages`](./claude-ai-pip-install-break-system-packages.md)
- [Claude Desktop's bash runs in a sandbox, not the user's real filesystem](./desktop-bash-sandboxed-not-host.md)

See also: [back to all categories](../)
