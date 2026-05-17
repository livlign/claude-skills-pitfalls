# Hardcoded tool names in SKILL.md are non-portable

- **Category:** skill-structure
- **Applies to:** Claude.ai ✅ | Claude Code ✅ | Claude Desktop ✅
- **Verified on:** Claude Code, 2026-05-17
- **Verification tier:** verified
- **Severity:** Silent fallback / silent substitution

## Symptom

A SKILL.md that says "call the `Read` tool" or "use `AskUserQuestion`" works on the platform the author tested and silently degrades elsewhere — falling back to prose on Code, or substituting a similar-named tool with different parameters on Claude.ai.

## Cause

Hardcoding a platform-specific tool name in instruction text invites the silent-fallback behavior documented in [`../cross-platform/silent-fallback-when-tool-missing.md`](../cross-platform/silent-fallback-when-tool-missing.md). The model on the other platform doesn't have that tool and either prose-substitutes or picks a near-match analogue.

## Fix

Describe intent, not tool names:

- "Read the file at X" — not "Call the Read tool with X"
- "Ask the user to pick" — not "Call AskUserQuestion with options Y"
- "Search Jira for X" — not "Call mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql"

The model on each platform picks the available local tool.

## Notes

Related: [`../cross-platform/mcp-tool-name-format-diverges.md`](../cross-platform/mcp-tool-name-format-diverges.md).
