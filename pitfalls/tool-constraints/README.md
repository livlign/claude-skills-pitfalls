# Tool constraint pitfalls

Hidden limits on a single tool — schema-enforced ceilings on counts, sizes, and timeouts that aren't surfaced in skill-authoring guidance.

Common questions this page answers:

- Why does `ask_user_input_v0` fail with a schema validation error when I pass 4 questions?
- What's the maximum `timeout` for `Bash` on Claude Code? On Claude Desktop?
- Why does `recent_chats` cap out at 20 results?
- Why is `image_search.max_results=10` rejected?

## Entries

- [`ask_user_input_v0` enforces a 3-question, 4-option ceiling](./ask-user-input-v0-question-and-option-limits.md)
- [Claude Code's `Bash` caps `timeout` at 600000ms (10 minutes)](./code-bash-600-second-ceiling.md)
- [Claude Desktop's bash caps `timeout_ms` at 45 seconds](./desktop-bash-45-second-ceiling.md)
- [`image_search.max_results` is bounded to [3, 5]](./image-search-result-count-bounds.md)
- [`recent_chats.n` caps at 20](./recent-chats-max-n.md)

See also: [back to all categories](../)
