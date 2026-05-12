---
name: x-publisher
description: Draft, validate, split into threads, open X/Twitter composer links, and use the dry-run-first MCP workflow for live X posting when local credentials are explicitly configured. Use when Codex needs to prepare social launch copy, repo/project announcements, X posts, tweet threads, or shareable publishing drafts where the user should manually review before posting.
---

# X Publisher

## Overview

Prepare X posts safely from local drafts or through the dry-run-first MCP runtime. The normal publishing path should be browser-first because most users will not have paid X developer console access. The local CLI creates validated composer links; the MCP runtime can create posts/threads, delete posts, look up users/posts, and delegate broader account-management operations to an official XMCP backend when configured. Live API/XMCP posting is opt-in only and still requires exact confirmation.

## Workflow

1. Draft concise post text in the user's voice and keep the strongest point first.
2. Run `scripts/x_publish.py validate` before sharing any post or thread.
3. Use `scripts/x_publish.py intent` for a single post composer link.
4. Use `scripts/x_publish.py thread` for long Markdown/text drafts.
5. Treat browser posting as the default path. Before suggesting live API/XMCP posting, ask whether the user has a free or paid X developer account; free accounts often cannot publish through API/XMCP, so prefer browser use unless the user confirms suitable paid access and local credentials are configured.

## Commands

Run commands from this skill folder:

```bash
python scripts/x_publish.py draft --text "Shipped x-publisher: local drafts plus a dry-run-first MCP posting path."
python scripts/x_publish.py validate --text "Shipped x-publisher" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` only after the generated URL looks correct.

## Guardrails

- Do not post directly from the local composer-link CLI. If asked for direct posting, use the MCP guidance in `references/mcp-usage.md`, require exact confirmation for mutating tools, and keep live credentials in environment variables only.
- Do not request or store X API keys in prompts or committed files.
- Treat local character counts as a conservative approximation. For direct API posting, re-check current X docs and use the official `twitter-text` guidance.
- Prefer shortening the draft before splitting into a thread unless the user explicitly wants a thread.
- Treat the source repo as authoritative. Sync the installed skill from the source repo with `python tools/install_local.py`.
- If API/XMCP publishing fails with credits, subscription, or access-tier errors, use the returned browser fallback plan. Operate only a locally signed-in browser session and verify the visible account/text before clicking Post.
- For hands-free fallback in v2, use `create_browser_fallback_plan` first, then `execute_browser_fallback` only with exact confirmation, `execute=True`, a target account username, and the signed-in Microsoft Edge Work profile visible.

## References

- `references/posting-workflow.md`: Practical draft, validation, and composer-link workflow.
- `references/mcp-usage.md`: How to list and run the MCP runtime.
- `references/x-api-mcp-v2.md`: Notes for the full X API MCP/plugin surface.
