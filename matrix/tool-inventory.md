# Tool inventory across Claude platforms

Last updated: 2026-06-14
Verified platforms: Claude.ai (web), Claude Code (CLI, darwin), Claude Desktop

For each capability, this matrix shows the tool name on each platform and notes key constraints. "—" means absent. "(deferred)" means the tool exists but requires `ToolSearch` before calling on Code/Desktop. Rows are *capabilities*, not tool names, so divergence is visible rather than hidden under names.

| Capability | Claude.ai | Claude Code | Claude Desktop | Notes / pitfall links |
|---|---|---|---|---|
| Ask user a structured question | `ask_user_input_v0` (max 3 q × 4 opt) | `AskUserQuestion` (max 4 q × 4 opt) | `AskUserQuestion` (max 4 q × 4 opt) | [schemas differ](../pitfalls/cross-platform/askuserquestion-vs-ask-user-input-v0.md); [Claude.ai caps](../pitfalls/tool-constraints/ask-user-input-v0-question-and-option-limits.md) |
| Run shell command | `bash_tool` (sandboxed, allowlisted net) | `Bash` (host, git policy, no state carryover, ~10min documented timeout) | `mcp__workspace__bash` (sandboxed, 45s cap, no state carryover) | [three shapes](../pitfalls/cross-platform/bash-tool-three-shapes.md); [Code no carryover](../pitfalls/tool-behaviors/code-bash-no-cwd-or-state-carryover.md) |
| Read a file | `view` (absolute path required; lists dirs) | `Read` (resolves to cwd, not skill dir) | `Read` | [view abs-path](../pitfalls/tool-behaviors/claude-ai-view-requires-absolute-paths.md); [Read cwd](../pitfalls/tool-behaviors/code-read-resolves-against-cwd-not-skill-dir.md) |
| Edit a file | `str_replace` (no `replace_all`) | `Edit` (requires prior Read; `replace_all` supported) | `Edit` (requires prior Read; `replace_all` supported) | [replace_all divergence](../pitfalls/cross-platform/edit-replace-all-divergence.md); [prior-read](../pitfalls/tool-behaviors/edit-requires-prior-read-same-conversation.md) |
| Create a file | `create_file` (refuses overwrite) | `Write` (silent overwrite; prior Read for existing) | `Write` (silent overwrite; prior Read for existing) | [overwrite semantics](../pitfalls/cross-platform/write-vs-create-file-overwrite-semantics.md) |
| Web search | `web_search` | `WebSearch` | `WebSearch` | |
| Web fetch | `web_fetch` (broader than bash allowlist) | `WebFetch` | `WebFetch` | [Claude.ai bash allowlist](../pitfalls/environment/claude-ai-network-egress-allowlist.md) |
| List directory | `view` (up to 2 levels) | — (use `Bash ls`) | — (use bash `ls`) | [view vs Read dir](../pitfalls/cross-platform/view-vs-read-directory-listing.md) |
| Inline image search | `image_search` (max_results ∈ [3,5]) | — | — | [bounds](../pitfalls/tool-constraints/image-search-result-count-bounds.md) |
| Search past chats by keyword | `conversation_search` (keyword-literal) | — | — (no keyword search) | [keyword meta-words](../pitfalls/tool-behaviors/conversation-search-keyword-only-matching.md); [three shapes](../pitfalls/cross-platform/past-chat-search-three-shapes.md) |
| List recent chats by time | `recent_chats` (n ≤ 20) | — (file-based memory) | `mcp__session_info__list_sessions` (deferred) | [n cap](../pitfalls/tool-constraints/recent-chats-max-n.md) |
| Surface files to user | `present_files` | — (files written to host) | `present_files` (deferred) | |
| Render inline visual (SVG/HTML) | `visualize:show_widget` family | — (markdown only) | `visualize:show_widget` family | [absent on Code](../pitfalls/cross-platform/visualization-absent-on-code.md) |
| Edit Claude's persistent memory | — | `MEMORY.md` + `memory/*.md` files | — | |
| Discover MCP connectors | `search_mcp_registry` | — | (deferred discovery) | [absent on Code](../pitfalls/cross-platform/mcp-discovery-layer-absent-on-code.md) |
| Suggest connector to user | `suggest_connectors` | — | — | [absent on Code](../pitfalls/cross-platform/mcp-discovery-layer-absent-on-code.md) |
| Find tool schema (deferred loading) | — (eager) | `ToolSearch` | `ToolSearch` | [deferred](../pitfalls/cross-platform/mcp-tools-deferred-on-code-and-desktop.md) |
| Spawn subagent | — | `Agent` | ❓ | |

## Verification status

This matrix is built from empirical testing where possible. Cells marked `❓` indicate platforms or capabilities not yet directly tested. Cells marked "—" reflect absence verified by inventory inspection.

Where a pitfall page exists, it cites a specific reproduction or schema source. Where a cell looks under-tested, contributions are welcome — add a row to a pitfall page rather than expanding this table inline.
