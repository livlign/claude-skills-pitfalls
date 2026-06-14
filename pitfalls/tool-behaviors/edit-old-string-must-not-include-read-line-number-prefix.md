# `Edit` fails with "String to replace not found" when `old_string` includes `Read`'s line-number prefix

> Claude Code's `Read` returns content in `cat -n` format (`<line>\t<text>`). If a skill copies a line from that output straight into `Edit`'s `old_string`, the leading line number and tab are not part of the file, so the match fails with "String to replace not found in file."

- **Category:** tool-behaviors
- **Applies to:** Claude.ai ❓ (see notes) | Claude Code ✅ | Claude Desktop ❓ (same `Edit`, untested)
- **Verified on:** Claude Code (Opus 4.8), 2026-06-14
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A skill reads a file, then constructs an `Edit` by reusing a line it just saw in the `Read` output. The `Edit` errors with `String to replace not found in file.` even though the text is visibly present in the file — because the copied string still carries the `<line-number>\t` prefix that `Read` prepended for display.

## Cause

`Read` displays content with a line-number prefix (`cat -n` style): `1\tfirst line`, `2\tsecond line`, etc. That prefix is presentation only — it is not in the file. `Edit` requires `old_string` to match the file's bytes exactly, so a prefixed `old_string` (`2\tsecond line`) never matches the real content (`second line`). The `Edit` tool description warns about this ("Strip the Read line prefix (line number + tab) before matching"), but it is easy to miss when assembling edits programmatically.

## Reproduction

A file whose real second line is `line two`, read back as `2\tline two`, then fed verbatim to `Edit`:

```
$ printf 'line one\nline two\nline three\n' > /tmp/probe/edit-target.txt
Read("/tmp/probe/edit-target.txt")
→ 1\tline one
  2\tline two
  3\tline three

Edit(file_path=".../edit-target.txt", old_string="2\tline two", new_string="2\tline TWO edited")
→ String to replace not found in file.
  String: 2	line two
```

Dropping the `2\t` prefix (`old_string="line two"`) matches and succeeds.

## Fix

Build `old_string` from the file's actual content, not from `Read`'s displayed output: strip the leading line number and the tab. The text after the first tab on a `Read` line is the real content.

## Notes

This is distinct from, but often confused with, the prior-`Read` requirement ([`edit-requires-prior-read-same-conversation.md`](./edit-requires-prior-read-same-conversation.md)) — there the `Read` is missing entirely; here the `Read` happened but its formatting leaked into the edit. `old_string` must also be unique unless `replace_all` is set ([`../cross-platform/edit-replace-all-divergence.md`](../cross-platform/edit-replace-all-divergence.md)). Claude.ai's `view` also shows line numbers, so the same trap plausibly applies to `str_replace` there, but this was verified only on Code.
