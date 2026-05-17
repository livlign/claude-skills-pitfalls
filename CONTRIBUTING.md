# Contributing

## Verification bar

Every new pitfall declares a verification tier:

- **`verified`** — reproduced empirically; include the reproduction (input + verbatim output, platform, date)
- **`schema-only`** — verified by reading the tool's JSON schema or description; cite the schema or system-prompt text
- **`stub`** — symptom and cause documented, no reproduction yet; acceptable as a starting point but should aim toward verification

Reproductions are strongly preferred. Don't upgrade a tier without evidence.

## Template

Use [`pitfalls/_template.md`](./pitfalls/_template.md). Follow it strictly. Stubs may omit the Reproduction and Fix sections; everything else stays.

## Platform tagging

Declare both:

- **Applies to:** which platforms the pitfall affects (Claude.ai / Claude Code / Claude Desktop) using ✅ / ❌ / ❓
- **Verified on:** which platforms you actually reproduced it on, with date

The two can differ — a pitfall may apply to a platform you haven't personally verified. Don't claim coverage you haven't tested.

## Scope

**In:** hidden constraints, schema gotchas, silent failures, cross-platform divergence, SKILL.md authoring traps, environment quirks.

**Out:** prompt engineering tips, content policy questions, bugs to file with Anthropic, opinion pieces.

## Filing format

- One PR per pitfall.
- File goes under the correct category folder, named after the specific failure (not the tool).
- If the pitfall is cross-platform, also add or update the relevant row in [`matrix/tool-inventory.md`](./matrix/tool-inventory.md).

## Tone

Concise. No padding. No marketing language. No "in conclusion." Code-style prose.
