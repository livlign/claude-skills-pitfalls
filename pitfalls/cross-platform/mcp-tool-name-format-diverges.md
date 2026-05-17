# MCP tool names use different formats on Claude.ai vs Code/Desktop

- **Category:** cross-platform
- **Applies to:** Claude.ai uses `Server:tool` | Claude Code/Desktop use `mcp__claude_ai_Server__tool`
- **Verified on:** 2026-05-17 across platforms
- **Verification tier:** verified
- **Severity:** Hard error

## Symptom

A SKILL.md that hardcodes a fully-qualified MCP tool name works on one platform and is invisible on the other.

## Cause

Same MCP server, same underlying tool, different fully-qualified names. Claude.ai: `Atlassian:searchJiraIssuesUsingJql`. Code/Desktop: `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql`.

## Fix

Describe the *capability* in the SKILL.md ("search Jira for X") rather than the tool name. Let each platform's Claude pick the locally-correct fully-qualified name.

## Notes

Related: [`mcp-tools-deferred-on-code-and-desktop.md`](./mcp-tools-deferred-on-code-and-desktop.md) and [`silent-fallback-when-tool-missing.md`](./silent-fallback-when-tool-missing.md).
