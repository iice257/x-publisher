# X API MCP V2 Notes

V2 should support direct posting and broader X account management through MCP/plugin tooling. Re-check current X docs before implementing because access tiers, pricing, scopes, and rate limits change.

## Current Direction

- X has an official XMCP server that exposes X API operations from the OpenAPI specification.
- Prefer building on, wrapping, or forking official XMCP rather than recreating raw endpoint generation.
- Add a safer product layer for agent workflows instead of exposing every raw API operation by default.

## Desired V2 Capabilities

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

## V1 Boundary

This skill does not post directly. When asked for direct posting, say that v1 only opens composer intent links and that direct posting belongs in the future MCP/API implementation.
