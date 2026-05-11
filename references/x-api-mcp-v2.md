# X API MCP Notes

The MCP runtime supports direct posting and targeted read/delete operations through the direct X API backend, with broader X account management delegated to an official XMCP backend. Re-check current X docs before expanding because access tiers, pricing, scopes, and rate limits change.

## Current Implementation Direction

- X has an official XMCP server that exposes X API operations from the OpenAPI specification.
- `x-publisher` includes a curated FastMCP layer in the source repo.
- Prefer running official XMCP separately and pointing `X_PUBLISHER_XMCP_URL` at it when credentials are ready.
- Add a safer product layer for agent workflows instead of exposing every raw API operation by default.

## Desired Full-Surface Capabilities

- Draft, validate, and post single posts.
- Create threads with explicit confirmation before publishing.
- Search posts and summarize recent account activity.
- Look up user/account context.
- Manage likes, follows, blocks, mutes, lists, and other account actions allowed by the API.
- Provide allow-list presets such as read-only, publisher, and full-management.
- Persist local auth safely if the chosen upstream server does not.

## Safety Requirements

- Require explicit confirmation before any mutating action.
- Separate draft/preview tools from publish/delete/follow/block tools.
- Show the exact text, target account, and affected object before posting or modifying account state.
- Keep credentials out of prompts and repository files.
- Respect API rate limits and display actionable errors when limits or access tiers block an operation.

## Composer CLI And MCP Boundary

The local composer-link CLI does not post directly. The MCP server defaults to dry-run and requires exact confirmation for mutating tools. Live calls require explicit local config and either the direct X API backend or a separately configured official XMCP backend.
