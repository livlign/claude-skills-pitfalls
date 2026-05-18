# Cross-platform pitfalls

Skills that work on one Claude surface (Claude.ai web, Claude Code CLI, Claude Desktop) can fail silently or behave differently on the others. This page indexes the divergences — same intent, different tool name, different schema, or different result shape.

Common questions this page answers:

- Why does my skill work on Claude.ai but not Claude Code?
- Which tools exist on Claude Desktop but not Claude.ai?
- Do `AskUserQuestion` and `ask_user_input_v0` behave the same?
- Why did `Write` overwrite my file when `create_file` refused to?

## Entries

- [`AskUserQuestion` and `ask_user_input_v0` are different tools](./askuserquestion-vs-ask-user-input-v0.md)
- [The bash tool has three structurally different shapes across platforms](./bash-tool-three-shapes.md)
- [Don't-assume-instructions are unenforceable without an in-skill picker](./dont-assume-instructions-unenforceable-without-picker.md)
- [`Edit.replace_all` exists on Code/Desktop; Claude.ai's `str_replace` has no equivalent](./edit-replace-all-divergence.md)
- [MCP discovery (`search_mcp_registry`, `suggest_connectors`) is absent on Claude Code](./mcp-discovery-layer-absent-on-code.md)
- [MCP tool name format diverges across platforms](./mcp-tool-name-format-diverges.md)
- [MCP tool schemas are deferred on Claude Code and Desktop](./mcp-tools-deferred-on-code-and-desktop.md)
- [Past-chat search has a different shape on each platform](./past-chat-search-three-shapes.md)
- [Skills fail silently when their named tool doesn't exist](./silent-fallback-when-tool-missing.md)
- [`view` lists directories; `Read` cannot](./view-vs-read-directory-listing.md)
- [Inline SVG/HTML visualization is absent on Claude Code](./visualization-absent-on-code.md)
- [`Write` overwrites silently; `create_file` refuses to overwrite](./write-vs-create-file-overwrite-semantics.md)

See also: [compatibility matrix](../../matrix/tool-inventory.md) · [back to all categories](../)
