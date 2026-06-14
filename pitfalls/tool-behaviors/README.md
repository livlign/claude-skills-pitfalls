# Tool behavior pitfalls

Undocumented runtime behaviors of individual tools — prerequisite calls, path resolution rules, hidden policies embedded in tool descriptions, state-carryover assumptions that don't hold.

Common questions this page answers:

- Why does `Edit` fail with "you must Read the file first" even though my skill just wrote it?
- Why does `Read("foo.md")` work in one turn and fail in the next?
- Why does my shell variable disappear between bash calls on Claude Desktop?
- Why does Claude Code refuse a `git commit --amend` my skill asked for?

## Entries

- [Claude.ai's `view` rejects relative paths and bare filenames](./claude-ai-view-requires-absolute-paths.md)
- [Claude Code's `Bash` embeds a strict git policy in its tool description](./code-bash-embedded-git-policy.md)
- [Claude Code's `Bash` does not persist cwd or shell state between calls](./code-bash-no-cwd-or-state-carryover.md)
- [Claude Code's `Read` resolves relative paths against cwd, not the skill directory](./code-read-resolves-against-cwd-not-skill-dir.md)
- [`conversation_search` is keyword-only; meta-words poison results](./conversation-search-keyword-only-matching.md)
- [Claude Desktop's bash has no state carryover between calls](./desktop-bash-no-state-carryover.md)
- [`Edit` requires a prior `Read` in the same conversation](./edit-requires-prior-read-same-conversation.md)
- [`Edit` fails with "String to replace not found" when `old_string` includes Read's line-number prefix](./edit-old-string-must-not-include-read-line-number-prefix.md)
- [`Write` requires a prior `Read` for existing files](./write-requires-prior-read-for-existing-files.md)

See also: [back to all categories](../)
