---
name: x-publisher
description: Draft, validate, split into threads, and open X/Twitter composer intent links for posts without direct API posting. Use when Codex needs to prepare social launch copy, repo/project announcements, X posts, tweet threads, or shareable publishing drafts where the user should manually review before posting.
---

# X Publisher

## Overview

Prepare X posts safely from local drafts. V1 creates validated composer links only; it never posts directly and never asks for X API credentials.

## Workflow

1. Draft concise post text in the user's voice and keep the strongest point first.
2. Run `scripts/x_publish.py validate` before sharing any post or thread.
3. Use `scripts/x_publish.py intent` for a single post composer link.
4. Use `scripts/x_publish.py thread` for long Markdown/text drafts.
5. Tell the user that the browser composer is the final review step and they must click Post manually.

## Commands

Run commands from this skill folder:

```bash
python scripts/x_publish.py draft --text "Shipped x-publisher v1: local drafts, validation, threading, and X composer links."
python scripts/x_publish.py validate --text "Shipped x-publisher v1" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher v1" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` only after the generated URL looks correct.

## Guardrails

- Do not post directly from this skill. If asked for direct posting, explain that v1 only opens X composer links and read `references/x-api-mcp-v2.md` for the future MCP path.
- Do not request or store X API keys for v1.
- Treat local character counts as a conservative approximation. For direct API posting, re-check current X docs and use the official `twitter-text` guidance.
- Prefer shortening the draft before splitting into a thread unless the user explicitly wants a thread.

## References

- `references/posting-workflow.md`: Practical draft, validation, and composer-link workflow.
- `references/x-api-mcp-v2.md`: Notes for the future full X API MCP/plugin direction.
